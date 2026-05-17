# Step 5: Social Email Bundle

Generate platform-specific social posts and email the bundle to Jeremy for manual posting.

## 5a. Generate X Thread (3 tweets)

Write a 3-tweet thread using personal/technical voice:
- Tweet 1: TL;DR + hook (what was built/solved)
- Tweet 2: Key technical insight or result
- Tweet 3: Link to `https://startaitools.com/posts/SLUG/` + hashtags

Style: conversational, authentic, no AI slop. Follow the `/lnx` X thread patterns.

Save to: `/home/jeremy/000-projects/blog/x-threads/YYYY-MM-DD-SLUG-backfill-x3.txt`

## 5b. Generate LinkedIn Post (1200-1500 chars)

Write a professional/company voice post (Intent Solutions brand):
- Hook -> context -> technical highlights -> business impact -> subtle CTA
- 3-5 professional hashtags

Save to: `/home/jeremy/000-projects/blog/linkedin-posts/YYYY-MM-DD-SLUG.txt`

## 5c. Combine into Social Bundle

Merge X thread + LinkedIn post + Substack draft into one file:

```
=== X THREAD ===
[X thread content]

=== LINKEDIN ===
[LinkedIn post content]

=== SUBSTACK ===
[Substack draft content or "SKIP: $SUBSTACK_OUTPUT_DIR not set"]
```

Save to: `/tmp/social-bundle-SLUG.txt`

## 5d. Email the Bundle

```bash
node /home/jeremy/.claude/skills/email/scripts/send-email.cjs \
  --to jeremy@intentsolutions.io \
  --subject "Social Bundle: SLUG" \
  --body "$(cat /tmp/social-bundle-SLUG.txt)"
```

Sends via Gmail SMTP (requires `GMAIL_USER_EMAIL` + `GMAIL_APP_PASSWORD` in env). If send fails, print the bundle path for manual copy.
