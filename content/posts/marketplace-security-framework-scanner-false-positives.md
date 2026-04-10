+++
title = 'Marketplace Security Framework and the False Positive Fight'
slug = 'marketplace-security-framework-scanner-false-positives'
date = 2025-10-13T10:00:00-05:00
draft = false
tags = ["security", "ci-cd", "open-source", "claude-code-plugins"]
categories = ["Development Journey"]
description = "Building a 6-vector security framework for the plugin marketplace, then spending half the day teaching the scanner what isn't a threat."
+++

Three days after launching the Claude Code plugin marketplace, the security story was "trust me, I checked." That needed to change before anyone installed a community plugin on their machine.

## The Security Framework

The day started with a full SECURITY.md — 407 lines covering a 6-vector threat model, three trust tiers (Community, Verified, Featured), responsible disclosure policy, and SLA commitments. Standard structure, but adapted to the plugin marketplace context where users execute community code inside their development environment.

The trust tiers map to concrete verification levels:

| Tier | Verification | Badge |
|------|-------------|-------|
| Community | Automated scans only | None |
| Verified | Manual review + author identity | Checkmark |
| Featured | Full audit + ongoing monitoring | Star |

This mirrors what npm, VS Code extensions, and Docker Hub do — nothing revolutionary, but the alternative was shipping plugins with zero trust signals.

## Four Automated Scans

Alongside the policy docs, four CI security scans went into the GitHub Actions pipeline:

1. **Secrets detection** — scan for API keys, tokens, private keys in plugin submissions
2. **Dangerous pattern matching** — flag `rm -rf`, `eval()`, `exec()`, and similar
3. **Suspicious URL scanning** — catch data exfiltration endpoints
4. **MCP dependency scanning** — verify MCP server dependencies are from known sources

Plus a User Security Guide (352 lines) and CodeQL integration for deeper static analysis. The guide walks plugin users through verifying trust tiers, checking scan results, and reporting suspicious plugins — because automated scanning only works if users know what the scanner does and doesn't catch.

Total additions for the framework: roughly 970 lines of security documentation and CI configuration across 4 new files.

## The False Positive Problem

Here's where the day got interesting. The scanner started flagging everything. Four consecutive fix commits tell the story:

**Fix 1**: The secrets detector flagged placeholder values. Lines like `API_KEY=your-key-here` in README examples triggered alerts. Fix: exclude known placeholder patterns (`your-key-here`, `xxx`, `example`).

**Fix 2**: AWS example keys and test tokens in documentation. The scanner correctly identified the pattern `AKIA...` but incorrectly classified documentation examples as real credentials. Fix: allowlist known AWS example key prefixes from docs.

**Fix 3**: Documentation patterns themselves. Security guides that *describe* what malicious code looks like were getting flagged as malicious. The scanner was essentially flagging its own user guide. Fix: exclude `*.md` and documentation directories from certain scan categories.

**Fix 4**: The dangerous pattern detector flagged `rm -rf /var/cache` in a legitimate cleanup script the same way it flagged `rm -rf /`. Fix: only flag `rm -rf /` (root), not `rm -rf /var/` or other specific paths. Similarly, `eval()` mentions in README explanations aren't the same as `eval()` calls in executable code.

```yaml
# Before: flags everything
- name: Check dangerous patterns
  run: grep -rn 'eval\|exec\|rm -rf' plugins/

# After: context-aware scanning
- name: Check dangerous patterns
  run: |
    grep -rn 'rm -rf /' plugins/ --include='*.py' --include='*.js' \
      | grep -v '/var/' | grep -v '/tmp/' | grep -v '/cache/'
    grep -rn 'eval(' plugins/ --include='*.py' --include='*.js' \
      | grep -v 'README' | grep -v '*.md'
```

## What This Pattern Teaches

Security scanners are easy to write and hard to tune. The initial implementation took maybe two hours. The false positive fixes took the rest of the day — four separate commits, each one a judgment call about where to draw the line.

The core tension: every exclusion rule you add makes the scanner quieter but also blinds it to a class of real threats. Excluding `*.md` from dangerous pattern detection means a malicious actor could hide executable code in a markdown file (unlikely in this context, but not impossible). Excluding `rm -rf /var/` means a plugin could wipe a user's `/var/lib/` directory. Each exclusion is a bet about which threat is less likely.

The right mental model isn't "make it pass" — it's "make it pass for the right reasons." A green CI check should mean "we scanned this and found nothing concerning," not "we scanned this and ignored everything we found."

The marketplace shipped v1.0.37 with the full security infrastructure in place. Not because any of this is novel, but because an open-source project that accepts community code without automated security checks is a liability waiting to happen. And not because the scanner is perfect — it's not — but because an imperfect scanner that you iterate on is better than no scanner at all.

---

### Related Posts

- [Software Supply Chain Security](/posts/software-supply-chain-security/) — the broader context for why plugin security matters
- [Claude Code Plugin Marketplace Launch](/posts/claude-code-plugin-marketplace-launch/) — the marketplace this security framework protects
- [Marketplace Scaling: Learning Paths and Finance Plugins](/posts/marketplace-scaling-learning-paths-finance-plugins/) — the previous day's marketplace work
