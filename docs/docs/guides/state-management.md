# State Management

State management is critical for SPAs and dynamic route transitions.

## Page signature model

Each visited state is identified by:

- normalized URL
- compact DOM fingerprint
- semantic landmarks hash

This prevents revisiting equivalent states and controls infinite loops.

## Frontier strategy

- Use queue-based traversal with depth tracking.
- Enqueue only same-origin and non-denied links.
- Preserve `via_action` metadata for diagnostics.

## Edge history

Track transitions as:

`(from_signature, action_type, to_signature)`

This enables:

- loop diagnostics,
- dead-end detection,
- action redundancy filtering.
