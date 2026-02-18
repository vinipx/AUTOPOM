# Contributing Guidelines

## Principles

- Keep extraction and generation layers decoupled.
- Prefer deterministic transformations over implicit behavior.
- Preserve clean code naming in generated outputs.

## Pull request expectations

- Include tests for new extraction or generation logic.
- Update documentation for new config keys or behavior.
- Avoid introducing brittle selector defaults.

## Local checks

```bash
PYTHONPATH=src python3 -m compileall src
```

If docs are changed:

```bash
cd docs
npm run build
```
