## Summary

Describe the change in one or two sentences.

## Linear

Linear issue:

Use the `PASS-123` format in the title, branch name, or body. The
`Linear issue reference` check fails when the PR cannot be traced to feedback.

## Demo Change Type

- [ ] Healthy baseline / green PR
- [ ] Intentional CI failure for the demo
- [ ] Fix for a previously failing demo PR
- [ ] Other repository change

## Expected Check Outcome

- [ ] Backend should fail
- [ ] Frontend lint should fail
- [ ] Frontend tests should fail
- [ ] Frontend build should fail
- [ ] All CI checks should pass

Expected workflow/check names:

- `Backend`
- `Frontend`
- `Deploy Frontend` after merge to `main`
- `SonarCloud` only if configured

## Files Touched

List the main files changed and why they are part of the demo.

## Local Evidence

Paste the commands you ran locally and the result.

```text
Example:
.\scripts\run-ci-checks.ps1 -Scope backend
PASS: uv run ruff check .
PASS: uv run pytest
```

## Risk Review

- User-facing risk:
- CI/CD demo risk:
- Rollback plan:

## Notes For Reviewers

State whether this PR is meant to fail intentionally or is expected to be mergeable.
