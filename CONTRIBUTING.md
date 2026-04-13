# Contributing

## Development setup

```bash
git clone https://github.com/brianpelow/runbook-gen
cd runbook-gen
uv sync
uv run pytest
```

## Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes with tests
4. Run: `uv run ruff check . && uv run pytest`
5. Submit a pull request

## Standards

- All PRs require passing CI
- Test coverage must not decrease
- Update CHANGELOG.md for user-facing changes