# Ledgerline Settlement Audit

Audit tooling and release documentation for the Ledgerline settlement service.

## Layout

- `src/ledgerline/io/` -- ledger ingestion and reader paths
- `src/ledgerline/settlement/` -- rounding and reconciliation helpers
- `docs/` -- audit and release documentation
- `ops/` -- release pipeline definitions

## Release documentation

The verified-fix register for each release train lives in `docs/fix-register.md`.
Entries are appended by the release engineer before the release tag is cut.
