-- rebuild-index.sql
-- Derives a SQLite analytics index from the JSONL source-of-truth files.
-- Run the canonical rebuild-methodology-index.sh; never apply this directly to index.db.
-- Candidate-only schema v2; rebuild helper atomically publishes validated output.
PRAGMA user_version = 2;
PRAGMA foreign_keys = ON;

CREATE TABLE source_records (
    source TEXT NOT NULL, line_number INTEGER NOT NULL, raw_line TEXT NOT NULL,
    sha256 TEXT NOT NULL, kind TEXT NOT NULL,
    PRIMARY KEY (source, line_number)
);
CREATE TABLE source_accounting (
    source TEXT PRIMARY KEY, sha256 TEXT NOT NULL, total_lines INTEGER NOT NULL,
    json_records INTEGER NOT NULL, blank_lines INTEGER NOT NULL
);
CREATE TABLE index_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE post_identities (
    slug TEXT PRIMARY KEY, provenance TEXT NOT NULL, content_path TEXT,
    content_sha256 TEXT, content_commit TEXT, published_date TEXT
);

-- ============================================================
-- Schema
-- ============================================================

DROP TABLE IF EXISTS decisions;
CREATE TABLE decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,                    -- YYYY-MM-DD
    slug TEXT NOT NULL UNIQUE REFERENCES post_identities(slug),
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
    applied_patterns TEXT,                 -- JSON array of pattern_ids fired by apply-patterns.py (Thread B2)
    created_at TEXT DEFAULT (datetime('now'))
);

DROP TABLE IF EXISTS feedback;
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
    date_assessed TEXT NOT NULL,           -- When the feedback was recorded
    original_tier INTEGER CHECK (original_tier BETWEEN 1 AND 4),
    original_tier_status TEXT NOT NULL CHECK (original_tier_status IN ('known', 'legacy_unknown')),
    classification_status TEXT NOT NULL CHECK (classification_status IN ('classified', 'legacy_unclassified')),
    source_line INTEGER NOT NULL,
    correct_tier INTEGER,                  -- NULL if original was correct
    was_correct INTEGER CHECK (was_correct IN (0, 1)),
    reasoning TEXT,
    year_from_now_useful INTEGER,          -- 1/0/NULL
    engagement_data TEXT,                  -- JSON: views, shares, comments
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (slug) REFERENCES post_identities(slug)
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
JOIN feedback f ON d.slug = f.slug AND f.original_tier = d.tier
GROUP BY d.tier;

-- Brier score (lower is better — 0 is perfect calibration)
CREATE VIEW IF NOT EXISTS v_brier_score AS
SELECT
    ROUND(AVG((d.confidence - f.was_correct) * (d.confidence - f.was_correct)), 4) AS brier_score,
    COUNT(*) AS sample_size
FROM decisions d
JOIN feedback f ON d.slug = f.slug AND f.original_tier = d.tier;

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

-- Learned-pattern usage: how often each pattern actually fired, from
-- decisions.applied_patterns (Thread B2). This is the live signal; the
-- times_applied field in patterns.jsonl is its backfilled snapshot.
CREATE VIEW IF NOT EXISTS v_pattern_usage AS
SELECT
    json_each.value AS pattern_id,
    COUNT(*) AS times_fired
FROM decisions, json_each(decisions.applied_patterns)
WHERE applied_patterns IS NOT NULL
  AND applied_patterns != '[]'
GROUP BY json_each.value
ORDER BY times_fired DESC;

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
JOIN feedback f ON d.slug = f.slug AND f.original_tier = d.tier
GROUP BY quadrant;


-- Explicit historical exclusions: never included in calibration by invented tiers.
CREATE VIEW v_legacy_unclassified AS
SELECT slug, original_tier, original_tier_status, classification_status, source_line
FROM feedback WHERE original_tier_status = 'legacy_unknown'
OR classification_status = 'legacy_unclassified';
