#!/usr/bin/env bash
# rebuild-methodology-index.sh — Rebuild the SQLite analytics index from JSONL source-of-truth.
#
# JSONL files are append-only sources of truth. This script derives a queryable
# SQLite index for analytics, feedback correlation, and calibration reports.
#
# Safe to re-run — drops and recreates all tables.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
METH_DIR="${SKILL_DIR}/methodology"
DB="${METH_DIR}/index.db"
SCHEMA="${METH_DIR}/rebuild-index.sql"

if [[ ! -f "$SCHEMA" ]]; then
  echo "ERROR: schema file not found at $SCHEMA" >&2
  exit 1
fi

echo "Rebuilding methodology index at $DB"

# Step 1: schema
rm -f "$DB"
sqlite3 "$DB" < "$SCHEMA"

# Step 2: import JSONL via Python
python3 - "$METH_DIR" "$DB" <<'PYEOF'
import json, sqlite3, sys, os

meth_dir, db_path = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON;")

# Import decisions.jsonl
decisions_path = os.path.join(meth_dir, "decisions.jsonl")
dec_count = 0
if os.path.exists(decisions_path):
    with open(decisions_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            # Skip audit-addendum records (enriched agent_audit entries appended
            # after the primary decision). They share (date, slug) with the primary
            # record but carry no classification fields.
            if rec.get("audit_addendum") or "tier" not in rec:
                continue
            dims = rec.get("dimensions", {})
            sigs = rec.get("source_signals", {})
            conn.execute("""
                INSERT OR REPLACE INTO decisions
                    (date, slug, tier, tier_name, confidence,
                     dim_novelty, dim_arc, dim_nar, dim_tch, dim_scp, dim_rpr,
                     reasoning, alternatives_considered, thesis_candidate,
                     rhetorical_structure, sig_git, sig_prs, sig_session,
                     sig_beads, sig_email, cadence_type, anti_inflation_flags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rec["date"], rec["slug"], rec["tier"], rec["tier_name"], rec["confidence"],
                dims.get("novelty", 0), dims.get("arc", 0), dims.get("nar", 0),
                dims.get("tch", 0), dims.get("scp", 0), dims.get("rpr", 0),
                rec.get("reasoning", ""), rec.get("alternatives_considered", ""),
                rec.get("thesis_candidate", ""), rec.get("rhetorical_structure", ""),
                sigs.get("git", "absent"), sigs.get("prs", "absent"),
                sigs.get("session", "absent"), sigs.get("beads", "absent"),
                sigs.get("email", "absent"),
                rec.get("cadence_type", "daily"),
                json.dumps(rec.get("anti_inflation_flags", []))
            ))
            dec_count += 1
    conn.commit()

# Import feedback.jsonl (optional)
feedback_path = os.path.join(meth_dir, "feedback.jsonl")
fb_count = 0
if os.path.exists(feedback_path):
    with open(feedback_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            try:
                conn.execute("""
                    INSERT OR REPLACE INTO feedback
                        (slug, feedback_date, was_correct, actual_tier, notes)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    rec["slug"], rec.get("feedback_date", ""),
                    int(rec.get("was_correct", 0)),
                    rec.get("actual_tier"), rec.get("notes", "")
                ))
                fb_count += 1
            except sqlite3.Error:
                pass
    conn.commit()

# Import patterns.jsonl (optional)
patterns_path = os.path.join(meth_dir, "patterns.jsonl")
pat_count = 0
if os.path.exists(patterns_path):
    with open(patterns_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            try:
                conn.execute("""
                    INSERT OR REPLACE INTO patterns
                        (pattern_name, description, first_seen, last_seen, occurrences)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    rec.get("pattern_name", ""), rec.get("description", ""),
                    rec.get("first_seen", ""), rec.get("last_seen", ""),
                    rec.get("occurrences", 0)
                ))
                pat_count += 1
            except sqlite3.Error:
                pass
    conn.commit()

conn.close()

print(f"Imported: decisions={dec_count}, feedback={fb_count}, patterns={pat_count}")
PYEOF

# Step 3: report summary
echo ""
echo "=== Tier distribution ==="
sqlite3 -column -header "$DB" "
  SELECT tier, tier_name, COUNT(*) as posts,
         ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM decisions), 1) as pct
  FROM decisions
  GROUP BY tier, tier_name
  ORDER BY tier;"

echo ""
echo "=== Recent decisions (last 10) ==="
sqlite3 -column -header "$DB" "
  SELECT date, tier, substr(slug, 1, 50) as slug, ROUND(confidence, 2) as conf
  FROM decisions
  ORDER BY date DESC, slug
  LIMIT 10;"

echo ""
echo "Index rebuild complete: $DB"
