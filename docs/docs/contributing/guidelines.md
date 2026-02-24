# Contributing Guidelines

## Principles

- Keep extraction and generation layers decoupled.
- Prefer deterministic transformations over implicit behavior.
- Preserve clean code naming in generated outputs.

## Pull request expectations

- Include tests for new extraction or generation logic.
- Update documentation for new config keys or behavior.
- Ensure all linting and formatting checks pass (use `pre-commit`).
- Avoid introducing brittle selector defaults.

## Local checks

### Quality Gates (Pre-commit)

We use `pre-commit` to ensure consistent code quality. Install it once in your local environment:

```bash
pre-commit install
```

To run checks manually on all files:

```bash
pre-commit run --all-files
```

### Manual Syntax Check

```bash
PYTHONPATH=src python3 -m compileall src
```

If docs are changed:

```bash
cd docs
npm run build
```
