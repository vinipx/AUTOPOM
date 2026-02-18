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
    G --> H[Generate POM (Java/JS/TS)]
    H --> I[Persist Output + Report]
    I --> B
```

## Components

- **Navigator:** Executes actions and discovers links.
- **State Store:** Tracks visited signatures and graph edges.
- **Semantic Analyzer:** Converts compact browser context to structured models.
- **Self-Healing Verifier:** Tests and repairs selectors before persistence.
- **POM Synthesizer:** Produces compile-ready Playwright page objects in Java, JavaScript, or TypeScript.

## Design principles

- Token-efficient prompts from compact DOM context.
- Deterministic code generation through schema contracts.
- Guardrails first: domain boundaries, depth limits, and cycle detection.
- Configuration-driven output language with shared semantic model and generation pipeline.
