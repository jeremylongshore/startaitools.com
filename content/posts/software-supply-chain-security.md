+++
title = 'Software Supply Chain Security After Axios'
slug = 'software-supply-chain-security'
date = 2026-04-02T08:00:00-05:00
draft = false
tags = ["security", "supply-chain", "open-source", "ci-cd", "devops"]
categories = ["Technical Deep-Dive"]
description = "The axios npm compromise validated every warning in a 38-page supply chain security survey. Three attack vectors, one incident, six steps to act on."
toc = true
tldr = "A North Korea-nexus threat actor backdoored axios (~100M weekly downloads) through a compromised maintainer account. A major academic survey had already mapped the three attack vectors this exploit used — dependencies, build infrastructure, and humans — and documented why current defenses fail at each one. Here is what the research says and what to do about it."
+++

On March 31, 2026, attackers published two malicious versions of axios — a package with roughly 100 million weekly npm downloads — during a window of a little over three hours. Google Threat Intelligence Group attributed the campaign to UNC1069, a North Korea-nexus threat actor. The malicious releases introduced a dependency that used a postinstall script to deploy a cross-platform remote access trojan.

During that window, any CI/CD pipeline or developer workstation that freshly resolved the affected versions and allowed lifecycle scripts to run could have been compromised. Projects with previously committed lockfiles were far less likely to be affected.

A 38-page academic paper had already explained exactly how and why this would happen.

## The Paper That Called It

Williams et al. published "Research Directions in Software Supply Chain Security" in ACM TOSEM in May 2025. Fifteen researchers from the NSF-funded S3C2 consortium synthesized findings from eight summits with 131 practitioners across 42 industrial organizations and 15 US government agencies. They identified three attack vectors: code dependencies, build infrastructure, and humans.

The axios compromise hit all three simultaneously.

I read this paper the same week the axios incident broke. The overlap is not a coincidence — it's confirmation that we have a well-understood problem and a deeply inadequate response.

## What Happened

The group Google Threat Intelligence tracks as UNC1069 (Microsoft calls them Sapphire Sleet) compromised the npm account of axios maintainer jasonsaayman. They published two versions — 1.14.1 and 0.30.4 — targeting both the current and legacy release lines. Both added a new dependency: `plain-crypto-js`.

That dependency's `postinstall` hook downloaded a platform-specific RAT from `sfrclak[.]com:8000`. macOS, Windows, Linux — all covered. In npm, `postinstall` scripts run automatically during `npm install`. No user interaction required. No warning displayed.

The exposure window was a little over three hours before community detection triggered a takedown. That's a long time for a package installed roughly 100 million times per week.

The initial compromise path was familiar — credential theft followed by a malicious publish. But the downstream payload was serious: a staged dependency, a cross-platform RAT with macOS/Windows/Linux coverage, and cleanup behavior to hide the postinstall evidence. It worked against one of the most popular packages in the ecosystem.

## Vector 1: The Dependency Problem

Sonatype logged **512,847 malicious packages** in 2024 — a **156% increase** year-over-year. Meanwhile, 96% of commercial code bases contain open source components, and 77% of all code is open source (Synopsys). The attack surface grows faster than detection capability.

The paper documents that detection tools for malicious packages have **false positive rates exceeding 15%** (Vu et al.). At that rate, automated blocking is impractical — you can't reject one in seven legitimate packages. So most malicious packages get through, and the ones that get caught are caught by humans who happen to notice.

The axios attacker exploited the most basic trust assumption in package management: that a published version of a popular package is safe, and that its dependencies are reviewed. `plain-crypto-js` was a brand-new package. Nobody reviewed it because postinstall hooks execute automatically.

The broader picture is worse. Three thousand popular npm packages (over 10K monthly downloads each) are abandoned. Vulnerabilities remain undiscovered for an average of **three years**. When they are discovered, 63% of security advisories in the GitHub Advisory Database lack patch links. We're failing to respond to known vulnerabilities, let alone prevent new attacks.

## Vector 2: Your CI/CD Pipeline Is the Weapon

Any pipeline or workstation that freshly resolved axios during the exposure window and allowed lifecycle scripts to run was a potential victim. The RAT didn't need to trick a developer. It just needed the build pipeline to do what build pipelines do: resolve dependencies and run scripts. Projects with committed lockfiles that didn't update were not affected.

The paper found that only **20% of software builds** match bit-to-bit when reproduced. Eighty percent of builds can't prove they haven't been tampered with. The ARGUS study analyzed 2.8 million GitHub Actions workflows across one million repositories and found code injection vulnerabilities in 4,307 of them.

SolarWinds demonstrated the category in 2020 — attackers compromised a vendor's build and update channel to sign malicious code with official keys. The axios incident is a different mechanic (registry publish via a compromised maintainer account) but the same underlying failure: build systems trust what they install, and attackers exploit that trust at whatever layer is weakest.

SLSA (Supply-chain Levels for Software Artifacts) defines maturity levels for build provenance. Sigstore has accumulated over 2.2 million signatures across critical software projects. But most organizations have no provenance metadata, no build attestation, no verification. The tools exist. The adoption doesn't.

## Vector 3: The Human Problem Has No Patch

The axios attack started with a compromised human. Jasonsaayman's npm credentials were the entry point. Everything else followed from that single point of failure.

The 2024 Tidelift survey found that **60% of open source maintainers are unpaid**. They spend 11% of their time on security — up from 4% in 2021 — a nearly threefold increase in security burden with no increase in compensation. Only 14% have formal processes to prioritize security issues.

The xz-utils attack in 2024 showed the extreme case: a multi-year social engineering campaign targeted a burned-out solo maintainer. The attacker gained trust, became a co-maintainer, and inserted a backdoor into a compression library used by virtually every Linux distribution. The paper's authors admit: "it is unclear if any existing security practice could have meaningfully prevented or even detected the xz-utils attack."

You can mandate 2FA. You can enforce credential rotation. But the human attack surface is not a technical problem with a technical solution. It's a systemic problem rooted in how open source is funded, maintained, and governed.

## What to Do Monday Morning

The paper catalogs frameworks — SLSA, SBOMs, OpenSSF Scorecard, Sigstore — and documents their limitations. OpenSSF Scorecard has only 9 of 18 metrics that are reliably computable, and its ability to predict actual vulnerabilities is weak (R-squared of 9-12%, meaning it explains almost none of the variance). SBOMs are mandated by Executive Order 14028, but 71% of NVD entries lack the patch links that make them actionable.

The frameworks matter, but none of them would have stopped the axios attack alone. Defense-in-depth is the only viable strategy. Six steps, ordered by effort:

1. **Pin exact dependency versions with integrity hashes.** Stop resolving to latest. If your lockfile specified axios 1.14.0 with a hash, the malicious 1.14.1 never installed.

2. **Disable postinstall scripts in CI.** Run `npm install --ignore-scripts` and whitelist explicitly. The axios RAT relied entirely on a postinstall hook. No execution, no compromise.

3. **Enable 2FA on every package registry account.** npm, PyPI, RubyGems — all of them. The axios attacker got in through compromised credentials.

4. **Run OpenSSF Scorecard on your critical dependencies.** It's imperfect, but it surfaces obvious red flags: no branch protection, no code review, no signed releases.

5. **Adopt SLSA level 1 for your own builds.** Generate provenance metadata. It costs almost nothing and gives you a baseline for build integrity.

6. **Fund your dependencies.** If 60% of maintainers are unpaid and your business runs on their code, your security budget should include them. Tidelift, GitHub Sponsors, Open Collective — pick one.

None of these are sufficient alone. The xz-utils attack would have bypassed most of them. That's the point — make the attacker's job harder at every layer.

## The Gap Between Knowledge and Action

The Williams et al. paper is not a prediction. It's a diagnosis. The researchers documented failure modes that practitioners already know about, backed by data from 131 industry participants who confirmed: yes, these are the problems, and no, we haven't solved them.

The axios compromise didn't reveal a new vulnerability. It demonstrated an old one, at scale, against a trusted target, by a nation-state-linked adversary. The three-hour window between compromise and remediation is a testament to the community's response speed — but lockfiles, `npm ci`, and `--ignore-scripts` would have blocked exposure without relying on detection at all. Response speed was the most visible defense that worked in real time. It shouldn't have been the primary one.

Read the paper. It's 38 pages. It won't make your dependencies safe. But it will show you exactly where the risks are, what exists to counter them, and why none of it is enough yet.

---

**Related posts:**

- [Building Moat: Auth, On-Chain Receipts, and 117 Integration Tests](/posts/building-moat-auth-persistence-onchain-receipts-117-tests/) -- security-first architecture with defense-in-depth testing
- [Building Production-Grade CI/CD: From Documentation Chaos to Automated Deployment](/posts/building-production-ci-cd-documentation-to-deployment/) -- the pipeline infrastructure that supply chain attacks target
- [Verified Plugins Program: Building a Quality Signal for the Marketplace](/posts/verified-plugins-program-quality-signal-for-the-marketplace/) -- trust signals and quality gates for third-party code
