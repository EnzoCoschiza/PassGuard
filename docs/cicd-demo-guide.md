# PassGuard CI/CD Demo Guide

## Purpose

This guide turns the existing GitHub Actions workflows into a coherent CI/CD demo.
Each suggested pull request exercises one type of protection without leaving an
intentional failure in `main`.

## Workflow Map

- `CI` in `.github/workflows/ci.yml`
  - Backend: `uv run ruff check .`, `uv run pytest`
  - Frontend: `npm run lint`, `npm run test`, `npm run build`
- `Linear Traceability` in `.github/workflows/linear-traceability.yml`
  - Runs on pull requests
  - Fails when the PR title, branch name, and body do not contain a Linear issue
    reference like `PASS-123`
- `Deploy Frontend` in `.github/workflows/pages.yml`
  - Runs on push to `main` or `master`
  - Rebuilds the frontend, runs a deploy smoke test, and publishes
    `frontend/dist` to GitHub Pages only if the smoke test passes
- `SonarCloud` in `.github/workflows/sonarqube.yml`
  - Optional for the demo
  - Useful only if `SONAR_TOKEN` is configured in GitHub

## Linear Feedback Loop

Use Linear as the visible feedback platform:

1. Create an issue such as `PASS-12 Relajar validacion de anios academicos`.
2. Create a branch named `pass-12-allow-academic-year-passwords`.
3. Open a PR titled `PASS-12 Allow academic year passwords`.
4. Include `Fixes PASS-12` in the PR body.
5. Show that Linear links the PR/checks back to the issue through the GitHub
   integration.

The repository also has a PR gate named `Linear issue reference`. It fails if a
PR cannot be traced to an issue ID in the `PASS-123` format.

## Suggested Demo Flow

### PR 0: Healthy baseline

- Objective: show the repository in a passing state before breaking anything.
- Files to touch: none, or a low-risk doc change like `README.md`.
- Change type: no-op or documentation-only.
- Expected checks: all green in `CI`; `Deploy Frontend` runs after merge to `main`
  or `master`, or when started manually with `workflow_dispatch`.
- Teaching message: CI starts from a known-good baseline and gives confidence before new work.

### PR 1: Frontend lint failure

- Objective: show that style and code quality rules block a merge even when behavior looks unchanged.
- Files to touch: `frontend/src/App.tsx`
- Change type: introduce an obvious ESLint issue such as an unused local variable inside `App`.
- Expected check: `Frontend` job fails at `npm run lint`.
- Teaching message: CI protects consistency and catches rushed edits early.

### PR 2: Backend logic regression caught by tests

- Objective: show that business rules are enforced by backend tests.
- Files to touch: `app/services/analyzer.py`
- Change type: implement the Linear request to stop penalizing academic years
  like `2026`.
- Expected check: `Backend` job fails at `uv run pytest`.
- Good target assertions:
  - `tests/test_analyzer.py::test_year_detection_penalizes_score`
  - `tests/test_api.py::test_analyze_password_contract`
- Teaching message: feedback can request a plausible feature, but CI protects the
  SDD rule that years between `1900` and `2099` are predictable and must remain
  penalized.

### PR 3: Frontend behavior regression caught by tests

- Objective: show that UI behavior is also covered by automated tests.
- Files to touch: `frontend/src/App.tsx`
- Change type: rename visible text or alter an error message without updating tests.
- Expected check: `Frontend` job fails at `npm run test`.
- Good target assertions:
  - `frontend/src/App.test.tsx` looks for `Analizar`
  - `frontend/src/App.test.tsx` looks for `No se pudo analizar la contrasena. Intenta de nuevo.`
- Teaching message: UI contracts can be tested and protected in CI.

### PR 4: Frontend build failure

- Objective: show that a project can pass some checks and still fail to ship.
- Files to touch: `frontend/src/App.tsx` or `frontend/src/api.ts`
- Change type: create a TypeScript or import mismatch that compiles locally only as source text, not as a build.
- Expected check: `Frontend` job fails at `npm run build`.
- Safe demo examples:
  - import a symbol that does not exist
  - reference a response property that is not present in `AnalyzePasswordResponse`
- Teaching message: build validation catches integration issues beyond lint and tests.

### PR 5: Fixed version of a previously failing PR

- Objective: show the intended development loop: fail, inspect, fix, rerun, merge.
- Files to touch: same files as the failed PR.
- Change type: correct the broken code and update tests only if the product change is intentional.
- Expected check: all `CI` checks pass.
- Teaching message: CI is a feedback mechanism, not just a gate.

### PR 6: Merge and show CD

- Objective: close the demo with deployment evidence.
- Files to touch: any already-approved change.
- Change type: merge an all-green PR into `main`.
- Expected check: `Deploy Frontend` workflow runs tests, builds the frontend,
  passes the deploy smoke test, and updates GitHub Pages.
- Teaching message: CI validates quality before CD publishes the artifact.

### Optional: Deploy smoke failure

- Objective: show that deploy has its own technical gate after build.
- Files to touch: `frontend/vite.config.ts`
- Change type: intentionally break the GitHub Pages base path, for example by
  building with `/PassGuard-broken/` instead of `/PassGuard/`.
- Expected check: `Deploy Frontend` fails at `Run deploy smoke test`; the deploy
  job is skipped because it depends on the build job.
- Teaching message: a deploy pipeline must validate the deliverable artifact, not
  only compile source code.

## How To Keep The Demo Coherent

- Use one failure type per PR. Avoid stacking multiple broken checks in the same branch.
- Keep changes small and explainable in under one minute.
- Prefer edits in files that already have tests:
  - backend logic: `app/services/analyzer.py`
  - backend API contract: `tests/test_api.py`
  - frontend behavior: `frontend/src/App.tsx`
  - frontend tests: `frontend/src/App.test.tsx`
- Never merge intentionally failing code into `main`.
- Use the local runner script before opening each PR to predict the CI result.

## Local Rehearsal Commands

Run the same essential checks locally:

```powershell
.\scripts\run-ci-checks.ps1
```

The runner sets `UV_CACHE_DIR` to `.cache/uv` inside the repo so it does not
depend on the global `uv` cache.

Only backend:

```powershell
.\scripts\run-ci-checks.ps1 -Scope backend
```

Only frontend:

```powershell
.\scripts\run-ci-checks.ps1 -Scope frontend
```

Install dependencies first if needed:

```powershell
.\scripts\run-ci-checks.ps1 -InstallDeps
```

## Suggested Narration

1. Show `CI` and explain the backend and frontend jobs.
2. Open the Linear issue and show the linked PR.
3. Predict that the PR should fail because it relaxes `YEAR_DETECTED`.
4. Confirm the failing backend tests and connect them to the SDD rule.
5. Push the fix and show the same PR turning green.
6. Merge the green PR and show the deploy smoke test plus GitHub Pages deployment.

## One-Slide Visual

Use `docs/cicd-demo-slide.html` as the single slide requested by the assignment.
It contains the CI/CD scheme and the tool labels for Linear, GitHub, Actions,
Docker, Sonar, FastAPI, React, and Vite.
