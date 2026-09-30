+++
title = 'Require the Phone at Intake, Not When Staff Call Back'
slug = 'require-the-phone-at-intake'
date = 2026-09-29T08:00:00-06:00
draft = false
tags = ["intake-hardening", "validation", "fail-closed", "now-lms", "devops"]
categories = ["DevOps"]
description = "now-lms /request-access added a required, server-validated phone field at intake (PR #123), stored as a labeled line of the existing body."
tldr = "Add the field staff will need at the moment staff will need it. Validate on the server (an 8-digit floor rejects a local number with no area code; 15 is the E.164 max), store the value as a labeled line of the existing contact-message body, and let the watcher that already forwards that body carry the new field for free. /request-access at now-lms shipped in PR #123 (5/5 CI green) and went live the same day."
+++

The /request-access form on now-lms shipped a contact message with no phone number. I noticed it the day an applicant asked staff to call them back. Staff got the email, opened it, looked for a number, found nothing. The bug was not in the intake. The bug was the intake's design. The form asked what the application asked. It did not ask what staff would need five minutes after reading the answer.

PR #123 fixes that. I added a required Phone field, validated server-side, stored as a labeled line of the existing contact-message body. The watcher that already forwards that body carries the new field for free. The change is small. The lesson is bigger.

## The change

The PR is #123, commit `55160f86`, deployed 2026-09-29 17:51 CDT. The form gains one labeled field, rendered as `type=tel` with `autocomplete=tel` and `inputmode=tel`, marked `required=True`. The server-side form gains one `StringField`, validated by `DataRequired()` and `Length(max=32)`, plus a regex and a digit count:

```python
_PHONE_CHARS = re.compile(r"^\+?[0-9 ().\-]+$")
PHONE_MIN_DIGITS = 8
PHONE_MAX_DIGITS = 15
```

The validator normalizes the string (strip whitespace) then counts digits. Eight is the floor. Fifteen is the ceiling. The regex accepts a leading plus, digits, spaces, dots, parentheses, and hyphens. Anything else is rejected.

The template renders the labeled block:

```html
<div class="field">
  <label for="phone">Phone</label>
  <input id="phone" name="phone" type="tel" autocomplete="tel"
         inputmode="tel" required maxlength="32" />
</div>
```

Storage is the fork's no-migration design. The phone goes in as the first labeled line of the contact-message body:

```
Phone: +1 555 123 4567

(request body)
```

The waiting list is native `contact_messages` rows. No new column. No alembic step. No DB migration on a fork where the schema is held still on purpose.

A follow-up commit in the same PR addressed the MiniMax review. The placeholder is a locale-specific example format, so it now goes through gettext like its sibling placeholders. The accepted-formats test gains `03-1234-5678` (Japan, 10 digits).

## Why the 8-digit floor matters

A 7-digit local number has no area code. Staff cannot call it back from a different region. The eight-digit floor rejects the format that looks plausible and is not actionable.

Fifteen is the E.164 maximum. The ITU publishes the standard. The max length of a fully qualified international phone number is 15 digits. Above 15, no carrier routes it.

The floor and the ceiling are not magic numbers. They are the operating range of a phone number staff can actually use.

## Why the labeled-body storage

The fork runs on a no-migration policy. Schema changes cost more than the original author wanted to pay for a fork that mostly tracks upstream. Adding a column to `contact_messages` means a migration, a watcher change, and a deploy dance.

Storing the phone in the body is free. The watcher at `intent-os/ops/lms/lms-intake-watch.sh` reads the full body and forwards it to the owner inbox and the leads channel. The phone rides on the same forward. No watcher change. The new field traveled the path the existing reader already walked.

## Also shipped

Two other now-lms theme changes shipped the same day. PR #124 added Heather Johnson as Legal Counsel. PR #125 finished the network navigation and aligned Heather's team profile. startaitools.com itself shipped zero code or content commits on 2026-09-29. The six commits were all auto-generated release machinery closing out the 2026-09-28 team-page-ordering post (v1.21.15 and v1.21.16, two auto-bumps because the post and its asset landed as two separate commits). intent-eval-platform merged htjt.25, an eval headroom and saturation signal (#321), and htjt.26, retiring the Groq and NVIDIA defaults (#323). Provider-default discipline.

## Use this

What I take from this: add the field staff will need at the moment staff will need it. Validate on the server (the floor rejects what staff cannot use; the ceiling matches what carriers route). Store it where the existing watcher already reads. Let the forwarding mechanism carry the new field for free.

## Related posts

- [disclosure-gate-reject-pii-at-source](/posts/disclosure-gate-reject-pii-at-source/) on the same intake-time validation pattern, applied to PII (2026-06-19)
- [seven-merges-one-audit-zero-leaks](/posts/seven-merges-one-audit-zero-leaks/) on fail-closed discipline at the Hustle admin intake (2026-09-18)
- [team-page-ordering-is-a-release-decision](/posts/team-page-ordering-is-a-release-decision/) on release-mechanics discipline (2026-09-28)