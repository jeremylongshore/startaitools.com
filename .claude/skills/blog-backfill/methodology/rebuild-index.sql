-- rebuild-index.sql
-- Derives a SQLite analytics index from the JSONL source-of-truth files.
-- Run: sqlite3 methodology/index.db < methodology/rebuild-index.sql
-- Safe to re-run — drops and recreates all tables.

-- ============================================================
-- Schema
-- ============================================================

DROP TABLE IF EXISTS decisions;
CREATE TABLE decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,                    -- YYYY-MM-DD
    slug TEXT NOT NULL UNIQUE,
    tier INTEGER NOT NULL CHECK (tier BETWEEN 1 AND 4),
    tier_name TEXT NOT NULL,
    confidence REAL NOT NULL CHECK (confidence BETWEEN 0 AND 1),

    -- Six scoring dimensions (0-5)
    dim_novelty INTEGER CHECK (dim_novelty BETWEEN 0 AND 5),
    dim_arc INTEGER CHECK (dim_arc BETWEEN 0 AND 5),
    dim_nar INTEGER CHECK (dim_nar BETWEEN 0 AND 5),
    dim_tch INTEGER CHECK (dim_tch BETWEEN 0 AND 5),
    dim_scp INTEGER CHECK (dim_scp BETWEEN 0 AND 5),
    dim_rpr INTEGER CHECK (dim_rpr BETWEEN 0 AND 5),

    reasoning TEXT,
    alternatives_considered TEXT,
    thesis_candidate TEXT,
    rhetorical_structure TEXT,

    -- Source signal strengths
    sig_git TEXT DEFAULT 'absent',
    sig_prs TEXT DEFAULT 'absent',
    sig_session TEXT DEFAULT 'absent',
    sig_beads TEXT DEFAULT 'absent',
    sig_email TEXT DEFAULT 'absent',

    cadence_type TEXT DEFAULT 'daily',     -- daily, weekly, monthly
    anti_inflation_flags TEXT,             -- JSON array as text
    created_at TEXT DEFAULT (datetime('now'))
);

DROP TABLE IF EXISTS feedback;
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
    date_assessed TEXT NOT NULL,           -- When the feedback was recorded
    original_tier INTEGER NOT NULL,
    correct_tier INTEGER,                  -- NULL if original was correct
    was_correct INTEGER NOT NULL DEFAULT 1,
    reasoning TEXT,
    year_from_now_useful INTEGER,          -- 1/0/NULL
    engagement_data TEXT,                  -- JSON: views, shares, comments
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (slug) REFERENCES decisions(slug)
);

DROP TABLE IF EXISTS patterns;
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id TEXT NOT NULL UNIQUE,       -- e.g., "anti-inflate-003"
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    direction TEXT CHECK (direction IN ('upgrade', 'downgrade', 'neutral')),
    conditions TEXT,                       -- When this pattern applies
    evidence TEXT,                         -- What data supports it
    discovered_date TEXT NOT NULL,
    last_validated TEXT,
    times_applied INTEGER DEFAULT 0,
    active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX idx_decisions_date ON decisions(date);
CREATE INDEX idx_decisions_tier ON decisions(tier);
CREATE INDEX idx_decisions_cadence ON decisions(cadence_type);
CREATE INDEX idx_feedback_slug ON feedback(slug);
CREATE INDEX idx_patterns_active ON patterns(active);

-- ============================================================
-- Views for common queries
-- ============================================================

-- Tier distribution over time (monthly)
CREATE VIEW IF NOT EXISTS v_tier_distribution AS
SELECT
    strftime('%Y-%m', date) AS month,
    tier,
    tier_name,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY strftime('%Y-%m', date)), 1) AS pct
FROM decisions
WHERE cadence_type = 'daily'
GROUP BY strftime('%Y-%m', date), tier
ORDER BY month, tier;

-- Average confidence by tier
CREATE VIEW IF NOT EXISTS v_confidence_by_tier AS
SELECT
    tier,
    tier_name,
    COUNT(*) AS total,
    ROUND(AVG(confidence), 3) AS avg_confidence,
    ROUND(MIN(confidence), 3) AS min_confidence,
    ROUND(MAX(confidence), 3) AS max_confidence
FROM decisions
GROUP BY tier;

-- Calibration accuracy (stated confidence vs actual correctness)
CREATE VIEW IF NOT EXISTS v_calibration AS
SELECT
    d.tier,
    COUNT(*) AS assessed_count,
    SUM(f.was_correct) AS correct_count,
    ROUND(AVG(d.confidence), 3) AS avg_stated_confidence,
    ROUND(AVG(f.was_correct) * 1.0, 3) AS actual_accuracy,
    ROUND(AVG(d.confidence) - AVG(f.was_correct) * 1.0, 3) AS calibration_gap
FROM decisions d
JOIN feedback f ON d.slug = f.slug
GROUP BY d.tier;

-- Brier score (lower is better — 0 is perfect calibration)
CREATE VIEW IF NOT EXISTS v_brier_score AS
SELECT
    ROUND(AVG((d.confidence - f.was_correct) * (d.confidence - f.was_correct)), 4) AS brier_score,
    COUNT(*) AS sample_size
FROM decisions d
JOIN feedback f ON d.slug = f.slug;

-- Most common anti-inflation flags
CREATE VIEW IF NOT EXISTS v_anti_inflation_frequency AS
SELECT
    json_each.value AS flag,
    COUNT(*) AS times_triggered
FROM decisions, json_each(decisions.anti_inflation_flags)
WHERE anti_inflation_flags IS NOT NULL
  AND anti_inflation_flags != '[]'
GROUP BY json_each.value
ORDER BY times_triggered DESC;

-- Top posts by teaching potential
CREATE VIEW IF NOT EXISTS v_top_teaching AS
SELECT
    date, slug, tier, tier_name, dim_tch, thesis_candidate
FROM decisions
WHERE cadence_type = 'daily'
ORDER BY dim_tch DESC, confidence DESC
LIMIT 20;

-- Weekly velocity
CREATE VIEW IF NOT EXISTS v_weekly_velocity AS
SELECT
    strftime('%Y-W%W', date) AS week,
    COUNT(*) AS posts,
    SUM(CASE WHEN tier = 1 THEN 1 ELSE 0 END) AS tier1,
    SUM(CASE WHEN tier = 2 THEN 1 ELSE 0 END) AS tier2,
    SUM(CASE WHEN tier = 3 THEN 1 ELSE 0 END) AS tier3,
    ROUND(AVG(confidence), 3) AS avg_confidence
FROM decisions
WHERE cadence_type = 'daily'
GROUP BY strftime('%Y-W%W', date)
ORDER BY week;

-- Decision quality matrix (Annie Duke 2x2)
-- Good decision + good outcome, good decision + bad outcome, etc.
CREATE VIEW IF NOT EXISTS v_decision_quality AS
SELECT
    CASE
        WHEN d.confidence >= 0.7 AND f.was_correct = 1 THEN 'good-decision-good-outcome'
        WHEN d.confidence >= 0.7 AND f.was_correct = 0 THEN 'good-decision-bad-outcome'
        WHEN d.confidence < 0.7 AND f.was_correct = 1 THEN 'lucky-outcome'
        WHEN d.confidence < 0.7 AND f.was_correct = 0 THEN 'bad-decision-bad-outcome'
    END AS quadrant,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM decisions d
JOIN feedback f ON d.slug = f.slug
GROUP BY quadrant;

-- ============================================================
-- Import helper (call from Python/shell after creating tables)
-- ============================================================
-- To import from JSONL, use a script that reads each line as JSON
-- and inserts into the appropriate table. The JSONL files are the
-- source of truth; this SQLite DB is a derived, queryable index.
--
-- Example Python import:
--   import json, sqlite3
--   conn = sqlite3.connect('methodology/index.db')
--   for line in open('methodology/decisions.jsonl'):
--       rec = json.loads(line)
--       conn.execute('''INSERT OR REPLACE INTO decisions
--           (date, slug, tier, tier_name, confidence,
--            dim_novelty, dim_arc, dim_nar, dim_tch, dim_scp, dim_rpr,
--            reasoning, alternatives_considered, thesis_candidate,
--            rhetorical_structure, sig_git, sig_prs, sig_session,
--            sig_beads, sig_email, cadence_type, anti_inflation_flags)
--           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
--           (rec['date'], rec['slug'], rec['tier'], rec['tier_name'],
--            rec['confidence'],
--            rec['dimensions']['novelty'], rec['dimensions']['arc'],
--            rec['dimensions']['nar'], rec['dimensions']['tch'],
--            rec['dimensions']['scp'], rec['dimensions']['rpr'],
--            rec['reasoning'], rec['alternatives_considered'],
--            rec['thesis_candidate'], rec['rhetorical_structure'],
--            rec['source_signals'].get('git', 'absent'),
--            rec['source_signals'].get('prs', 'absent'),
--            rec['source_signals'].get('session', 'absent'),
--            rec['source_signals'].get('beads', 'absent'),
--            rec['source_signals'].get('email', 'absent'),
--            rec.get('cadence_type', 'daily'),
--            json.dumps(rec.get('anti_inflation_flags', []))))
