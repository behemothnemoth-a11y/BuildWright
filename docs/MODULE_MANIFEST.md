# Module Manifest

Every composed module receives a manifest beside its `.litematic`.

The manifest records:

- brief and template IDs;
- room bounds;
- style and palette;
- random seed;
- every selected fixture;
- placement target, origin, transform and occupied bounds;
- connectors;
- final block count;
- number of Astra Microblock hosts;
- canonical source path;
- Litematic path and SHA-256;
- independent readback summary;
- warnings;
- maturity and live-game state.

This is provenance, not decoration. It lets later tools answer questions such as:

- Which fixture made this fireplace?
- Which seed produced this room?
- Did a connector move?
- Is this result live-game-tested or only structurally validated?
- Which modules contain Astra hosts?

`OFFLINE_COMPILED / PENDING` must not be silently promoted to tested or approved.
