from __future__ import annotations
from html import escape
from pathlib import Path
from .geometry import Box

def render_plan_svg(plan, path:Path, scale:int=10):
    W,H,D=plan.room_size; pad=28; width=W*scale+pad*2;height=D*scale+pad*2
    def rx(x):return pad+x*scale
    def rz(z):return pad+z*scale
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<rect width="100%" height="100%" fill="#16181c"/>',
         f'<rect x="{pad}" y="{pad}" width="{W*scale}" height="{D*scale}" fill="#292d33" stroke="#d8d8d8" stroke-width="2"/>']
    for k in plan.keepouts:
        out.append(f'<rect x="{rx(k.min_x)}" y="{rz(k.min_z)}" width="{(k.max_x-k.min_x+1)*scale}" height="{(k.max_z-k.min_z+1)*scale}" fill="#3d5961" opacity="0.38" stroke="#6fb3c3"/>')
    palette=['#745f8f','#8b6652','#5d7c66','#826c44','#526f8a','#8a5b72','#6c6c87','#77714e']
    for i,p in enumerate(plan.placements):
        b=p.box;c=palette[i%len(palette)]
        out.append(f'<rect x="{rx(b.min_x)}" y="{rz(b.min_z)}" width="{(b.max_x-b.min_x+1)*scale}" height="{(b.max_z-b.min_z+1)*scale}" fill="{c}" opacity="0.72" stroke="#e5e5e5" stroke-width="1"/>')
        label=escape(p.fixture_id)
        out.append(f'<text x="{rx(b.min_x)+3}" y="{rz(b.min_z)+12}" font-family="monospace" font-size="9" fill="white">{label}</text>')
    out.append(f'<text x="{pad}" y="18" font-family="sans-serif" font-size="13" fill="white">{escape(plan.brief_id)} — top-down composition plan</text>')
    out.append('</svg>')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(('\n'.join(out)).encode('utf-8'))
