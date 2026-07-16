# Security Policy

## Scope

This repository holds the source for the static blog published at
[startaitools.com](https://startaitools.com). It contains no user data, no
authentication, and no server-side application code. The most relevant security
concerns are therefore:

- Vulnerabilities in the published site (for example, an XSS vector introduced
  through embedded HTML in a post, since the Hugo renderer runs with
  `unsafe = true`).
- Exposure of a secret accidentally committed to the repository or its history.
- Compromise of the build or deploy pipeline.

## Reporting a Vulnerability

Please report suspected vulnerabilities privately. Do **not** open a public
GitHub issue for a security problem.

- Email: **jeremy@intentsolutions.io**
- Include: a description, the affected URL or file, and reproduction steps.

You can expect an initial acknowledgement within a few business days. Once a fix
is shipped, the reporter is credited unless anonymity is requested.

## Supported Versions

Only the currently deployed site (the `master` branch) is supported. There are
no maintained release branches.
