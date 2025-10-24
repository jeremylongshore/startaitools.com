+++
title = 'Multi-User Linux Architecture: Debugging Production Permission Systems'
date = 2025-10-23T14:45:00-05:00
draft = false
tags = ["systems-architecture", "linux", "debugging", "production", "infrastructure"]
+++

When you're architecting multi-user Linux systems and encounter permission errors, the solution reveals your engineering maturity. Do you patch with `chmod 777` or design a scalable architecture? This is how I approached debugging and fixing a production multi-user permission system.

## The Challenge

**Scenario:** Multi-user Linux environment running Claude Code across two user accounts with shared configuration requirements.

**Initial error state:**
```
EACCES: permission denied, open
syscall: "open", errno: -13, code: "EACCES"
```

**Business requirements:**
- Two independent user accounts need application access
- Shared configuration (plugins, tools, commands)
- No permission conflicts between users
- Scalable to additional users
- Production-grade reliability

**The question:** How do you architect shared resources without creating ownership battles?

## My Approach: Systematic Problem Decomposition

### Phase 1: Investigation and Root Cause Analysis

I started with the fundamentals: understanding what was actually failing before proposing solutions.

**Discovery process:**
1. Examined error context - which system call failed?
2. Checked current user permissions and home directory ownership
3. Identified that the application was trying to write logs/config
4. Traced ownership of existing files and directories
5. Found ownership pollution from cross-user debugging attempts

**Key finding:** The permission error wasn't about running the application—it was about the application's inability to write to directories it expected to own.

```bash
# Found the root cause
ls -la /home/jeremy/.claude/debug/
drwx------ 2 admincostplus admincostplus 12288 Oct 23 14:21 debug
```

User `admincostplus` had created directories in `jeremy`'s home during troubleshooting, leaving jeremy unable to write to his own `.claude/debug` directory.

**Professional insight:** Always trace ownership chains in multi-user environments. The obvious permission issue often masks deeper ownership problems.

## Phase 2: Architectural Design

Instead of patching the immediate problem, I designed a production-ready multi-user architecture using three Linux primitives:

### 1. Shared Directory with Group Ownership

```bash
SHARED=/opt/claude-shared
GROUP=claudeusers

# Create shared location with setgid bit
mkdir -p "$SHARED"
chmod 2775 "$SHARED"  # setgid ensures group inheritance
```

**Why this works:** The setgid bit (2 in 2775) forces all new files to inherit the directory's group, preventing ownership conflicts.

### 2. Symlink Architecture for Admin Users

```bash
# Admin user's home directories become symlinks
ln -s /opt/claude-shared/.claude /home/admincostplus/.claude
ln -s /opt/claude-shared/.claude-code /home/admincostplus/.claude-code
```

**Strategic benefit:** Admin operations transparently redirect to shared storage. The application doesn't know it's writing to a shared location.

### 3. Real Directories for Master User

The master user (`jeremy`) maintains real directories in his home, providing:
- Full ownership and control
- Ability to test changes before syncing to shared
- Rollback capability if shared config breaks
- Independence from shared storage availability

## Phase 3: Implementation and Edge Cases

### The Ownership Cleanup Problem

After implementing the architecture, the master user still hit EACCES. Investigation revealed:

```bash
# Jeremy's directories were polluted with admincostplus ownership
find /home/jeremy/.claude -user admincostplus -o -group admincostplus
# Returned ~100 files
```

**Solution:**
```bash
sudo chown -R jeremy:jeremy /home/jeremy/.claude
sudo chown -R jeremy:jeremy /home/jeremy/.claude-code
```

**Lesson learned:** In multi-user debugging, always clean up ownership after cross-user operations. Silent ownership pollution creates hard-to-diagnose issues later.

### The Environment Variable Bug

The `CLAUDE_CODE_HOME` environment variable wasn't being set due to shell escaping:

```bash
# Original (broken)
[ "\$USER" = "admincostplus" ] && export CLAUDE_CODE_HOME="/opt/claude-shared/.claude-code"

# Fixed (proper variable expansion)
[ "$USER" = "admincostplus" ] && export CLAUDE_CODE_HOME="/opt/claude-shared/.claude-code"
```

**Professional approach:** Test each configuration layer independently. Don't assume scripts worked—verify every assumption.

## The Complete Production Solution

Here's the final architecture script that runs in production:

```bash
#!/bin/bash
# Production multi-user configuration
# Handles: ownership, permissions, symlinks, environment, ACLs

MASTER_USER=jeremy
ADMIN_USER=admincostplus
SHARED=/opt/claude-shared
GROUP=claudeusers

# 1. Group creation and membership
getent group "$GROUP" >/dev/null || groupadd "$GROUP"
usermod -a -G "$GROUP" "$MASTER_USER"
usermod -a -G "$GROUP" "$ADMIN_USER"

# 2. Shared directory with setgid
mkdir -p "$SHARED"
chown -R "$MASTER_USER:$GROUP" "$SHARED"
chmod 2775 "$SHARED"

# 3. Seed shared from master user's config
DIRS=(".claude" ".claude-code" ".config/claude-code" ".local/share/claude-code")
for rel in "${DIRS[@]}"; do
  src="/home/$MASTER_USER/$rel"
  dst="$SHARED/$rel"
  [ -d "$src" ] && rsync -a --delete "$src"/ "$dst"/ || mkdir -p "$dst"
done

# 4. Create symlinks for admin user
for rel in "${DIRS[@]}"; do
  link="/home/$ADMIN_USER/$rel"
  target="$SHARED/$rel"
  [ -e "$link" ] && [ ! -L "$link" ] && \
    mv "$link" "$link.bak-$(date +%Y%m%d-%H%M%S)"
  rm -rf "$link"
  ln -s "$target" "$link"
done

# 5. Set permissions with ACLs
chown -R "$MASTER_USER:$GROUP" "$SHARED"
find "$SHARED" -type d -exec chmod 2775 {} +
setfacl -R -m g:$GROUP:rwx -m d:g:$GROUP:rwx "$SHARED" 2>/dev/null || true

# 6. Environment configuration
cat >/etc/profile.d/claude-code-admin.sh <<'EOF'
[ "$USER" = "admincostplus" ] && export CLAUDE_CODE_HOME="/opt/claude-shared/.claude-code"
EOF
chmod 644 /etc/profile.d/claude-code-admin.sh

echo "✅ Multi-user architecture deployed"
```

## Verification Methodology

I implemented comprehensive smoke tests to verify each layer:

```bash
# Layer 1: Symlink resolution
sudo -iu admincostplus bash -lc 'readlink -f ~/.claude'
# Expected: /opt/claude-shared/.claude

# Layer 2: Master user isolation
sudo -iu jeremy bash -lc 'readlink -f ~/.claude'
# Expected: /home/jeremy/.claude (real directory)

# Layer 3: Write permissions (both users)
sudo -iu admincostplus bash -lc 'touch ~/.claude/test.txt && rm ~/.claude/test.txt'
sudo -iu jeremy bash -lc 'touch ~/.claude/test.txt && rm ~/.claude/test.txt'
# Expected: Both succeed

# Layer 4: Application execution
sudo -iu jeremy bash -lc 'claude --version'
# Expected: 2.0.25 (Claude Code)

sudo -iu admincostplus bash -lc 'claude --version'
# Expected: 2.0.8 (Claude Code)

# Layer 5: Environment variables
sudo -iu admincostplus bash -lc 'echo $CLAUDE_CODE_HOME'
# Expected: /opt/claude-shared/.claude-code
```

**All tests passed.** Zero permission errors, zero ownership conflicts, both users operational.

## Technical Skills Demonstrated

**Linux Systems Architecture:**
- Multi-user permission design with groups and ACLs
- Setgid bit usage for automatic group inheritance
- Symlink-based transparent redirection
- Environment variable management for user-specific config

**Debugging Methodology:**
- Systematic root cause analysis (ownership vs permissions)
- Layer-by-layer verification of complex systems
- Ownership pollution detection and cleanup
- Edge case identification (escaped variables, stale processes)

**Production Engineering:**
- Scalable architecture (easily extends to N users)
- Comprehensive smoke tests at each layer
- Backup strategy (timestamped backups before destructive operations)
- Documentation and verification procedures

**Problem-Solving Approach:**
- Started with investigation, not solutions
- Designed architecture before implementing
- Tested each component independently
- Iterated when edge cases emerged

## Business Impact

**Before:**
- Manual permission fixes after each conflict
- Users blocked from working due to EACCES errors
- No clear ownership model
- Configuration drift between users

**After:**
- Zero permission conflicts between users
- Automatic group inheritance prevents ownership issues
- Shared configuration with master/admin separation
- Architecture scales to additional users with one command

**Scalability:** Adding a third user requires:
1. `usermod -a -G claudeusers newuser`
2. Create symlinks to `/opt/claude-shared`
3. Done.

## Related Work

- [Scaling AI Systems: Disaster Recovery and Production Batch Processing](https://jeremylongshore.com/posts/scaling-ai-systems-disaster-recovery-production-batch-processing/) - Production system architecture and reliability
- [Building Production CI/CD: Documentation to Deployment](https://jeremylongshore.com/posts/building-production-ci-cd-documentation-to-deployment/) - Infrastructure automation and deployment patterns
- [Automating Developer Workflows with Custom AI Commands](https://jeremylongshore.com/posts/automating-developer-workflows-custom-ai-commands/) - Developer experience and productivity optimization

## Key Takeaways for Engineering Leaders

**1. Architecture Over Patches**
The difference between junior and senior engineers: juniors patch symptoms (`chmod 777`), seniors architect solutions (group permissions + symlinks + setgid).

**2. Systematic Debugging**
In production systems, assume nothing. Verify:
- Ownership at every layer
- Permissions on files AND directories
- Group membership and inheritance
- Environment variables in actual shells
- Application behavior with actual workloads

**3. Scalability by Design**
This architecture supports 2 users or 200 users with the same code. Design for scale from day one.

**4. Test Before Declaring Success**
Scripts can fail silently. Comprehensive smoke tests are not optional—they're how you know your solution actually works.

## The Engineering Mindset

When faced with `EACCES: permission denied`, most developers Google "how to fix permission denied." Senior engineers ask:

1. What is the system call that's failing?
2. What file/directory is being accessed?
3. Who owns it and what are the permissions?
4. What is the user context and group membership?
5. What is the desired end state architecture?

This mindset shift—from "fix the error" to "design the system"—is what separates debugging from engineering.

**Final result:** Production-grade multi-user Linux architecture with zero permission conflicts, automatic group inheritance, and verified operation across both user accounts.

This is how you build systems that scale.
