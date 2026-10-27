# Optional Discord activity observations

Status: implemented source hooks, disabled by default; production installation and
activation belong to the Intent OS automation rollout. Tracked by
`bd_000-projects-txsk.20.1` under the Discord automation epic. This is an activity
projection, not the article feed, a mail receipt archive or a new publication gate.

The four cron scripts keep their existing email, Buzz, ledger and exit behavior.
They call `blog_activity_emit` only at the following boundaries:

| Producer | Observation | Required evidence and retry identity |
| --- | --- | --- |
| `blog-daily` | `published` | Accepted producer, parent's pipeline lock, non-canary lander result 0, 15 or 21. These results verify public liveness; 15 still leaves the original degraded alert active. Identity is the target date and phase. |
| `blog-daily` | `pending` / `failed` | The real land attempt returns 13 / another non-publication result. These describe an observed attempt, not a claim that every failure in the entire cron was captured. |
| `blog-daily` | `nothing_due` | Existing public article, delivery/index reconciliation, completed no-op and healthy prior recovery. No canary event. |
| `blog-packet` | `sent` | Real mail command succeeds and the existing ledger records `sent`. One observation per public post slug; HOLD, dry-run, mail failure and failed receipt update are excluded. |
| `blog-packet` | `nothing_due` | Real sweep, no selected packets, parseable array ledger with yesterday present and every entry explicitly marked sent. A failed gap-alert email cannot authorize this observation. |
| `blog-rollup` | `sent` | Validated nontrivial report and successful real mail command. Identity is the rollup's date. |
| `blog-recommendation` | `ready` | Existing deterministic gate and push succeed, then `gh pr create` succeeds with a valid PR URL for this repository. Identity is the public PR number. This does not mean merged. |
| `blog-recommendation` | `nothing_due` | Successful eligible-queue lookup returns empty outside dry-run. Identity is the observation date. |

Mail success means the existing mailer's successful return, not proof of inbox
reading or a recipient's subsequent action. No recipients, article titles, URLs,
bead identifiers, logs or private body text enter the activity outbox.

## Runtime contract

Leave `INTENT_ACTIVITY_ENABLED` unset or `0` until the shared rollout is reviewed.
To activate an installed producer, its environment requires:

- `INTENT_ACTIVITY_ENABLED=1`.
- `INTENT_ACTIVITY_SPOOL_DIR`: an absolute owner-private directory, mode `0700`.
- The appropriate `<producer>-event.py` beside the reviewed Intent OS
  `activity_spool.py`, normally in `$HOME/bin/lib/discord-activity/`.

The four fixed wrappers are maintained in `scripts/blog/`. The shared module is
maintained in Intent OS, `ops/automation/discord-activity/`, with deduplicating
entrypoint support introduced by commit `64bdf201f89c1bfbe58d5b911835fb46efd9872b`.
Do not install an older module that lacks `main(..., deduplicate=True)`.
`INTENT_ACTIVITY_BRIDGE` is a trusted absolute executable-script path override for
fixtures or an explicitly configured single producer. Do not assign one producer's
wrapper as a global override for all four jobs.

The bridge receives only `--result <fixed-enum> --observation-key <sha256>`.
The domain-separated hash combines fixed producer, phase and the bounded public
identity above. The shared spool allocates the UUID transactionally and retains the
identity after acknowledged intake. Repeated observations keep one delivery; a
later phase (for example pending then published) is a separate observation.
Deleting or replacing the spool destroys that retry history.

There is no Discord credential or network call here. The separate Intent OS
shipper owns intake and member-safe aggregation. Every bridge invocation is bounded
by five seconds and suppresses bridge output. Failure emits one generic warning and
never reverses publication, changes a receipt or suppresses the original alert.
A failure before durable capture can lose the optional activity observation: inspect
the original producer receipt and repair capture through the reviewed operator path;
never resend mail or republish an article merely to regenerate a Discord event.
These hooks do not claim transactional delivery across the mailer and the outbox.

## Verification and rollback

`tests/test_blog_activity.py` executes the actual relevant shell branches with
synthetic mail, ledger, GitHub and report fixtures. Full cron bootstrap is excluded
because it reads installed credentials and performs unrelated publishing work.
The ordinary suite checks truth boundaries, quiet-queue validation, privacy,
fixed producer wrappers, default-off behavior and failure isolation.

The cross-repository outbox test explicitly requires the reviewed dependency:

```sh
INTENT_ACTIVITY_SHARED_SOURCE=/absolute/reviewed/activity_spool.py \
  python3 -m pytest tests/test_blog_activity.py -q
```

It stages that module alongside the real wrappers in a private temporary directory,
checks four producer UUIDs, repeat observations, and replay after acknowledged rows
are removed while tombstones remain. No email, publish or live Discord call occurs.
Without this environment variable the integration test is explicitly skipped; unit
checks still run. Run `scripts/blog/lint-all.sh` before committing pipeline changes.

Rollback is `INTENT_ACTIVITY_ENABLED=0`; keep the spool for audited recovery. Legacy
notification paths and the production publisher continue to operate independently.
