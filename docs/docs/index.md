---
sidebar_position: 1
---

# AutoPOM-Agent Documentation

AutoPOM-Agent is an AI autonomous spider that crawls web applications and generates Java Playwright Page Object Models.

## What you will find here

- **Configuration** to run controlled crawls and manage credentials.
- **Architecture** covering the agentic loop, state graph, and synthesis pipeline.
- **Core guides** for selector mapping, self-healing, and Java output strategy.
- **Tutorials** for first runs and authenticated exploration.
- **Use cases** for practical implementation patterns in enterprise contexts.

## Core workflow

1. Start with a base URL.
2. Agent observes and decides next action.
3. Interactive elements are extracted and semantically named.
4. Selectors are validated and healed.
5. Java POM code is generated from structured JSON page models.
