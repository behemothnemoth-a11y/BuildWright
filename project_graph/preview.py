from __future__ import annotations
from pathlib import Path

from .model import ProjectPlan, port_for
from .solver import PlacedModule, project_bounds, world_port

def _write_lf(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))

def render_project_svg(plan: ProjectPlan, placed: dict[str, PlacedModule], path: Path):
    x0, y0, z0, x1, y1, z1 = project_bounds(placed.values())
    pad = 6
    width = x1 - x0 + 1 + pad * 2
    height = z1 - z0 + 1 + pad * 2
    scale = 6
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width*scale}" height="{height*scale}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#111318"/>',
        '<g font-family="monospace" font-size="2.5" fill="#e7e9ee">'
    ]
    colors = ["#4d6575", "#70566f", "#5e7054", "#786449", "#52687b", "#6f5555"]
    for index, module in enumerate(placed.values()):
        ox, oy, oz = module.origin
        w, h, depth = module.size
        x = ox - x0 + pad
        z = oz - z0 + pad
        color = colors[index % len(colors)]
        svg.append(f'<rect x="{x}" y="{z}" width="{w}" height="{depth}" fill="{color}" fill-opacity=".45" stroke="{color}" stroke-width=".6"/>')
        svg.append(f'<text x="{x+1}" y="{z+3}">{module.id} y={oy}</text>')

    for connection in plan.connections:
        a_mod = plan.modules[connection.a_module]
        b_mod = plan.modules[connection.b_module]
        a = world_port(placed[a_mod.id].origin, port_for(a_mod, connection.a_port)).pos
        b = world_port(placed[b_mod.id].origin, port_for(b_mod, connection.b_port)).pos
        ax, az = a[0] - x0 + pad, a[2] - z0 + pad
        bx, bz = b[0] - x0 + pad, b[2] - z0 + pad
        dash = ' stroke-dasharray="2,1"' if connection.mode == "corridor" else ""
        svg.append(f'<line x1="{ax}" y1="{az}" x2="{bx}" y2="{bz}" stroke="#e8c36a" stroke-width=".7"{dash}/>')
        svg.append(f'<circle cx="{ax}" cy="{az}" r=".8" fill="#e8c36a"/>')
        svg.append(f'<circle cx="{bx}" cy="{bz}" r=".8" fill="#e8c36a"/>')
    svg.append('</g></svg>')
    _write_lf(path, "\n".join(svg) + "\n")
