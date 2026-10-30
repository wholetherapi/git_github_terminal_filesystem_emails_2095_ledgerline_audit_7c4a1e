# Verified Fix Register

Every production fix that ships with a release train is listed here.
Append new rows at the end of the `Verified Fixes` section; do not reorder or edit existing rows.

## Verified Fixes

- **src/ledgerline/io/ledger_reader.py** — Add shard-aware batching to the ledger reader — d2c451f58481eee7e91a30bc80da47d58d5b83f6 — Ana Petrova <a.petrova@ledgerline.dev>
- **src/ledgerline/io/timeout_guard.py** — Harden ledger reader timeout handling — cfc0eed924b65e9cc2fcf4e51bb6292217ac4c4f — Priya Deshmukh <p.deshmukh@ledgerline.dev>
- **src/ledgerline/settlement/rounding.py** — Normalise minor-unit rounding for zero-decimal currencies — 7522d793678c05bd5fa1c22e2868aea1f6b29596 — Ravi Menon <r.menon@ledgerline.dev>

## Notes

- Row format: `- **path** — subject — full commit SHA — author name <author email>`
- Only fixes present on the release branch may be listed for that train.
