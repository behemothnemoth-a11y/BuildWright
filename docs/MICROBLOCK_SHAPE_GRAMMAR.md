# Microblock Shape Grammar

BuildWright ships 40 reusable cell-space primitives in `packs/microblock/primitives.json`.

The grammar is intentionally compositional. Assets call a small number of understandable operations—chamfer, taper, inset, arch curves, mullions, openwork, bosses, brackets, molding profiles—rather than storing opaque one-off cell clouds.

## Rules
- Grid is provider-defined; current Astra profile is 16 cells per axis.
- A primitive must preserve declared sockets/connectors unless explicitly allowed to consume them.
- One-cell features are not texture noise. They require a contour, functional, or focal reason.
- Negative-space primitives must leave structurally legible borders.
- Adjacent-host expansion must be explicit in a translation plan.
- Rotation/mirror must transform geometry and directional material state together.

## Organic shapes
Organic microblock work uses taper, root taper, edge rounding and selective weather chips. Do not convert entire leaf canopies into microcells; keep the large botanical silhouette readable.
