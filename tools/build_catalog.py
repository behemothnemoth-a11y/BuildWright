#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT_JSON=ROOT/"catalog/catalog.json"
OUT_MD=ROOT/"CATALOG.md"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def manifests(folder):
    rows=[]
    for p in sorted(Path(folder).glob("*.manifest.json")):
        d=load(p)
        rows.append({
            "id":d.get("id",p.stem.replace(".manifest","")),
            "size":d.get("size"),
            "blocks":d.get("blocks",d.get("block_count")),
            "modules":d.get("modules"),
            "connections":d.get("connections"),
            "maturity":d.get("maturity"),
            "live_game_status":d.get("live_game_status"),
            "microblock_hosts":int(d.get("microblock_hosts",0) or 0),
            "manifest":str(p.relative_to(ROOT)).replace("\\","/"),
            "litematic":d.get("litematic")
        })
    return rows

def projects():
    rows=[]
    for folder in sorted((ROOT/"projects").iterdir()):
        if not folder.is_dir() or folder.name.startswith("_"):
            continue
        row={"id":folder.name,"project_md":None,"state_md":None,"modules":[]}
        if (folder/"PROJECT.md").is_file():
            row["project_md"]=str((folder/"PROJECT.md").relative_to(ROOT)).replace("\\","/")
        if (folder/"PROJECT_STATE.md").is_file():
            row["state_md"]=str((folder/"PROJECT_STATE.md").relative_to(ROOT)).replace("\\","/")
        if (folder/"module_registry.json").is_file():
            row["modules"]=load(folder/"module_registry.json").get("modules",[])
        rows.append(row)
    return rows
def build_catalog():
    cfg=load(ROOT/"buildwright.json")
    milestones=load(ROOT/"catalog/milestones.json")["milestones"]
    fixtures=load(ROOT/"fixtures/registry.json")
    styles=load(ROOT/"project_graph/style_registry.json")
    composition=manifests(ROOT/"composition/compiled_examples")
    vanilla_composition=[x for x in composition if x.get("microblock_hosts",0)==0]
    optional_microblock_examples=[x for x in composition if x.get("microblock_hosts",0)>0]
    detailed_composition=manifests(ROOT/"composition/detailed_examples")
    whole=manifests(ROOT/"project_graph/compiled_examples")
    detailed_projects=manifests(ROOT/"project_graph/detailed_examples")
    structural_projects=manifests(ROOT/"project_graph/structural_examples")
    style_finish_projects=manifests(ROOT/"project_graph/style_finish_examples")
    showcases=manifests(ROOT/"project_graph/style_showcases")
    groups=defaultdict(list)
    for f in fixtures["fixtures"]:
        groups[f"{f['stage']}:{f['category']}:{f['family']}"].append(f["id"])
    tools=sorted(p.name for p in (ROOT/"tools").iterdir() if p.is_file())
    docs=sorted(p.name for p in (ROOT/"docs").glob("*.md"))
    summary={
        "vanilla_pack_families":cfg["pack_system"]["families"],
        "vanilla_pack_variants":cfg["pack_system"]["assets"],
        "microblock_families":cfg["pack_system"]["microblock_families"],
        "microblock_variants":cfg["pack_system"]["microblock_assets"],
        "microblock_primitives":cfg["pack_system"]["microblock_primitives"],
        "microblock_detail_profiles":cfg["pack_system"]["microblock_detail_profiles"],
        "vanilla_fixtures":fixtures["counts"]["vanilla"],
        "microblock_fixtures":fixtures["counts"]["microblock"],
        "transform_cases":fixtures["counts"]["transform_cases"],
        "composition_templates":cfg["composition_system"]["templates"],
        "composition_palettes":cfg["composition_system"]["palettes"],
        "composition_examples":len(composition),
        "vanilla_composition_examples":len(vanilla_composition),
        "optional_microblock_examples":len(optional_microblock_examples),
        "vanilla_detail_examples":len(detailed_composition),
        "whole_building_examples":len(whole),
        "vanilla_detail_projects":len(detailed_projects),
        "structural_site_projects":len(structural_projects),
        "style_finish_projects":len(style_finish_projects),
        "style_profiles":styles["count"],
        "style_families":len(styles["families"]),
        "style_showcases":len(showcases),
        "tools":len(tools),
        "documentation_pages":len(docs)
    }
    return {
        "schema_version":1,
        "buildwright_version":cfg["version"],
        "minecraft_target":cfg["minecraft"]["primary_target"],
        "summary":summary,
        "milestones":milestones,
        "fixtures":fixtures["fixtures"],
        "fixture_groups":dict(sorted(groups.items())),
        "style_profiles":styles["profiles"],
        "style_families":styles["families"],
        "composition_examples":composition,
        "vanilla_composition_examples":vanilla_composition,
        "optional_microblock_examples":optional_microblock_examples,
        "vanilla_detail_examples":detailed_composition,
        "whole_building_examples":whole,
        "vanilla_detail_projects":detailed_projects,
        "structural_site_projects":structural_projects,
        "style_finish_projects":style_finish_projects,
        "style_showcases":showcases,
        "projects":projects(),
        "tools":tools,
        "documentation":docs
    }

def size_text(size):
    return " x ".join(str(v) for v in size) if size else "-"
def markdown(data):
    s=data["summary"]
    out=[
        "# BuildWright Catalogue","",
        f"Generated inventory of BuildWright {data['buildwright_version']} for Minecraft {data['minecraft_target']}.","",
        "**Want pictures? Open the [BuildWright Visual Catalogue](VISUAL_CATALOG.md).**","",
        "This file is generated by tools/build_catalog.py. Machine-readable data lives in catalog/catalog.json.","",
        "## Vanilla baseline inventory","",
        "**The baseline is vanilla-only. Microblocks are an optional later refinement layer.**","",
        "| Vanilla system | Count |","| --- | ---: |",
        f"| Vanilla pack families | {s['vanilla_pack_families']} |",
        f"| Vanilla pack variants | {s['vanilla_pack_variants']} |",
        f"| Compiled vanilla fixtures | {s['vanilla_fixtures']} |",
        f"| Composition templates | {s['composition_templates']} |",
        f"| Composition palettes | {s['composition_palettes']} |",
        f"| Vanilla room/module baseline examples | {s['vanilla_composition_examples']} |",
        f"| VANILLA_DETAIL_COMPLETE room-role examples | {s['vanilla_detail_examples']} |",
        f"| Vanilla whole-building baseline projects | {s['whole_building_examples']} |",
        f"| VANILLA_DETAIL_COMPLETE whole-building projects | {s['vanilla_detail_projects']} |",
        f"| Structural/site intelligence regression projects | {s['structural_site_projects']} |",
        f"| Style-family finish regression projects | {s['style_finish_projects']} |",
        f"| Universal style profiles | {s['style_profiles']} |",
        f"| Architectural style families | {s['style_families']} |",
        f"| Vanilla style baseline compiles | {s['style_showcases']} |","",
        "## Optional Astra Microblocks refinement inventory","",
        "This is retained for post-vanilla detail work and is **not** part of the base output.","",
        "| Optional refinement system | Count |","| --- | ---: |",
        f"| Microblock families | {s['microblock_families']} |",
        f"| Microblock variants | {s['microblock_variants']} |",
        f"| Microblock primitives | {s['microblock_primitives']} |",
        f"| Microblock detail profiles | {s['microblock_detail_profiles']} |",
        f"| Compiled Astra fixtures | {s['microblock_fixtures']} |",
        f"| Hybrid microblock proof examples | {s['optional_microblock_examples']} |",
        f"| Transform regression cases | {s['transform_cases']} |","",
        "## Repository totals","",
        f"- Command-line/build tools: {s['tools']}",
        f"- Documentation pages: {s['documentation_pages']}","",
        "## Milestones","",
        "| Drop | Version | Name | Status |","| --- | --- | --- | --- |"
    ]
    for m in data["milestones"]:
        out.append(f"| {m['drop']} | {m['version']} | {m['name']} | {m['status']} |")
    out += ["","### Milestone highlights",""]
    for m in data["milestones"]:
        out += [f"**{m['drop']} — {m['name']}**","", "; ".join(m["highlights"]) + ".",""]

    out += ["## Universal style library","",f"{len(data['style_profiles'])} profiles across {len(data['style_families'])} architectural families.",""]
    by_family=defaultdict(list)
    for item in data["style_profiles"]:
        by_family[item["family"]].append(item)
    for family in sorted(by_family):
        names=", ".join(f"{p['id']} ({p['display_name']})" for p in by_family[family])
        out.append(f"- **{family}:** {names}")
    out += ["","Profiles describe architectural language rather than a specific project. Styles can also blend a primary and secondary profile while material-role overrides remain explicit.",""]

    out += ["## Vanilla compiled fixture catalogue",""]
    for key,ids in data["fixture_groups"].items():
        stage,category,family=key.split(":",2)
        if stage!="vanilla":
            continue
        out += [f"### {category} · {family}","",", ".join(ids),""]
    out += ["## Optional Astra fixture catalogue","",
            "Retained for post-vanilla refinement only. These are not part of the baseline build output.",""]
    for key,ids in data["fixture_groups"].items():
        stage,category,family=key.split(":",2)
        if stage!="microblock":
            continue
        out += [f"### {category} · {family}","",", ".join(ids),""]

    return out
def add_manifest_table(out,title,rows,whole=False):
    out += [f"## {title}",""]
    if whole:
        out += ["| ID | Modules | Connections | Size | Blocks | Maturity | Live game |","| --- | ---: | ---: | --- | ---: | --- | --- |"]
        for r in rows:
            out.append(f"| {r['id']} | {r.get('modules') or '-'} | {r.get('connections') or '-'} | {size_text(r.get('size'))} | {r.get('blocks') or '-'} | {r.get('maturity') or '-'} | {r.get('live_game_status') or '-'} |")
    else:
        out += ["| ID | Size | Blocks | Maturity | Live game |","| --- | --- | ---: | --- | --- |"]
        for r in rows:
            out.append(f"| {r['id']} | {size_text(r.get('size'))} | {r.get('blocks') or '-'} | {r.get('maturity') or '-'} | {r.get('live_game_status') or '-'} |")
    out.append("")

def finish_markdown(data,out):
    add_manifest_table(out,"Vanilla room/module baseline examples",data["vanilla_composition_examples"])
    add_manifest_table(out,"VANILLA_DETAIL_COMPLETE room-role examples",data["vanilla_detail_examples"])
    add_manifest_table(out,"Vanilla whole-building regression baselines",data["whole_building_examples"],True)
    add_manifest_table(out,"VANILLA_DETAIL_COMPLETE whole-building projects",data["vanilla_detail_projects"],True)
    add_manifest_table(out,"Structural & site intelligence regressions",data["structural_site_projects"],True)
    add_manifest_table(out,"Style-family vanilla finish regressions",data["style_finish_projects"],True)
    add_manifest_table(out,"Vanilla style baseline compiles",data["style_showcases"])
    if data["optional_microblock_examples"]:
        add_manifest_table(out,"Optional Astra/microblock proof examples",data["optional_microblock_examples"])
    out += ["## Project-specific work tracked in this repo",""]
    for project in data["projects"]:
        out += [f"### {project['id']}",""]
        if project["project_md"]:
            out.append(f"- Project definition: {project['project_md']}")
        if project["state_md"]:
            out.append(f"- Project state: {project['state_md']}")
        for m in project["modules"]:
            artifact=m.get("working_artifact") or m.get("working_brief")
            tail=f" — {artifact}" if artifact else ""
            out.append(f"- {m.get('id')} — {m.get('name')} — **{m.get('state')}**{tail}")
        out.append("")
    out += [
        "## Tooling made so far","",
        ", ".join(data["tools"]),"",
        "## Maturity reminder","",
        "OFFLINE_COMPILED and SERIALIZATION_VALIDATED mean BuildWright has structurally generated and read back an artifact. LIVE_GAME_PENDING means it still needs a real Minecraft/Fabric/Litematica test. REVIEW_CANDIDATE, APPROVED, and MERGED require progressively stronger human and in-game review.",""
    ]
    return "\n".join(out).rstrip()+"\n"

def render_markdown(data):
    return finish_markdown(data,markdown(data))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check",action="store_true")
    args=ap.parse_args()
    data=build_catalog()
    jb=(json.dumps(data,indent=2)+"\n").encode("utf-8")
    mb=render_markdown(data).encode("utf-8")
    if args.check:
        bad=[]
        if not OUT_JSON.is_file() or OUT_JSON.read_bytes()!=jb:
            bad.append(str(OUT_JSON.relative_to(ROOT)))
        if not OUT_MD.is_file() or OUT_MD.read_bytes()!=mb:
            bad.append(str(OUT_MD.relative_to(ROOT)))
        if bad:
            print("CATALOG: MISMATCH",", ".join(bad))
            raise SystemExit(1)
        print("CATALOG: PASS",data["summary"])
        return
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_bytes(jb)
    OUT_MD.write_bytes(mb)
    print("CATALOG: WROTE",data["summary"])

if __name__=="__main__":
    main()
