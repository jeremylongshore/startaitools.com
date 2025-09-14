# Claude Commands Guide

## What are Claude Commands?

Claude Commands are custom shortcuts that make it easier to trigger specific workflows in Claude Code. Instead of typing long instructions, you can use simple commands like `/create-prd` to start complex processes.

## How Claude Commands Work

1. **Command Files**: Stored in `.claude/commands/` directory
2. **Naming**: File name becomes the command (e.g., `create-prd.md` → `/create-prd`)
3. **Activation**: Type `/` followed by the command name in Claude Code
4. **Scope**: Can be project-specific or global

## Available Commands in This Project

### `/create-prd`
Creates a Product Requirements Document for a new feature
- Asks clarifying questions
- Generates structured PRD
- Saves to `/tasks/` directory

### `/generate-tasks`
Generates a task list from an existing PRD
- Lists available PRDs
- Creates parent tasks and sub-tasks
- Saves as `tasks-[prd-name].md`

### `/process-tasks`
Works through a task list systematically
- Completes one sub-task at a time
- Waits for approval between tasks
- Commits when parent tasks complete

### `/create-adr`
Creates an Architecture Decision Record
- Documents important technical decisions
- Follows ADR template format
- Numbers sequentially

## Setting Up Claude Commands

### Project-Level Commands (This Project)
```bash
# Already set up in this project:
.claude/commands/
├── create-prd.md
├── generate-tasks.md
├── process-tasks.md
└── create-adr.md
```

### Global Commands (All Projects)
To make these commands available in ALL your projects:

1. **Find your Claude global directory**:
   ```bash
   # Usually located at:
   ~/.claude/         # Linux/Mac
   %USERPROFILE%\.claude\  # Windows
   ```

2. **Create global commands directory**:
   ```bash
   mkdir -p ~/.claude/commands
   ```

3. **Copy commands to global directory**:
   ```bash
   cp .claude/commands/*.md ~/.claude/commands/
   ```

4. **Restart Claude Code**:
   Type `/exit` and restart

## Creating Your Own Commands

### Basic Command Structure
```markdown
# File: .claude/commands/my-command.md

[Brief description of what the command does]

[Detailed instructions for Claude to follow]

[Any parameters or options to handle]
```

### Example: Create a Test Command
```markdown
# File: .claude/commands/run-tests.md

Please run the test suite for this project.

1. Identify the testing framework (Jest, pytest, etc.)
2. Run the appropriate test command
3. Summarize the results
4. If tests fail, offer to help fix them
```

## Command Best Practices

1. **Keep commands focused**: One command = one workflow
2. **Provide clear instructions**: Tell Claude exactly what to do
3. **Handle edge cases**: What if files don't exist?
4. **Use consistent naming**: Use kebab-case (e.g., `create-prd`, not `CreatePRD`)
5. **Document parameters**: If command needs input, specify how

## Advanced Features

### Chaining Commands
Commands can reference other commands:
```markdown
# File: .claude/commands/full-feature.md

Please help me build a complete feature:
1. First use /create-prd to define requirements
2. Then use /generate-tasks to create task list
3. Finally use /process-tasks to implement
```

### Conditional Logic
```markdown
# File: .claude/commands/smart-build.md

Check the project type and run appropriate build:
- If package.json exists: npm run build
- If Cargo.toml exists: cargo build
- If go.mod exists: go build
```

## Troubleshooting

### Commands Not Working?
1. **Check file location**: Must be in `.claude/commands/`
2. **Restart Claude**: Exit and restart after adding commands
3. **Check file extension**: Must be `.md` files
4. **Verify syntax**: Type `/` to see available commands

### Command Conflicts
- Project commands override global commands
- If same command exists in both, project version is used

## Benefits of Using Commands

1. **Consistency**: Same workflow every time
2. **Speed**: Quick to trigger complex processes
3. **Documentation**: Commands serve as workflow documentation
4. **Shareability**: Can share commands with team
5. **Customization**: Tailor Claude to your specific needs

## Tips for This Project

- Use `/create-prd` when planning new features
- Use `/generate-tasks` to break down PRDs into actionable items
- Use `/process-tasks` to systematically implement features
- Use `/create-adr` to document architectural decisions

## Next Steps

1. Try the commands: Type `/create-prd` to start
2. Customize existing commands to your preferences
3. Create new commands for your common workflows
4. Share useful commands with the community

---

*Remember: After adding or modifying commands, restart Claude Code with `/exit` for changes to take effect.*