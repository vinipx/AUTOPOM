---
sidebar_position: 1
---

# AutoPOM-Agent Documentation

AutoPOM-Agent is an AI autonomous spider that crawls web applications and generates Playwright Page Object Models in Java, JavaScript, or TypeScript.

## What you will find here

- **Configuration** to run controlled crawls and manage credentials.
- **Architecture** covering the agentic loop, state graph, and synthesis pipeline.
- **Core guides** for selector mapping, self-healing, and multi-language POM output strategy.
- **Tutorials** for first runs and authenticated exploration.
- **Use cases** for practical implementation patterns in enterprise contexts.

## Core workflow

1. Start with a base URL.
2. Agent observes and decides next action.
3. Interactive elements are extracted and semantically named.
4. Selectors are validated and healed.
5. POM code is generated from structured JSON page models in the selected language.

## What's new

- Configurable `pom_language` with support for `java`, `javascript`, and `typescript`.
- Language-specific output folders under `output/<language>/`.
- Extended integration and unit tests validating language selection behavior.
