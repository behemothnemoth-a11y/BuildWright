# Microblock Performance and Complexity Budgets

BuildWright budgets are conservative design guardrails, not engine hard limits.

## Budget dimensions
- number of converted hosts;
- materials per host;
- disconnected components per host;
- one-cell features;
- TIER 4 share;
- simultaneous visible dense modules.

Start large builds with `performance_guarded`. Escalate only locally. Astra 0.4.0 uses greedy face merging and cached shapes, but that is not permission to convert every block. Geometry still has memory, mesh, collision/selection and visual-complexity cost.

## Visual budget
Performance is only half the problem. Dense microgeometry can make a room unreadable long before it makes the client slow. If everything has a contour, nothing is a focal point.
