# Architecture Overview

## High-level flow

```mermaid
flowchart TD
    A[Base URL + Config] --> B[Observe Page]
    B --> C[Think: Next Action]
    C --> D[Execute Action]
    D --> E[Extract DOM + Visual Hints]
    E --> F[Map Elements + Build JSON PageModel]
    F --> G[Verify/Heal Selectors]
    G --> H[Generate Java POM]
    H --> I[Persist Output + Report]
    I --> B
```

## Components

- **Navigator:** Executes actions and discovers links.
- **State Store:** Tracks visited signatures and graph edges.
- **Semantic Analyzer:** Converts compact browser context to structured models.
- **Self-Healing Verifier:** Tests and repairs selectors before persistence.
- **Java Synthesizer:** Produces compile-ready Java Playwright page objects.

## Design principles

- Token-efficient prompts from compact DOM context.
- Deterministic code generation through schema contracts.
- Guardrails first: domain boundaries, depth limits, and cycle detection.
