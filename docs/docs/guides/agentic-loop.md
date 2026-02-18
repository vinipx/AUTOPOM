# Agentic Loop

AutoPOM-Agent follows an `Observation -> Thought -> Action` cycle.

## Observation

- Capture compact DOM summary for interactive nodes only.
- Capture current URL, title, and landmarks.
- Capture screenshot or cropped visual hints for ambiguous controls.

## Thought

- Decide highest-value next action:
  - click unvisited internal link,
  - complete auth step,
  - open modal/menu,
  - stop when novelty is low.

## Action

- Execute action with browser adapter.
- Re-compute page signature.
- Persist transition edge and discovered elements.

## Practical safeguards

- Stop when page/action/depth budgets are exhausted.
- Stop when repeated signatures exceed threshold.
- Skip denied/external domains automatically.
