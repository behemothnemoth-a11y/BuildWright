# Composition Compiler

DROP 0005 adds BuildWright's first deterministic room/module composition layer.

It is not an AI that invents architecture from nothing. It is a bounded compiler that combines:

- a room/module brief;
- an approved composition template;
- the compiled fixture library from DROP 0004;
- style-profile weights;
- palette remapping;
- connector and circulation keepouts;
- deterministic variation;
- collision checks;
- the BuildWright Litematic exporter.

The output is an editable canonical module source, a manifest, a top-down SVG plan, and a loadable `.litematic`.

## Pipeline

```text
composition brief
  -> template
  -> style + palette
  -> fixture candidate scoring
  -> deterministic slot selection
  -> connector / keepout reservation
  -> collision-safe fixture placement
  -> shell construction
  -> fixture transform + palette remap
  -> authoritative connector re-carve
  -> canonical module source
  -> Litematic export
  -> independent readback
  -> manifest + plan preview
```

## Commands

Plan without compiling:

```powershell
python tools/plan_composition.py examples/composition/gothic_library_demo.json `
  --json .buildwright/generated/library-plan.json `
  --svg .buildwright/generated/library-plan.svg
```

Compile:

```powershell
python tools/compile_module.py examples/composition/gothic_library_demo.json `
  --output-dir .buildwright/generated/library
```

Create a starter brief:

```powershell
python tools/new_room_brief.py my_library --template library --size 45,15,33
```

## Deliberate limitations

DROP 0005 does not claim to solve freeform reference reconstruction, final facade design, redstone behavior, or real-time Axiom placement. It composes tested parts into a bounded module and preserves enough provenance to refine the result manually or in later compiler stages.

Every compiled module remains `LIVE_GAME_PENDING` until it is actually loaded and reviewed in Minecraft.


## Cross-platform deterministic text

Committed composition example JSON and SVG files are canonical UTF-8 with LF line endings.
Compiler code writes those artifacts as bytes rather than platform-translated text, and `.gitattributes` pins the committed example outputs to LF. Byte-for-byte recompilation remains a required validation gate on Windows and Linux.
