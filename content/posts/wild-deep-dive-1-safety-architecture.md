+++
title = 'Deep Dive Part 1: The Safety Architecture of Letting AI Agents Touch Your Production Rails Database'
slug = 'wild-deep-dive-1-safety-architecture'
date = 2026-03-26T13:00:00-05:00
draft = false
tags = ["wild-ecosystem", "ruby", "rails", "security", "mcp", "claude-code", "ai-agents"]
categories = ["Wild Ecosystem Deep Dive"]
description = "How the wild ecosystem makes it structurally impossible for AI agents to cause damage when accessing production Rails databases. Defense in depth, adversarial testing, and hard safety ceilings."
toc = true
+++

When an AI agent needs to debug a production issue, it faces a dilemma: either it has no access to live data (useless), or it gets a Rails console (dangerous). There is no safe middle ground in standard tooling.

The [wild ecosystem](/wild-ecosystem/) solves this with a systematic approach to safe production introspection and gated mutations. This is not about trusting the AI. It is about building infrastructure that makes it impossible to cause damage, regardless of what code the agent executes or parameters it provides.

This article is Part 1 of a four-part deep dive into the wild ecosystem's architecture. We will examine the specific mechanisms that allow an AI agent to query a production Rails database without write access, without raw Ruby execution, and without data leakage -- and how mutations are gated through a two-phase confirmation protocol that logs every action.

The guardrails are not advisory. They are structural.

---

## The Problem: Why Standard Solutions Fail

When production debugging is needed, a Rails engineer has three options:

1. **Rails console access**: The agent can execute arbitrary Ruby. One typo -- or one adversarial instruction in a prompt -- and the database mutates. The agent can exfiltrate all data. There are no limits.

2. **No access**: The agent gets no live data and cannot debug. It must work from logs and secondhand reports.

3. **Read-only database replica with application-level guards**: The agent can query, but only what is explicitly allowed. Mutations are impossible. Access patterns are audited. This requires deliberate architecture.

Most teams choose option 1 because option 2 is unhelpful and option 3 requires substantial engineering effort. The wild ecosystem provides that engineering as two composable repositories:

- **[wild-rails-safe-introspection-mcp](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp)**: Safe, read-only inspection of Rails models and records. No write paths. No arbitrary code execution.
- **[wild-admin-tools-mcp](https://github.com/jeremylongshore/wild-admin-tools-mcp)**: Gated administrative mutations (retrying jobs, invalidating caches, toggling flags) with two-phase confirmation and audit logging.

Together, they form the foundation for AI agents to interact with production systems safely.

---

## Defense in Depth: Four Enforcement Layers

Safe production access is not achieved through a single mechanism. It is achieved through four independent layers, each capable of blocking an attack. An attacker must bypass all four.

### Layer 1: Database Credentials and Routing

The system connects to the database as a read-only user whenever possible. If infrastructure supports it, all queries are routed to a read replica, isolating introspection traffic from the primary write database. If neither option is available, the fallback is documented in the audit trail so operators know the structural guarantee is degraded.

This layer is your infrastructure guarantee. But it is not sufficient alone. The system does not trust it.

### Layer 2: Application-Level Write Prevention

The application layer explicitly refuses any method that could trigger a write. This happens before the database layer, regardless of what credentials are in use.

```ruby
module WritePrevention
  FORBIDDEN_METHODS = %i[
    save save!
    create create!
    update update!
    update_all
    destroy destroy!
    destroy_all
    delete delete_all
    insert insert_all
    upsert upsert_all
    touch
    increment! decrement!
    toggle!
  ].freeze

  WRITE_SQL_PATTERN = /\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE)\b/i

  def self.assert_not_write_method!(name)
    return unless write_method?(name)
    raise WriteAttemptError, "Write method '#{name}' is forbidden. This system is read-only."
  end

  def self.assert_sql_read_only!(sql)
    return unless sql.is_a?(String)
    stripped = sql.gsub(/'[^']*'/, "''").gsub(/"[^"]*"/, '""')
    return unless stripped.match?(WRITE_SQL_PATTERN)
    raise WriteAttemptError, 'Write SQL detected. This system is read-only.'
  end
end
```

This module is called on every ActiveRecord operation and raw SQL invocation. There is no code path that bypasses it. The forbidden methods list is explicit and finite -- not a blacklist that future Rails versions might render incomplete.

### Layer 3: Query Guard and Column Filtering

Even if a query gets to the database, it is constrained by the query guard. The guard enforces three things:

1. **Model access control**: Models are not accessible by default. Only models on the allowlist can be queried.
2. **Column access control**: Even on allowed models, sensitive columns are stripped from results.
3. **Resource limits**: Row counts and query timeouts are enforced.

```ruby
module QueryGuard
  DENIAL_RESPONSE = {
    status: :denied,
    reason: :model_not_allowed,
    message: 'The requested model is not on the access allowlist.'
  }.freeze

  def self.find_by_id(model_name, id, request_context:)
    recorder_opts = { tool_name: 'lookup_record_by_id', model_name: model_name,
                      parameters: { id: id }, request_context: request_context }
    Audit::Recorder.record(**recorder_opts) do
      next AUTH_DENIAL unless request_context.authenticated?

      accessible = ColumnResolver.accessible_columns(model_name)
      next DENIAL_RESPONSE unless accessible

      result = Adapter::RecordLookup.find_by_id(model_name, id)
      next result unless result[:status] == :ok

      result.merge(
        record: ResultFilter.filter_record(result[:record], accessible)
      )
    end
  end
end
```

Notice the flow: authentication check, model access check, query execution, column filtering, and audit logging. All within a single method. There is no skip path.

### Layer 4: Audit Trail

Every invocation -- success, denial, timeout, error -- produces a structured, append-only audit record. The record includes caller identity, action, parameters, outcome, duration, and resources affected.

An attacker cannot hide their actions. Exfiltration of data one record at a time is visible in the audit trail. Brute-force enumeration of record IDs is visible. Configuration tampering requires filesystem access, which is orthogonal to application security.

The audit trail is JSONL, stored in a file that cannot be modified through the application. It is the record of what happened, not what the application claims happened.

---

## The Allowlist/Denylist Model: Explicit Access Control

The safety model inverts the typical Rails convention. By default, nothing is accessible. Models are not automatically exposed to introspection. You must explicitly add them to the allowlist.

The allowlist is defined in YAML at server startup. Changes require restarting the server. This is intentional: configuration errors cannot accidentally expand access without an operator taking action.

```yaml
allowed_models:
  - name: Account
    columns: all_except_blocked
  - name: User
    columns: [id, email, name, created_at, updated_at, status]
  - name: FeatureFlag
    columns: all
```

The denylist operates on top of the allowlist. A model can be on the allowlist but have specific columns blocked.

```yaml
blocked_resources:
  models:
    - CreditCard
    - ApiKey
    - SessionToken
  columns:
    - model: User
      columns: [password_digest, encrypted_password, otp_secret]
    - model: Account
      columns: [stripe_customer_id, billing_token, tax_id]
    - model: "*"
      columns: [ssn, credit_card_number, social_security_number]
```

When a blocked column appears in a record, it is silently stripped from the response. The response does not indicate that columns were removed. This prevents information leakage about what sensitive data exists in your schema.

When a model is not on the allowlist, the denial response is identical to the denial response for a non-existent model:

```json
{
  "status": "denied",
  "reason": "model_not_allowed",
  "message": "The requested model is not on the access allowlist."
}
```

An attacker cannot distinguish between a model that does not exist and a model that exists but is blocked. Both produce the same response.

---

## Two-Phase Confirmation for Mutations

The introspection layer is strictly read-only. But production debugging often requires mutations: retrying failed jobs, invalidating caches, toggling feature flags. These operations must be safe and reversible.

The mutation layer ([wild-admin-tools-mcp](https://github.com/jeremylongshore/wild-admin-tools-mcp)) implements a two-phase confirmation protocol. No mutation executes without explicit confirmation from the caller.

The flow is:

1. **Caller invokes an action** with parameters (e.g., "retry the failed mailer jobs from the past hour").
2. **Server generates a dry-run preview** showing exactly what would change: affected resources, count, blast radius.
3. **Server issues a single-use confirmation nonce** tied to the action, parameters, and caller identity.
4. **Caller confirms by re-invoking with the nonce**.
5. **Server validates the nonce** and executes the mutation, or rejects if nonce is expired, already used, or mismatched.

```ruby
class NonceManager
  def generate(action_name, params, caller_id, ttl_seconds: 30)
    ttl = ttl_seconds.clamp(MIN_TTL, MAX_TTL)
    nonce = "#{NONCE_PREFIX}#{SecureRandom.hex(16)}"
    entry = NonceEntry.new(
      nonce: nonce,
      binding_hash: compute_binding_hash(action_name, params, caller_id),
      action_name: action_name,
      caller_id: caller_id,
      expires_at: Time.now + ttl
    )
    @store.store(entry)
    nonce
  end

  private

  def compute_binding_hash(action_name, params, caller_id)
    sorted_params_json = params.sort.to_h.to_json
    Digest::SHA256.hexdigest("#{action_name}|#{sorted_params_json}|#{caller_id}")
  end
end
```

The binding hash includes the sorted parameters and caller identity. If any of these change, the hash changes. If the nonce is replayed with different parameters, it fails. All failure reasons are conflated into a single, opaque response: "nonce_invalid". This prevents probing attacks.

---

## Adversarial Testing: Proving the Guarantees

The safety guarantees are verified through adversarial test suites. Claude Code, the AI that will eventually use these tools, also wrote the tests that try to break them.

### Prompt Injection Through Parameters

Model names, filter values, and record IDs are treated as opaque data, never as code.

```ruby
it 'denies model_name payload "Account.destroy_all"' do
  response = tool_schema.call(model_name: 'Account.destroy_all', server_context: ctx)
  parsed = parse_response(response)
  expect(response.error?).to be(true)
  expect(parsed[:status]).to eq('denied')
end

it 'treats id containing Ruby code as opaque string' do
  response = tool_lookup.call(
    model_name: 'Account', id: 'system("rm -rf /")', server_context: ctx
  )
  parsed = parse_response(response)
  expect(parsed[:status]).to eq('not_found')
end
```

Model names are always resolved through allowlist hash lookup. There is no `constantize`, no `const_get`, no dynamic class resolution. The allowlist is a hash. Lookup succeeds or fails. That is all.

### SQL Injection Through Filter Values

Filter values are never interpolated into SQL. They are always passed as parameterized bindings:

```ruby
it 'treats filter value containing SQL injection as opaque string' do
  response = tool_filter.call(
    model_name: 'Account', field: 'name',
    value: "'; DROP TABLE accounts; --",
    server_context: ctx
  )
  parsed = parse_response(response)
  expect(parsed[:status]).to eq('ok')
  expect(parsed[:records].length).to eq(0)
end
```

The filter value is a literal string. The query matches zero records. The table is unchanged.

### Confirmation Bypass

Nonce validation is mandatory. A fabricated, expired, or reused nonce is rejected with an opaque failure:

```ruby
it 'denies a fabricated nonce' do
  response = tools::ManageBackgroundJobs.call(
    action: 'retry_job', job_id: 'job-1',
    nonce: 'fake_nonce_123', server_context: server_context
  )
  body = response.structured_content
  expect(body[:status]).to eq('denied')
  expect(body[:reason]).to eq('nonce_invalid')
  expect(job_adapter.write_methods_called).to be_empty
end
```

Every test explicitly verifies that no write methods were called. The mutation was not executed. The database snapshot before and after the request is identical.

---

## Hard Ceilings vs Soft Limits

The system enforces both soft limits (configurable defaults) and hard ceilings (not configurable).

| Limit | Default | Hard Ceiling |
|-------|---------|-------------|
| Row cap | 50 | 1,000 |
| Query timeout | 5 seconds | 30 seconds |
| Nonce TTL | 30 seconds | 10-120 seconds |

A soft limit can be configured higher, but a hard ceiling cannot. If configuration tries to set a row cap to 5,000, the system enforces 1,000 instead. If configuration tries to set a query timeout to 60 seconds, the system enforces 30 seconds instead.

Why? Because configuration files can be edited by humans. Configuration errors are easy. A hard ceiling ensures that a configuration mistake cannot silently expand the scope of accessible data or allow runaway queries.

If the hard ceiling is exceeded, the query is cancelled and an error is returned. It is not truncated silently. The caller knows something went wrong. They cannot assume they received complete results when they did not.

---

## Claude Code's Role: The AI That Builds Its Own Guardrails

The wild ecosystem is unusual in that the same AI system that will use these tools also built the guardrails that constrain its access.

Claude Code made the architectural decisions that define the safety model:

- **Allowlist hash instead of constantize**: Rather than trusting Rails to resolve class names dynamically, the system uses an explicit hash lookup. More cumbersome but absolutely safe from code injection.
- **Parameterized queries everywhere**: Every query is built with bindings, never string interpolation. Not a convenience -- a hard requirement enforced by the adapter layer.
- **Two-phase confirmation for mutations**: Rather than allowing a single request to trigger an action, the system requires a dry-run followed by a confirmation with a nonce.
- **Opaque failure reasons**: When nonce validation fails, the client receives a single "nonce_invalid" response regardless of whether the nonce is expired, already used, or mismatched.

Claude Code also wrote the adversarial test suite. The tests that prove these guarantees exist -- that attempt to inject code, bypass confirmation, and exfiltrate data -- came from the same source as the implementation.

The guarantees are not about trusting Claude Code. They are about building infrastructure such that the question of trust becomes irrelevant. The agent cannot write, cannot execute arbitrary code, cannot exceed resource limits, and every action is audited. Whether the agent is helpful or adversarial -- it does not matter. The infrastructure guarantees hold.

---

## What Comes Next

This is Part 1 of the [Wild Ecosystem Deep Dive](/wild-ecosystem/) series.

- **Part 2**: [CLAUDE.md -- The Human-AI Collaboration Pattern](/posts/wild-deep-dive-2-claude-md/) -- How per-repo contracts between human and AI prevent scope creep and enforce safety
- **Part 3**: [The Observability Loop](/posts/wild-deep-dive-3-observability/) -- How the telemetry-transcript-gap mining pipeline teaches AI tools to improve themselves
- **Part 4**: [Claude Code as Tech Lead](/posts/wild-deep-dive-4-tech-lead/) -- What it means when the AI makes the architectural decisions

The safety is not in the agent. It is in the infrastructure.

---

*Part of the [Wild Ecosystem](/wild-ecosystem/) -- 10 Ruby gems for governed AI agent operations in production Rails. Built with [Claude Code](https://claude.ai/code).*
