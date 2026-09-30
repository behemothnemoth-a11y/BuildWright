# Connectors and Keepouts

Connectors are first-class architecture.

A staircase, portal, door, tunnel or gallery exit that is intended to lead somewhere must not be converted into decorative dead space by fixture placement.

## Wall connector

```json
{
  "id": "west_library",
  "side": "west",
  "center": "50%",
  "width": 5,
  "height": 5,
  "depth": 2,
  "clearance": 4,
  "target": "library-west"
}
```

`depth` is the actual opening depth through the current shell. `clearance` extends the protected interior approach used by the placement planner.

## Guarantees in DROP 0005

1. connector keepouts are built before fixture selection;
2. normal fixtures cannot occupy those keepouts;
3. the actual opening is carved into the shell;
4. connector cells are re-carved after all fixture placement;
5. the connector definition is copied into module source and manifest.

The re-carve step is intentional. A decorative asset can never silently close a declared exit.

## Explicit keepout boxes

Briefs may also provide boxes:

```json
"keepouts": [[10, 1, 0, 16, 6, 8]]
```

The order is `minX,minY,minZ,maxX,maxY,maxZ`.

Use explicit keepouts for central ceremonial axes, player circulation, future staircase branches, vehicle paths, machinery service lanes, or sightline protection.
