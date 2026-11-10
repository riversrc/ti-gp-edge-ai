# Contributing

## Branches

- `main` holds finished versions only (Version 0, 1, 2). Never commit or open a PR
  directly against `main`.
- `dev` is everyday work and the default branch.
- Feature branches come off `dev` and get PR'd back into `dev`.
- When a version is done, `dev` is merged into `main` and tagged `v0.0`, `v1.0`, `v2.0`.

## Short version

1. Pick an assigned issue.
2. Branch from `dev`.
3. Make small commits.
4. Open a PR into `dev` linking the issue.
5. Get 1 approval and a passing CI run.
6. Squash and merge.
7. Delete the branch.

## Branch names

Use `feat/`, `fix/`, `docs/`, or `chore/` plus a short description:

- `feat/fan-blade-widget`
- `fix/csv-player-offset`
- `docs/update-readme`
- `chore/bump-onnxruntime`

```
git checkout dev
git pull
git checkout -b feat/fan-blade-widget
```

## Commit messages

Present tense, under ~70 characters.

Good:
- `Add CSV player window stepping`
- `Fix off-by-one in FFT bin averaging`

Bad:
- `fixed stuff`
- `updates`

## Pull requests

- One task per PR.
- Fill in the PR template.
- Include `Closes #N` so the issue closes automatically.
- Open as Draft if it isn't ready for review yet.
- Merge the latest `dev` into your branch and make sure CI passes before requesting
  review.

## Reviews

- Needs 1 approval from someone else, ideally within about 2 days.
- Comment on the code, not the person.
- Approve when it works and is understandable.
- Request changes only for real problems.
- Author resolves comments, then asks for re-review.

## Merging

- Feature branches squash-merge into `dev`.
- `dev` merges into `main` only at the end of a version, with a merge commit, after
  team approval.

## Releasing a version

1. All milestone issues are closed.
2. `dev` runs successfully on the AM64x board.
3. Open a PR `dev` -> `main` titled "Release Version N".
4. Merge with a merge commit.
5. Create a GitHub Release tagged `vN.0`.

## Code style

- Every Python file starts with a docstring saying what it does.
- Settings belong in the demo YAML, not hard-coded in Python or JS.

## Offline rule

The dashboard must work with no internet connection: no CDN links, no web fonts, no
online APIs. Copy any needed libraries into `frontend/vendor/`.

## Large files

- Commit CSVs and `.onnx` files only if they're under ~50 MB.
- Ask before committing anything bigger.
- Never commit secrets.

## Weekly reports

Link the PRs merged into `dev` that week.
