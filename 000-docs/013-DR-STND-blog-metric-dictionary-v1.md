# 013 — Blog metric dictionary v1

| Field | Value |
|---|---|
| Date | 2026-10-05 |
| Status | Frozen at v1.0.0. Machine record: `scripts/blog/metric-dictionary.json` (authoritative if this page and the JSON disagree) |
| Beads | `startaitools-9a8.2.3` (dictionary), `startaitools-9a8.13.3` (versioned reports) |
| Derived from | Measurement contract v1.0.0 (private store, sha256 `e370f7cf…3a56`), baselines `baseline-v1` and `baseline-v1-tos`, `weekly_metrics.py`, `traffic_quality.py`, `native-metrics-devto.py` |
| Governs | Every number in the weekly rollup and in recovery or pilot readouts |

## Why

Earlier reports put numbers side by side whose denominators differed: a year-over-year change
against a year with no collection, an all-sites total compared across the week the site list grew,
a 7-day statistic over one post cohort beside a 28-day statistic over a smaller one, and
per-placement rates set against per-post rates. Each of those reads as a trend and measures nothing.
The dictionary gives each reported metric one definition and makes an ineligible comparison print
`n/a` with its reason.

## What every metric states

Numerator, denominator, eligibility, window, filter version, unit, and the rule that turns an
ineligible or failed value into a named state instead of a 0. The dictionary carries definitions
only. Measured values and baselines stay in the private measurement store.

## The number at the top

| Phase | Measure | Unit |
|---|---|---|
| Recovery | Open critical exceptions, with the age of the oldest | exception, day |
| Pilot (primary) | Search-referred filtered sessions per article in its first 28 days | session |
| Pilot (secondary) | Outbound clicks to the demonstrated resource per 100 filtered article sessions | event session per 100 sessions |

## Rules that do not bend

- **Sessions are not people.** Umami's "visitors" column counts sessions; the id rotates monthly.
- **Clicks are not outcomes.** An `outbound_click` is an attempt, never a visit, install, download,
  subscription, accepted inquiry or revenue.
- **Unknown, unavailable, n/a and zero stay distinct.** A failed query is `unavailable`, an
  unrecorded quantity is `unknown`, an ineligible window is `n/a`; only a successful query over an
  eligible window yields `0`.
- **A comparison needs one definition on both sides**: same metric, dictionary major version, filter
  version and tier, unit, denominator and population, with both windows fully observed. Otherwise it
  is `n/a`.
- **Native platform numbers keep their own units.** Dev.to page views are platform-reported lifetime
  counts. They are never added to, compared with, or divided by site sessions.

## Versioning

A definition never changes in place. Adding a metric is a minor version. Changing a numerator,
denominator, eligibility, window, filter or unit is a major version, and the baseline is recomputed
under both versions for one overlap period. Every weekly rollup prints the report version, the
dictionary version and sha, and the filter version it used. The first rollup on a new major or minor
version carries a one-time baseline-reset note.

## Check

`python3 scripts/blog/metric_dictionary.py check` validates the file; `tests/test_metric_dictionary.py`
runs in CI.
