# Sync standalone repository

- [x] Mirror the corrected skill, scripts, references, metadata, and tests.
- [x] Correct stale examples and remove unverified platform and timing claims.
- [x] Run local validation and security checks.
- [x] Review the complete diff.
- [x] Prepare the reviewed branch for PR delivery.

## Review note

The standalone package now carries the same deterministic decoder, fail-open
hook, documentation, metadata, and regression coverage as the collection. The
test path was made repository-relative so it also runs in GitHub Actions.
