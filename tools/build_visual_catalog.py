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
          "live_game_status":meta.get("live_game_status"),
          "microblock_hosts":int(meta.get("microblock_hosts",0) or 0)
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

def build_pages(fixtures,rooms,projects,styles,detailed_rooms,detailed_projects,structural_projects,style_finish_projects):
    registry=load(ROOT/"project_graph/style_registry.json")
    style_meta={x["id"]:x for x in registry["profiles"]}
    style_briefs={p.stem:load(p) for p in (ROOT/"examples/style_showcases").glob("*.json")}

    for row in styles:
        raw=row["id"].removeprefix("style_showcase_")
        row["detail_level"]="VANILLA_STYLE_BASELINE"
        row["uses_astra_microblocks"]=False
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
            row["family"]="hybrid_style"
            row["roof"]="hybrid"
            row["window"]="hybrid"

    vanilla_fixtures=[x for x in fixtures if x["stage"]=="vanilla"]
    micro_fixtures=[x for x in fixtures if x["stage"]=="microblock"]
    vanilla_rooms=[x for x in rooms if x.get("microblock_hosts",0)==0]
    hybrid_rooms=[x for x in rooms if x.get("microblock_hosts",0)>0]
    for row in vanilla_rooms:
        row["detail_level"]="VANILLA_BASELINE"
        row["uses_astra_microblocks"]=False
    for row in hybrid_rooms:
        row["detail_level"]="OPTIONAL_MICROBLOCK_REFINEMENT"
        row["uses_astra_microblocks"]=True
    for row in projects:
        row["detail_level"]="VANILLA_BASELINE"
        row["uses_astra_microblocks"]=False
    for row in detailed_rooms:
        row["detail_level"]="VANILLA_DETAIL_COMPLETE"
        row["uses_astra_microblocks"]=False
    for row in detailed_projects:
        row["detail_level"]="VANILLA_DETAIL_COMPLETE"
        row["uses_astra_microblocks"]=False
    for row in structural_projects:
        row["detail_level"]="VANILLA_DETAIL_COMPLETE"
        row["uses_astra_microblocks"]=False
    for row in style_finish_projects:
        row["detail_level"]="VANILLA_STYLE_FINISH_COMPLETE"
        row["uses_astra_microblocks"]=False

    contact_sheet(vanilla_fixtures,VIS/"fixture_overview_vanilla.png",cols=4)
    contact_sheet(micro_fixtures,VIS/"fixture_overview_microblock.png",cols=4)
    contact_sheet(vanilla_rooms,VIS/"room_overview.png",cols=3)
    contact_sheet(projects,VIS/"project_overview.png",cols=3)
    contact_sheet(detailed_rooms,VIS/"detail_room_overview.png",cols=3)
    contact_sheet(detailed_projects,VIS/"detail_project_overview.png",cols=3)
    contact_sheet(structural_projects,VIS/"structural_site_overview.png",cols=3)
    contact_sheet(style_finish_projects,VIS/"style_finish_overview.png",cols=4)
    contact_sheet(styles,VIS/"style_overview.png",cols=4)

    main=[
      "# BuildWright Vanilla Visual Catalogue","",
      "**This main catalogue is the vanilla foundation. Astra Microblocks are not part of the baseline shown here.**","",
      "The style cards are **style-language baselines**: massing, materials, facade rhythm, windows, and roof language. They are not the completed vanilla detail layer and should not be read as finished builds.","",
      "Pipeline: **vanilla base → complete vanilla architecture/detail/furnishing → in-game review → optional Astra Microblocks refinement**.","",
      "> Isometric images are deterministic renders of the actual compiled Litematic geometry using simplified material colors. They are not Minecraft screenshots or concept art.","",
      "## Vanilla Detail Complete","",
      f"### {len(detailed_rooms)} completed room-role examples + {len(detailed_projects)} completed whole-building regressions","",
      "![Vanilla detail rooms](catalog/visual/detail_room_overview.png)","",
      "![Vanilla detail projects](catalog/visual/detail_project_overview.png)","",
      "[Browse VANILLA_DETAIL_COMPLETE examples](catalog/visual/vanilla_detail.md)","",
      "## Structural & Site Intelligence","",
      f"### {len(structural_projects)} project-scale circulation / structure / site regressions","",
      "![Structural & site projects](catalog/visual/structural_site_overview.png)","",
      "[Browse structural & site regressions](catalog/visual/structural_site.md)","",
      "## Style-Family Vanilla Finish","",
      f"### {len(style_finish_projects)} family-specific finishing regressions","",
      "![Style finish projects](catalog/visual/style_finish_overview.png)","",
      "[Browse style-family finish regressions](catalog/visual/style_finish.md)","",
      "## Vanilla style baselines","",
      f"### {len(styles)} compiled baselines — 35 core styles + 2 style-blend demonstrations","",
      "![Style overview](catalog/visual/style_overview.png)","",
      "[Browse vanilla style baselines](catalog/visual/styles.md)","",
      "## Vanilla fixture library","",
      f"### {len(vanilla_fixtures)} compiled vanilla fixtures","",
      "![Vanilla fixture overview](catalog/visual/fixture_overview_vanilla.png)","",
      "[Browse vanilla fixtures](catalog/visual/fixtures.md)","",
      "## Vanilla room / module baselines","",
      f"### {len(vanilla_rooms)} vanilla examples","",
      "![Room overview](catalog/visual/room_overview.png)","",
      "[Browse vanilla rooms and modules](catalog/visual/rooms.md)","",
      "## Vanilla whole-building baselines","",
      f"### {len(projects)} regression projects","",
      "![Project overview](catalog/visual/project_overview.png)","",
      "[Browse vanilla whole-building projects](catalog/visual/projects.md)","",
      "## Optional detail layer — deliberately separate","",
      f"The retained Astra layer currently contains **{len(micro_fixtures)} microblock fixtures** and **{len(hybrid_rooms)} hybrid room example**. It is not the default BuildWright output.","",
      "[Open the optional Astra Microblocks catalogue](MICROBLOCK_CATALOG.md)","",
      "## Other catalogues","",
      "- [Full inventory and history](CATALOG.md)",
      "- [Machine-readable inventory](catalog/catalog.json)",
      "- [Machine-readable visual manifest](catalog/visual/visual_manifest.json)",""
    ]
    lf(MAIN,"\n".join(main))

    room_page=[
      "# Vanilla Room & Module Baselines","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      "> These are vanilla compiler baselines, not the complete finished vanilla-detail layer.","",
      card_table(vanilla_rooms,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · VANILLA BASELINE")
    ]
    lf(VIS/"rooms.md","\n".join(room_page))

    project_page=[
      "# Vanilla Whole-Building Baselines","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      "> These whole-building renders are vanilla regression baselines. They still require deeper vanilla detailing and in-game review.","",
      card_table(projects,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · VANILLA BASELINE")
    ]
    lf(VIS/"projects.md","\n".join(project_page))

    detail_page=[
      "# Vanilla Detail Complete","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      "**These examples have passed the automated vanilla finishing pipeline.** They include secondary architecture, furnishing, lighting, vegetation/service detail, and controlled storytelling without Astra Microblocks.","",
      "> VANILLA_DETAIL_COMPLETE is still an offline compiler maturity label. It does not replace in-game player-eye review.","",
      "## Detailed rooms / role regressions","",
      card_table(detailed_rooms,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · VANILLA_DETAIL_COMPLETE"),"",
      "## Detailed whole-building regressions","",
      card_table(detailed_projects,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · VANILLA_DETAIL_COMPLETE"),""
    ]
    lf(VIS/"vanilla_detail.md","\n".join(detail_page))

    structural_page=[
      "# Structural & Site Intelligence","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      "**These vanilla projects exercise project-scale circulation, structure and site systems.** Routed corridors, elevation stairs, towers/porches/balconies/buttresses, foundations, roads/plazas/walls/fences/retaining walls are all compiled geometry.","",
      "> These remain offline regression projects and still require in-game/player-eye review.","",
      card_table(structural_projects,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · STRUCTURAL/SITE REGRESSION")
    ]
    lf(VIS/"structural_site.md","\n".join(structural_page))

    style_finish_page=[
      "# Style-Family Vanilla Finish","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      "**These projects exercise one dedicated finishing grammar for each architectural family.** They extend VANILLA_DETAIL_COMPLETE with family-specific exterior rhythm, eaves, corner structure, lighting, planting, service runs, parapets and finials.","",
      "> These are deterministic pure-vanilla regression outputs and remain LIVE_GAME_PENDING until in-game review.","",
      card_table(style_finish_projects,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks · STYLE-FAMILY FINISH")
    ]
    lf(VIS/"style_finish.md","\n".join(style_finish_page))

    style_page=[
      "# Vanilla Style Baselines","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      f"**{len(styles)} compiled vanilla style baselines.** The 35 core profiles are project-neutral; two additional cards demonstrate style blending.","",
      "> These establish architectural language only. They are intentionally earlier than the complete vanilla detail/furnishing pass.","",
      card_table(styles,"../../",lambda r:f"{r.get('family','—')} · roof: {r.get('roof','—')} · windows: {r.get('window','—')} · VANILLA BASELINE")
    ]
    lf(VIS/"styles.md","\n".join(style_page))

    fx=["# Vanilla Fixture Visual Catalogue","",'[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)',"",
        f"**{len(vanilla_fixtures)} vanilla fixtures.** Astra fixtures are intentionally excluded from this baseline catalogue.",""]
    grouped={}
    for item in vanilla_fixtures:
        grouped.setdefault((item["category"],item["family"]),[]).append(item)
    for (cat,fam),group in sorted(grouped.items()):
        fx += [f"### {cat} · {fam}","",card_table(group,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('blocks') or '—'} blocks"),""]
    lf(VIS/"fixtures.md","\n".join(fx))

    micro_page=[
      "# Optional Astra Microblocks Detail Layer","",
      "[← Vanilla Visual Catalogue](../../VISUAL_CATALOG.md)","",
      "**This is not the BuildWright base layer.** These assets are retained for optional post-vanilla refinement after the vanilla build is complete and reviewed.","",
      f"## Astra fixture library — {len(micro_fixtures)} fixtures","",
      "![Astra fixture overview](fixture_overview_microblock.png)",""
    ]
    grouped={}
    for item in micro_fixtures:
        grouped.setdefault((item["category"],item["family"]),[]).append(item)
    for (cat,fam),group in sorted(grouped.items()):
        micro_page += [f"### {cat} · {fam}","",card_table(group,"../../",lambda r:f"{size_text(r.get('size'))} · optional microblock detail"),""]
    if hybrid_rooms:
        micro_page += ["## Hybrid proof-of-concept room","",
                       "> This room exists to test the optional refinement pipeline. It is not part of the vanilla baseline catalogue.","",
                       card_table(hybrid_rooms,"../../",lambda r:f"{size_text(r.get('size'))} · {r.get('microblock_hosts')} Astra hosts · OPTIONAL REFINEMENT"),""]
    lf(VIS/"microblocks.md","\n".join(micro_page))

    micro_root=[
      "# BuildWright Optional Microblock Catalogue","",
      "**Astra Microblocks are an optional refinement layer, not the base BuildWright output.**","",
      "The authoritative workflow is vanilla-first: finish the architecture, vanilla detailing, furnishing and player-eye review before deciding whether any local contour/detail benefits from microblocks.","",
      "![Astra fixture overview](catalog/visual/fixture_overview_microblock.png)","",
      "[Browse the optional detail-layer assets](catalog/visual/microblocks.md)","",
      "[Return to the vanilla visual catalogue](VISUAL_CATALOG.md)",""
    ]
    lf(ROOT/"MICROBLOCK_CATALOG.md","\n".join(micro_root))

    return vanilla_fixtures,micro_fixtures,vanilla_rooms,hybrid_rooms,detailed_rooms,detailed_projects,structural_projects,style_finish_projects

def build_manifest(fixtures,rooms,projects,styles,detailed_rooms,detailed_projects,structural_projects,style_finish_projects):
    vanilla_fixtures,micro_fixtures,vanilla_rooms,hybrid_rooms,detailed_rooms,detailed_projects,structural_projects,style_finish_projects=build_pages(fixtures,rooms,projects,styles,detailed_rooms,detailed_projects,structural_projects,style_finish_projects)
    return {
      "schema_version":4,
      "generator":"tools/build_visual_catalog.py",
      "vanilla":{
        "fixtures":vanilla_fixtures,
        "rooms":vanilla_rooms,
        "projects":projects,
        "style_baselines":styles,
        "detail_complete_rooms":detailed_rooms,
        "detail_complete_projects":detailed_projects,
        "structural_site_projects":structural_projects,
        "style_finish_projects":style_finish_projects
      },
      "optional_microblock":{
        "fixtures":micro_fixtures,
        "hybrid_rooms":hybrid_rooms
      },
      "counts":{
        "vanilla_fixtures":len(vanilla_fixtures),
        "vanilla_rooms":len(vanilla_rooms),
        "vanilla_projects":len(projects),
        "vanilla_style_baselines":len(styles),
        "vanilla_detail_rooms":len(detailed_rooms),
        "vanilla_detail_projects":len(detailed_projects),
        "structural_site_projects":len(structural_projects),
        "style_finish_projects":len(style_finish_projects),
        "microblock_fixtures":len(micro_fixtures),
        "hybrid_rooms":len(hybrid_rooms)
      }
    }

def validate_manifest(data):
    missing=[]
    groups=[
      data["vanilla"]["fixtures"],data["vanilla"]["rooms"],data["vanilla"]["projects"],data["vanilla"]["style_baselines"],
      data["vanilla"]["detail_complete_rooms"],data["vanilla"]["detail_complete_projects"],
      data["vanilla"]["structural_site_projects"],data["vanilla"]["style_finish_projects"],
      data["optional_microblock"]["fixtures"],data["optional_microblock"]["hybrid_rooms"]
    ]
    for rows in groups:
        for row in rows:
            if not (ROOT/row["image"]).is_file(): missing.append(row["image"])
            if not (ROOT/row["source"]).is_file(): missing.append(row["source"])
    for p in (MAIN,ROOT/"MICROBLOCK_CATALOG.md",VIS/"fixtures.md",VIS/"rooms.md",VIS/"projects.md",VIS/"styles.md",VIS/"microblocks.md",VIS/"vanilla_detail.md",VIS/"structural_site.md",VIS/"style_finish.md",
              VIS/"fixture_overview_vanilla.png",VIS/"fixture_overview_microblock.png",
              VIS/"room_overview.png",VIS/"project_overview.png",VIS/"detail_room_overview.png",VIS/"detail_project_overview.png",VIS/"structural_site_overview.png",VIS/"style_finish_overview.png",VIS/"style_overview.png"):
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
        want={
          "vanilla_fixtures":expected.get("vanilla_fixture_previews"),
          "vanilla_rooms":expected.get("vanilla_room_renders"),
          "vanilla_projects":expected.get("vanilla_project_renders"),
          "vanilla_style_baselines":expected.get("vanilla_style_baselines"),
          "vanilla_detail_rooms":expected.get("vanilla_detail_room_renders"),
          "vanilla_detail_projects":expected.get("vanilla_detail_project_renders"),
          "structural_site_projects":expected.get("structural_site_renders"),
          "style_finish_projects":expected.get("style_finish_renders"),
          "microblock_fixtures":expected.get("microblock_fixture_previews"),
          "hybrid_rooms":expected.get("hybrid_room_renders")
        }
        if data.get("counts")!=want:
            print("VISUAL CATALOG: COUNT MISMATCH",data.get("counts"),want);raise SystemExit(1)
        vanilla_rows=(data["vanilla"]["rooms"]+data["vanilla"]["projects"]+data["vanilla"]["style_baselines"]+
                      data["vanilla"]["detail_complete_rooms"]+data["vanilla"]["detail_complete_projects"]+
                      data["vanilla"]["structural_site_projects"]+data["vanilla"]["style_finish_projects"])
        if any(x.get("uses_astra_microblocks") for x in vanilla_rows):
            print("VISUAL CATALOG: ASTRA LEAKED INTO VANILLA OUTPUT");raise SystemExit(1)
        core=set(x["id"] for x in load(ROOT/"project_graph/style_registry.json")["profiles"])
        rendered={x["id"].removeprefix("style_showcase_") for x in data["vanilla"]["style_baselines"]}
        absent=sorted(core-rendered)
        if absent:
            print("VISUAL CATALOG: MISSING CORE STYLES",", ".join(absent));raise SystemExit(1)
        print("VISUAL CATALOG: PASS",data["counts"]);return

    fixtures=fixture_rows()
    rooms=render_group(ROOT/"composition/compiled_examples",IMAGES/"rooms",cutaway=True)
    projects=render_group(ROOT/"project_graph/compiled_examples",IMAGES/"projects")
    styles=render_group(ROOT/"project_graph/style_showcases",IMAGES/"styles")
    detailed_rooms=render_group(ROOT/"composition/detailed_examples",IMAGES/"detailed_rooms",cutaway=True)
    detailed_projects=render_group(ROOT/"project_graph/detailed_examples",IMAGES/"detailed_projects")
    structural_projects=render_group(ROOT/"project_graph/structural_examples",IMAGES/"structural_site")
    style_finish_projects=render_group(ROOT/"project_graph/style_finish_examples",IMAGES/"style_finish")
    data=build_manifest(fixtures,rooms,projects,styles,detailed_rooms,detailed_projects,structural_projects,style_finish_projects)
    lf(MANIFEST,json.dumps(data,indent=2))
    print("VISUAL CATALOG: WROTE",data["counts"])

if __name__=="__main__":
    main()
