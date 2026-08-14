# FinBank Risk Lakehouse v1.0.2 - Verified Security Refresh

## Highlights

- Refreshes the complete locked environment against the current vulnerability database.
- Raises resolver floors for `cryptography`, `GitPython` and `h2` so future lock refreshes cannot reintroduce the patched versions.
- Makes the local SQL lint executable configurable and caps BLAS threads by default for stable macOS imports.
- Isolates environment-doctor imports with a timeout so one dependency cannot block diagnostics indefinitely.
- Runs the consolidated DuckDB release gate before generating the GitHub Actions evidence artifact.

## Verified Scope

The release remains local-first and uses synthetic banking records. DuckDB is the default reviewer path, PostgreSQL is verified in CI, and AWS, Databricks and Snowflake remain documented blueprints rather than deployed environments.

## Security

The release gate audits the full locked dependency graph, including development extras. The release is publishable only when `make security-audit` reports no known vulnerabilities.

## Reproducible Gate

```bash
make clean-demo
AI_DEMO_MODE=1 DB_TARGET=duckdb make demo-local
make release-gate
make evidence-pack
```

## Validation Evidence

The release attachment `evidence.md` records the exact commit, test count, coverage, Rust tests, dbt statuses, replay result, dashboard smoke result and SHA-256 hashes for generated artifacts.

## Scope and Limitations

This is a portfolio release, not a production banking deployment. It does not claim real-customer processing, banking-scale load validation, production SLAs, regulated-model validation or deployed managed-cloud infrastructure.
