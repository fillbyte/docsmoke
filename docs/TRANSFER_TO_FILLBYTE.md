# Transfer to the fillbyte organization

This is the one-time migration runbook for moving the public repository from
`dev-ugurkontel/docsmoke` to `fillbyte/docsmoke`. Repository transfer, PyPI
ownership changes, trusted-publisher changes, tags, and releases are external
operations and must not be inferred from source changes alone.

## Canonical name

Keep all three public names unchanged:

| Surface | Canonical name |
| --- | --- |
| PyPI distribution | `docsmoke` |
| Python import package | `docsmoke` |
| Console command | `docsmoke` |

Do not rename the distribution to `doc-smoke`. Python package indexes
normalize punctuation runs, but they do not insert a separator: `doc-smoke`
and `docsmoke` are different normalized project names. More importantly,
`docsmoke==1.0.0` already exists on PyPI. A rename would create a second
distribution, require a migration release, split download history, and risk
dependency confusion without improving the import or CLI experience.

The project remains authored by Uğur Kontel. Moving repository and package
governance to an organization does not rewrite authorship.

## Verified pre-transfer state

As observed on 2026-08-30:

- GitHub origin is `https://github.com/dev-ugurkontel/docsmoke.git`.
- PyPI serves `docsmoke` version `1.0.0`; `doc-smoke` is not the same project.
- PyPI lists `ugurkontel` as the individual Owner and no PyPI organization.
- The `1.0.0` provenance names `dev-ugurkontel/docsmoke`, workflow
  `release.yml`, and environment `pypi`.

Re-query these facts immediately before migration. They are evidence for this
runbook, not a substitute for current account state.

## Before the GitHub transfer

1. Confirm `fillbyte` has no repository or fork named `docsmoke`.
2. Confirm the operator can create repositories in `fillbyte` and administer
   the source repository.
3. Confirm the organization permits GitHub Actions, GitHub Pages, public
   packages, and third-party actions pinned by this repository.
4. Record current rules, environments, Pages settings, Discussions, security
   settings, Actions permissions, and GHCR package linkage.
5. Merge the ownership-URL preparation through the normal protected-branch
   workflow. Do not rename the repository during transfer.

## Transfer and immediate verification

Transfer the repository in GitHub's repository settings to the `fillbyte`
owner. Then verify:

1. `https://github.com/fillbyte/docsmoke` is public and the old URL redirects.
2. Issues, pull requests, releases, stars, tags `v1` and `v1.0.0`, secrets,
   environments, and deploy keys remain present.
3. The local remote is updated explicitly:

   ```bash
   git remote set-url origin https://github.com/fillbyte/docsmoke.git
   git remote -v
   ```

4. Branch rules use the current CI job names and still require review.
5. Pages deploys from GitHub Actions to `https://fillbyte.github.io/docsmoke/`.
   GitHub does not redirect the old Pages site automatically.
6. Discussions, private vulnerability reporting, Dependabot, secret scanning,
   push protection, and code scanning are enabled.
7. The action resolves as `fillbyte/docsmoke@v1` from a separate smoke-test
   repository.
8. GHCR is linked to the transferred repository and a future release can write
   `ghcr.io/fillbyte/docsmoke`. Preserve the old image until consumers have a
   documented migration path.

Do not recreate `dev-ugurkontel/docsmoke`; doing so can destroy GitHub's old
repository redirect.

## PyPI trusted publishing and ownership

GitHub transfer does not update PyPI's trust policy. Before pushing another
release tag, add or replace the PyPI trusted publisher with:

- owner: `fillbyte`
- repository: `docsmoke`
- workflow: `release.yml`
- environment: `pypi`

Keep the individual `ugurkontel` Owner until a second verified recovery owner
or organization policy is in place. If an approved PyPI organization named
`fillbyte` exists, an organization Owner may separately transfer the existing
`docsmoke` project into it. This is optional for trusted publishing and must
not create a new `doc-smoke` project.

After the new trusted publisher is visible, remove the obsolete publisher for
`dev-ugurkontel/docsmoke`. Never test this by re-uploading `1.0.0`; PyPI release
files are immutable.

## First post-transfer release

1. Choose a version greater than `1.0.0`, update `pyproject.toml`, and move the
   relevant `[Unreleased]` entries into a dated changelog section.
2. Run `make all`, `make build`, and `python -m twine check dist/*` from a clean
   checkout.
3. Merge through the protected branch and create the new exact tag.
4. Approve the `pypi` environment deployment.
5. Verify PyPI provenance names `fillbyte/docsmoke`, the new project URLs point
   to `fillbyte`, GHCR exposes the new owner path, Pages is live, GitHub Release
   artifacts are signed, and moving tag `v1` points to the exact release.
6. Verify both `pipx install docsmoke` and `python -c "import docsmoke"` in a
   fresh Python 3.10+ environment.

The release workflow deliberately moves the public GitHub Release and `v1`
action tag only after PyPI and GHCR publishing succeed.
