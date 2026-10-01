# Exterior Envelope and Facade Compiler

The facade pass turns exposed module boundary faces into a coherent building exterior without replacing the module interior.

Current profiles:
- massive_gothic_manor
- classic_manor
- industrial
- modern

The compiler identifies cardinal sides not consumed by direct room attachments, then layers exterior-only depth onto those faces.

## Current operations

- plinth course
- projecting piers and bay rhythm
- boundary-wall window openings
- glazing
- sill and header trim
- cornice band
- connector exclusion zones

Doors, room connections and circulation ports always win over decorative bay rhythm.

This first implementation intentionally uses large readable facade shapes rather than random surface noise.

Future passes can add style-specific gables, buttresses, tracery, balconies, towers and asymmetrical facade zoning through the fixture library.
