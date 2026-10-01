#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
if str(ROOT/"tools") not in sys.path:
    sys.path.insert(0,str(ROOT/"tools"))

from render_litematic_iso import read_blocks, render_iso

VIS=ROOT/"catalog/visual"
IMAGES=VIS/"images"
MANIFEST=VIS/"visual_manifest.json"
MAIN=ROOT/"VISUAL_CATALOG.md"

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def lf(path,text):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_bytes((text.rstrip()+"\n").encode("utf-8"))

def font(size=16,bold=False):
    candidates=[
      Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
      Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    ]
    for p in candidates:
        if p.is_file():
            return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()

def render_group(folder:Path,target:Path,cutaway=False):
    target.mkdir(parents=True,exist_ok=True)
    rows=[]
    for lit in sorted(folder.glob("*.litematic")):
        manifest=lit.with_suffix(".manifest.json")
        meta=load(manifest) if manifest.is_file() else {}
        ident=meta.get("id",lit.stem)
        out=target/f"{ident}.png"
        result=render_iso(read_blocks(lit),out,cutaway=cutaway)
        rows.append({
          "id":ident,
          "label":meta.get("name",ident.replace("_"," ").title()),
          "source":str(lit.relative_to(ROOT)).replace("\\","/"),
          "image":str(out.relative_to(ROOT)).replace("\\","/"),
          "blocks":meta.get("blocks",result["total_blocks"]),
          "size":meta.get("size"),
          "maturity":meta.get("maturity"),
          "live_game_status":meta.get("live_game_status")
        })
    return rows

def fixture_rows():
    reg=load(ROOT/"fixtures/registry.json")
    rows=[]
    for f in reg["fixtures"]:
        preview=ROOT/f["preview"]
        rows.append({
          "id":f["id"],"label":f["id"].replace("_"," ").title(),
          "stage":f["stage"],"category":f["category"],"family":f["family"],
          "size":f.get("size"),"blocks":f.get("blocks"),
          "source":f["file"],"image":f["preview"],
          "sha256":sha(preview) if preview.is_file() else None
        })
    return rows

def contact_sheet(rows,out_path:Path,cols=4,cell=(310,245),thumb=(286,190)):
    if not rows: return
    rows_n=math.ceil(len(rows)/cols)
    bg=(22,24,28);fg=(232,234,238);muted=(160,166,174)
    sheet=Image.new("RGB",(cols*cell[0],rows_n*cell[1]),bg)
    draw=ImageDraw.Draw(sheet)
    f1=font(16,True);f2=font(12,False)
    for i,row in enumerate(rows):
        cx=(i%cols)*cell[0];cy=(i//cols)*cell[1]
        src=ROOT/row["image"]
        im=Image.open(src).convert("RGB")
        im.thumbnail(thumb,Image.Resampling.LANCZOS)
        ix=cx+(cell[0]-im.width)//2;iy=cy+8
        sheet.paste(im,(ix,iy))
        label=row["label"]
        if len(label)>34: label=label[:31]+"..."
        draw.text((cx+12,cy+204),label,font=f1,fill=fg)
        draw.text((cx+12,cy+224),row["id"],font=f2,fill=muted)
    out_path.parent.mkdir(parents=True,exist_ok=True)
    sheet.save(out_path,optimize=True)

def card_table(rows,image_prefix="",meta_fn=None,cols=3):
    lines=["<table>"]
    for start in range(0,len(rows),cols):
        lines.append("<tr>")
        for row in rows[start:start+cols]:
            meta=meta_fn(row) if meta_fn else ""
            src=image_prefix+row["image"]
            lines.append(
              '<td width="33%" valign="top">'
              f'<img src="{src}" width="100%"><br>'
              f'<b>{row["label"]}</b><br><code>{row["id"]}</code>'
              +(f"<br>{meta}" if meta else "")
              +"</td>"
            )
        if len(rows[start:start+cols])<cols:
            for _ in range(cols-len(rows[start:start+cols])): lines.append("<td></td>")
        lines.append("</tr>")
    lines.append("</table>")
    return "\n".join(lines)

def size_text(v):
    return " × ".join(str(x) for x in v) if v else "—"

def build_pages(fixtures,rooms,projects,styles):
    registry=load(ROOT/"project_graph/style_registry.json")
    style_meta={x["id"]:x for x in registry["profiles"]}
    style_briefs={p.stem:load(p) for p in (ROOT/"examples/style_showcases").glob("*.json")}

    for row in styles:
        raw=row["id"].removeprefix("style_showcase_")
        if raw in style_meta:
            row["label"]=style_meta[raw]["display_name"]
            row["profile_id"]=raw
            row["family"]=style_meta[raw]["family"]
            row["roof"]=style_meta[raw]["default_roof"]
            row["window"]=style_meta[raw]["window_shape"]
        else:
            brief=next((b for b in style_briefs.values() if b.get("id")==row["id"]),{})
            row["label"]=brief.get("name",raw.replace("_"," ").title()).replace("Style Showcase - ","")
            row["profile_id"]=raw
            row["family"]="hybrid"
            row["roof"]="hybrid"
            row["window"]="hybrid"

    vanilla=[x for x in fixtures if x["stage"]=="vanilla"]
    micro=[x for x in fixtures if x["stage"]=="microblock"]

    contact_sheet(vanilla,VIS/"fixture_overview_vanilla.png",cols=4)
    contact_sheet(micro,VIS/"fixture_overview_microblock.png",cols=4)
    contact_sheet(rooms,VIS/"room_overview.png",cols=3)
    contact_sheet(projects,VIS/"project_overview.png",cols=3)
    contact_sheet(styles,VIS/"style_overview.png",cols=4)

    main=[
      "# BuildWright Visual Catalogue","",
      "This is the picture-first catalogue for BuildWright. Fixture cards use the existing compiled-fixture previews. Room, project and style cards use deterministic isometric renders generated from the actual compiled Litematic geometry.","",
      "> The isometric renderer uses simplified material colors. These are exact compiled shapes, not Minecraft screenshots or shader renders.","",
      "## Quick galleries","",
      f"### Styles — {len(styles)} compiled showcases","",
      "![Style overview](catalog/visual/style_overview.png)","",
      "[Browse every style showcase](catalog/visual/styles.md)","",
      f"### Fixtures — {len(fixtures)} compiled fixtures","",
      "![Vanilla fixture overview](catalog/visual/fixture_overview_vanilla.png)","",
      "![Microblock fixture overview](catalog/visual/fixture_overview_microblock.png)","",
      "[Browse every fixture](catalog/visual/fixtures.md)","",
      f"### Room / module examples — {len(rooms)}","",
      "![Room overview](catalog/visual/room_overview.png)","",
      "[Browse rooms and modules](catalog/visual/rooms.md)","",
      f"### Whole-building regression projects — {len(projects)}","",
      "![Project overview](catalog/visual/project_overview.png)","",
      "[Browse whole-building projects](catalog/visual/projects.md)","",
      "## Other catalogues","",
      "- [Full inventory catalogue](CATALOG.md)",
      "- [Machine-readable inventory](catalog/catalog.json)",
      "- [Machine-readable visual manifest](catalog/visual/visual_manifest.json)",""
    ]
    lf(MAIN,"\n".join(main))

    room_page=[
      "# Room & Module Visual Catalogue","",
      "[← Visual Catalogue](../../VISUAL_CATALOG.md)","",
      card_table(rooms,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · {r.get('maturity') or 'offline'}")
    ]
    lf(VIS/"rooms.md","\n".join(room_page))

    project_page=[
      "# Whole-Building Visual Catalogue","",
      "[← Visual Catalogue](../../VISUAL_CATALOG.md)","",
      card_table(projects,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · {r.get('maturity') or 'offline'}")
    ]
    lf(VIS/"projects.md","\n".join(project_page))

    style_page=[
      "# Universal Style Visual Catalogue","",
      "[← Visual Catalogue](../../VISUAL_CATALOG.md)","",
      f"**{len(styles)} compiled style showcases.** The 35 core profiles are project-neutral; two additional cards demonstrate style blending.","",
      card_table(styles,"../../",lambda r:f"{r.get('family','—')} · roof: {r.get('roof','—')} · windows: {r.get('window','—')}")
    ]
    lf(VIS/"styles.md","\n".join(style_page))

    fx=["# Fixture Visual Catalogue","",'[← Visual Catalogue](../../VISUAL_CATALOG.md)',""]
    for stage,items in (("Vanilla",vanilla),("Astra Microblocks",micro)):
        fx += [f"## {stage} — {len(items)} fixtures",""]
        grouped={}
        for item in items:
            grouped.setdefault((item["category"],item["family"]),[]).append(item)
        for (cat,fam),group in sorted(grouped.items()):
            fx += [f"### {cat} · {fam}","",card_table(group,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks"),""]
    lf(VIS/"fixtures.md","\n".join(fx))

def build_manifest(fixtures,rooms,projects,styles):
    return {
      "schema_version":1,
      "generator":"tools/build_visual_catalog.py",
      "fixtures":fixtures,
      "rooms":rooms,
      "projects":projects,
      "styles":styles,
      "counts":{"fixtures":len(fixtures),"rooms":len(rooms),"projects":len(projects),"styles":len(styles)}
    }

def validate_manifest(data):
    missing=[]
    for group in ("fixtures","rooms","projects","styles"):
        for row in data[group]:
            if not (ROOT/row["image"]).is_file(): missing.append(row["image"])
            if not (ROOT/row["source"]).is_file(): missing.append(row["source"])
    for p in (MAIN,VIS/"fixtures.md",VIS/"rooms.md",VIS/"projects.md",VIS/"styles.md",
              VIS/"fixture_overview_vanilla.png",VIS/"fixture_overview_microblock.png",
              VIS/"room_overview.png",VIS/"project_overview.png",VIS/"style_overview.png"):
        if not p.is_file(): missing.append(str(p.relative_to(ROOT)))
    return missing

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()

    if args.check:
        if not MANIFEST.is_file():
            print("VISUAL CATALOG: MISSING MANIFEST");raise SystemExit(1)
        data=load(MANIFEST)
        missing=validate_manifest(data)
        if missing:
            print("VISUAL CATALOG: FAIL",", ".join(missing));raise SystemExit(1)
        expected=load(ROOT/"buildwright.json").get("visual_catalog",{})
        want={"fixtures":expected.get("fixture_previews"),"rooms":expected.get("room_renders"),"projects":expected.get("project_renders"),"styles":expected.get("style_renders")}
        if data.get("counts")!=want:
            print("VISUAL CATALOG: COUNT MISMATCH",data.get("counts"),want);raise SystemExit(1)
        core=set(x["id"] for x in load(ROOT/"project_graph/style_registry.json")["profiles"])
        rendered={x["id"].removeprefix("style_showcase_") for x in data["styles"]}
        absent=sorted(core-rendered)
        if absent:
            print("VISUAL CATALOG: MISSING CORE STYLES",", ".join(absent));raise SystemExit(1)
        print("VISUAL CATALOG: PASS",data["counts"]);return

    fixtures=fixture_rows()
    rooms=render_group(ROOT/"composition/compiled_examples",IMAGES/"rooms",cutaway=True)
    projects=render_group(ROOT/"project_graph/compiled_examples",IMAGES/"projects")
    styles=render_group(ROOT/"project_graph/style_showcases",IMAGES/"styles")
    build_pages(fixtures,rooms,projects,styles)
    data=build_manifest(fixtures,rooms,projects,styles)
    lf(MANIFEST,json.dumps(data,indent=2))
    print("VISUAL CATALOG: WROTE",data["counts"])

if __name__=="__main__":
    main()
