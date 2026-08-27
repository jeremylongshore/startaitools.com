# Omarchy Plugin Promotion Reference

Use this reference when writing a Start AI Tools article, social post, launch
note, or case study about Jeremy Longshore and Intent Solutions' Omarchy work.
It describes what is built, how it is built, and the claims the evidence can
support as of 2026-08-27.

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
fresh shell, render the widget, and capture a preview. It is not a claim that
every possible hardware state has been simulated.

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

## Current work to describe accurately

Eight earlier portfolio plugins are listed and verified in the marketplace.
Six newer entries are public and submitted for marketplace review:

| Plugin | Plain-language promise | Submission |
| --- | --- | --- |
| Loose Ends | Turns unfinished local Git work into a drainable bar queue. | [#2899](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2899) |
| Capture Conveyor | Provides a local inbox for recent Omarchy screenshots. | [#2900](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2900) |
| Workspace Storyboard | Helps re-enter active local workspaces. | [#2901](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2901) |
| Quiet Queue | Runs an owner-aware focus interval for notification silencing. | [#2902](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2902) |
| Flow Boundary | Records intentional local start and stop boundaries. | [#2903](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2903) |
| Desk Transition | Safely arranges active displays or returns focus to an internal panel. | [#2921](https://github.com/HANCORE-linux/omarchy-plugin-marketplace/issues/2921) |

Use “submitted” or “pending marketplace review” for these six. Do not call
them listed, approved, verified by marketplace staff, or universally E2E-tested.

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
- [Marketplace](https://omarchyplugins.com)
- [Omarchy](https://omarchy.org)
