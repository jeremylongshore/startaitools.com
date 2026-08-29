# Omarchy Plugin Promotion Reference

Use this reference when writing a Start AI Tools article, social post, launch
note, or case study about Jeremy Longshore and Intent Solutions' Omarchy work.
It describes what is built, how it is built, and the claims the evidence can
support as of 2026-08-28. Treat the evidence receipts and marketplace labels as
the authority when this document and a live system ever disagree.

## The short version

Intent Solutions builds small, native Omarchy Quattro widgets that answer one
specific desktop question without turning the bar into a generic dashboard.
The shared bet is not that a model can generate QML quickly. It is that each
plugin begins with a constrained template, must pass deterministic checks, and
is loaded in a real Omarchy shell before it is presented as ready.

The portfolio landing page is
[`intent-solutions-io/omarchy-plugins`](https://github.com/intent-solutions-io/omarchy-plugins).
The reusable starting point is
[`jeremylongshore/omarchy-widget-template`](https://github.com/jeremylongshore/omarchy-widget-template).
The reusable submission workflow is `$omarchy-ship`, located at
`/home/jeremy/.codex/skills/omarchy-ship/`. It is model-agnostic: any capable
assistant or engineer can run it, and its conclusions come from commands and
artifacts rather than the identity of the model that ran them.

## What the template establishes

Each entry is a Quickshell/QML Omarchy plugin with a `manifest.json`, bar
widget, panel, pure `Model.js` data layer, tests, CI, a README, and a curated
SVG banner. The template separates data parsing from QML so captured inputs can
be tested outside the compositor.

Its non-negotiable posture is practical rather than decorative:

- untrusted network text is cleaned before rendering and rendered as plain
  text;
- network calls are bounded by time and response size;
- untrusted values do not become shell arguments;
- a plugin does not silently disappear when a remote source is unavailable;
- runtime behavior does not depend on Node, Python, or another development-only
  interpreter being on an end user's graphical session PATH.

Do not describe the template as a guarantee that a plugin is safe. Describe it
as a repeatable baseline that makes the checks and their scope explicit.

## Development and proof lane

Development uses the persistent Buzz Omarchy rig, `intent-ops-buzz/omarchy-rig`.
It is the real development container used to validate plugin trees, load a
fresh shell, render the widget, capture a preview, and exercise installation
flows. It is not a claim that every possible hardware state has been simulated.

The `$omarchy-ship` lane checks the actual plugin root, compares the vendored
gate lane against its canonical denominator, runs offline tests, validates with
`omarchy-plugin-validate`, runs `qmllint`, renders in a real shell, and requires
a deliberate red-proof experiment. Its key rule is: a skipped applicable check
is **UNPROVEN**, not passed. A submission body is emitted only after a CLEAN
verdict; filing or pushing still requires separate authorization.

For promotional copy, distinguish these facts:

- **Static validation** proves the manifest/QML can be checked. It does not
  prove the plugin loaded.
- **Fresh-shell render** proves it loaded in the rig. It is stronger evidence
  than a screenshot from an old process.
- **Command-level tests** can prove the helper emits safe expected commands;
  they do not prove a physical monitor changed on every hardware configuration.
- A marketplace issue means **submitted for review**, not listed, approved, or
  security-certified.

## Current marketplace status

Marketplace labels, not the age of a GitHub issue, determine the language to
use. As of 2026-08-28, five entries remain public submissions with
`needs-fixes`; Desk Transition is listed and snapshot-verified.

| Plugin | Plain-language promise | Current marketplace state |
| --- | --- | --- |
| Loose Ends | Turns unfinished local Git work into a drainable bar queue. | [#2899](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2899) · submitted · needs fixes |
| Capture Conveyor | Provides a local inbox for recent Omarchy screenshots. | [#2900](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2900) · submitted · needs fixes |
| Workspace Storyboard | Helps re-enter active local workspaces. | [#2901](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2901) · submitted · needs fixes |
| Quiet Queue | Runs an owner-aware focus interval for notification silencing. | [#2902](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2902) · submitted · needs fixes |
| Flow Boundary | Records intentional local start and stop boundaries. | [#2903](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2903) · submitted · needs fixes |
| Desk Transition | One-click Desk and Laptop display scenes that never disable an output. | [#2921](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2921) · listed · snapshot verified |

Desk Transition was redesigned at
[`02c8814`](https://github.com/jeremylongshore/omarchy-desk-transition-entry/commit/02c8814be2b2075c7aebbe0d19a8d29eb8c2e2d4): its panel now shows explicit Desk
and Laptop scene cards, a useful no-display state, and a tight crop from a real
Buzz render for the listing image. The repository's test and gate workflows are
green for that commit. The marketplace's existing snapshot may still show the
old image until a verifier refreshes the already-listed entry. Do not claim the
new preview has itself been marketplace-verified before that refresh.

Use “listed and snapshot-verified” only for Desk Transition's current listing.
Use “submitted; needs fixes” for the other five. None of those labels means a
universal hardware E2E guarantee or a security certification.

## Foundry status

[Foundry](https://github.com/jeremylongshore/omarchy-foundry-entry) is public
development work, not a marketplace submission. It creates a constrained local
starter tree for a bar widget and deliberately stops before install, enable,
Git push, or marketplace filing.

Its current evidence goes beyond unit tests. The published source has seven
offline tests, nine enforced repository gates, and a 10/10 canonical-lane
freshness comparison. GitHub Actions' test and gate workflows are green at
[`1ccaa75`](https://github.com/jeremylongshore/omarchy-foundry-entry/commit/1ccaa7539c04d29c9823f43a98fe07f040855e6b).
The Buzz rig validated and rendered Foundry with zero validator errors, zero
QML lint errors, and no plugin-sourced shell-load warnings.

The stronger claim is backed by the tracked
`.rig-e2e-proof.json` receipt: the rig installed the exact Foundry commit from
GitHub, generated a disposable starter tree, committed and installed that tree
from a local Git URL, loaded it in a real Omarchy shell while Node was shadowed
with a failing stub, and rejected a hostile plugin id. The receipt records both
the installed Foundry SHA and generated-tree SHA. A deliberate isolated red
proof removed ID validation and made the unit suite fail; the original source
was untouched and re-run green.

The generated tree's standalone `qmllint` run emits expected
import-resolution warnings because the disposable directory sits outside the
shell's normal import path. Its real shell load is the decisive runtime proof.

Use “public, CI-green, and proven through Buzz-rig E2E” for Foundry. Do not say
it is marketplace-submitted, marketplace-approved, universally production-safe,
or capable of autonomously writing and publishing arbitrary plugin code. Foundry
creates a constrained starter tree and requires explicit human decisions for
testing, installation, Git actions, and marketplace filing.

## Evidence language Claude should preserve

Prefer these bounded phrases:

- “loaded in a fresh Omarchy shell on the Buzz rig”;
- “installed from the recorded GitHub commit during the E2E run”;
- “generated plugin loaded with Node absent from the session path”;
- “snapshot-verified marketplace listing” only where the marketplace label says
  so;
- “tests and gates passed” only with the repository or receipt named nearby.

Never flatten the evidence into “fully tested,” “secure,” “production certified
by Omarchy,” or “AI publishes plugins automatically.” The proof is concrete and
useful precisely because it says what was checked and what remains a human or
marketplace decision.

## The story worth telling

Lead with a concrete question a widget answers, then explain the engineering
discipline behind it. Good: “A bar widget that makes the unfinished work on
this machine visible without uploading it anywhere.” Better still: show the
pill and panel in a short clip, then name the tests that kept the claim honest.

Avoid generic claims such as “AI built an entire plugin ecosystem overnight,”
“fully tested everywhere,” “secure by default,” or “the marketplace approved
it.” The interesting story is more credible: assisted development moved fast
because deterministic gates, a real shell rig, and an evidence-first submission
process made fast feedback possible without pretending uncertainty was proof.

## Useful links

- [Portfolio umbrella](https://github.com/intent-solutions-io/omarchy-plugins)
- [Widget template](https://github.com/jeremylongshore/omarchy-widget-template)
- [Foundry](https://github.com/jeremylongshore/omarchy-foundry-entry)
- [Marketplace](https://omarchyplugins.com)
- [Omarchy](https://omarchy.org)
