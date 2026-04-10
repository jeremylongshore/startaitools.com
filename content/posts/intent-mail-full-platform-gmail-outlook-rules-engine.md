+++
title = 'Intent Mail: Full Email Platform in a Day — Gmail, Outlook, and a Rules Engine'
slug = 'intent-mail-full-platform-gmail-outlook-rules-engine'
date = 2025-12-23T10:00:00-06:00
draft = false
tags = ["email", "oauth", "sqlite", "mcp", "rules-engine", "architecture", "microsoft-graph"]
categories = ["Technical Deep-Dive"]
description = "35 commits building intent-mail from scratch: SQLite+FTS5 storage, Gmail OAuth with delta sync, Outlook via MS Graph, automation rules engine with dry-run, and MCP tools for agent-driven email management."
+++

35 commits in one repo. By the end of December 23rd, intent-mail was a working email platform with two provider connectors, full-text search, threaded send, attachment support, and a rules engine that could automate triage without touching the inbox until you said go.

## The Storage Layer: SQLite + FTS5

Email data has two access patterns: exact lookup (give me this thread) and fuzzy search (find all emails about the deployment incident). SQLite handles the first pattern natively. FTS5 — SQLite's full-text search extension — handles the second.

```sql
-- Core message table
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    thread_id TEXT NOT NULL,
    provider TEXT NOT NULL,  -- 'gmail' or 'outlook'
    subject TEXT,
    sender TEXT,
    recipients TEXT,  -- JSON array
    body_text TEXT,
    body_html TEXT,
    received_at DATETIME,
    labels TEXT,      -- JSON array
    has_attachments BOOLEAN DEFAULT 0,
    raw_headers TEXT  -- JSON for full header preservation
);

-- FTS5 virtual table for search
CREATE VIRTUAL TABLE messages_fts USING fts5(
    subject, body_text, sender, recipients,
    content='messages',
    content_rowid='rowid'
);
```

The FTS5 index covers subject, body, sender, and recipients. Searching for "deployment incident from:ops-team" returns results in milliseconds, even with thousands of stored messages. Triggers keep the FTS index in sync with the main table — insert a message, the FTS index updates automatically.

Why SQLite instead of a proper email server? Because intent-mail isn't an email server. It's a local-first email management layer that syncs from Gmail and Outlook, stores messages locally for fast search and agent access, and sends through the provider APIs. The user's email stays in Gmail/Outlook. Intent-mail is a working copy.

## Gmail OAuth Connector with Delta Sync

The Gmail connector uses OAuth 2.0 with offline refresh tokens. First-time auth redirects to Google's consent screen. After consent, the refresh token is stored locally (encrypted, same pattern as Lumera-Emanuel) and used for all subsequent API calls.

Delta sync is the critical optimization. Instead of pulling the full mailbox on every sync, the connector tracks a sync checkpoint — Gmail's `historyId`. Each sync call asks: "what changed since historyId X?" Gmail returns only the messages added, deleted, or label-changed since that checkpoint.

```python
def delta_sync(self, since_history_id: int) -> SyncResult:
    changes = self.gmail.users().history().list(
        userId='me',
        startHistoryId=since_history_id,
        historyTypes=['messageAdded', 'messageDeleted', 'labelAdded']
    ).execute()

    added = []
    for record in changes.get('history', []):
        for msg in record.get('messagesAdded', []):
            full = self._fetch_full_message(msg['message']['id'])
            added.append(full)

    return SyncResult(
        added=added,
        deleted=[...],
        new_history_id=changes['historyId']
    )
```

The first sync pulls recent messages (configurable depth, default 30 days). Every subsequent sync is incremental. A mailbox with 50,000 messages takes minutes for the initial sync and seconds for updates.

Gmail send supports threading and multipart messages. Reply to a thread and the connector sets the correct `In-Reply-To` and `References` headers so Gmail groups the reply properly. Multipart messages include both plaintext and HTML bodies — some recipients see HTML, some see text, all see something readable.

## Outlook Connector via MS Graph

The Outlook connector mirrors the Gmail connector's interface but uses Microsoft Graph API underneath. OAuth 2.0 with MSAL authentication. Delta sync via Graph's `/messages/delta` endpoint, which works conceptually like Gmail's history API but returns a `@odata.deltaLink` URL instead of a numeric ID.

The challenge with Graph API: pagination. Gmail returns delta results in a single response up to a size limit. Graph API always paginates, and the pagination token expires after 30 minutes. The connector handles this with eager pagination — on each sync, it follows `@odata.nextLink` tokens until exhausted, collecting all changes before processing any of them.

Attachment support required different handling per provider. Gmail returns attachments as base64 in the message payload (small attachments) or requires a separate API call (large attachments). Graph API always returns attachment metadata separately, with a download URL that requires auth headers. The unified attachment interface hides these differences:

```python
class Attachment:
    filename: str
    content_type: str
    size_bytes: int

    async def download(self) -> bytes:
        # Provider-specific download logic
        ...
```

## MCP Tools for Agent Access

Six MCP tools expose the email platform to AI agents:

| Tool | Purpose |
|------|---------|
| `search_email` | FTS5 search across all synced messages |
| `get_thread` | Retrieve a full email thread with all messages |
| `send_email` | Compose and send via Gmail or Outlook |
| `reply_to_thread` | Reply with proper threading headers |
| `list_labels` | Get available labels/folders per provider |
| `apply_label` | Label/move messages |

The tools are provider-agnostic. An agent calls `search_email(query="invoice Q4")` and gets results from both Gmail and Outlook accounts. The agent doesn't need to know which provider a message came from — the tools handle routing.

## The Rules Engine

The automation rules engine was the most architecturally interesting piece. Rules are defined as code — not a GUI, not a YAML config, but actual Python expressions with a constrained grammar.

```python
# Rule definition
rule = Rule(
    name="auto-label-deploys",
    condition='subject contains "deploy" AND sender in ops_team',
    actions=[
        LabelAction(label="ops/deployments"),
        ArchiveAction(),
    ],
    enabled=True,
)
```

The parser validates rule conditions against a whitelist of operators and field names. You can't write arbitrary Python — the condition language supports `contains`, `matches` (regex), `in` (list membership), `AND`, `OR`, `NOT`, and field access for `subject`, `sender`, `recipients`, `body`, `labels`, and `has_attachments`.

The validator checks rules at definition time: does the field exist? Is the operator valid for this field type? Does the referenced list (like `ops_team`) exist in the contacts database? A malformed rule fails validation before it ever touches a message.

### Dry-Run Mode

Every rule supports dry-run execution. Run the rules engine against your inbox in dry-run mode and it reports what would happen without making any changes:

```
[DRY-RUN] Rule "auto-label-deploys" matched 14 messages:
  - "Deploy v2.3.1 to production" from ops@company.com → label: ops/deployments, archive
  - "Deploy rollback requested" from incidents@company.com → label: ops/deployments, archive
  ...
```

This matters because email rules with bugs have real consequences. An overly broad rule that archives everything from a domain could hide important messages. Dry-run lets you verify before committing.

## Gemini Review Feedback

The Gemini PR reviewer flagged two issues in the rules engine. First: the condition parser didn't handle nested parentheses, so `(A AND B) OR C` parsed correctly but `(A AND (B OR C))` threw a syntax error. The fix was a recursive descent parser replacing the original regex-based approach.

Second: the `send_email` tool accepted raw HTML body content without sanitization. A malicious or confused agent could inject tracking pixels or scripts. The fix added an HTML sanitizer that strips `<script>`, `<img>` with external sources, and `<style>` blocks before sending.

Both catches were legitimate. The Gemini reviewer earned its keep on this PR.

---

35 commits, two email providers, full-text search, threaded conversations, a rules engine with dry-run, and MCP tools for agent integration. Intent-mail went from nothing to a real tool in a single day.

### Related Posts

- [Perception Agent System: Zero to MCP Server and Dashboard in One Day](/posts/perception-agent-system-zero-to-mcp-dashboard/)
- [Building Production CI/CD: Documentation to Deployment](/posts/building-production-ci-cd-documentation-to-deployment/)
- [Lumera-Emanuel Launch and git-with-intent Open-Source Release](/posts/lumera-emanuel-launch-gwi-open-source-release/)
