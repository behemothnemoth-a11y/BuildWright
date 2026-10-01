from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from composition.geometry import resolve_coord
from composition.transforms import transform_direction, transform_pos, transformed_size
from .style import resolve_style

Vec3 = tuple[int, int, int]
CARDINAL = {"north", "south", "east", "west"}
VERTICAL = {"up", "down"}

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

@dataclass(frozen=True)
class Port:
    id: str
    side: str
    pos: Vec3
    width: int = 3
    height: int = 4
    depth: int = 1
    clearance: int = 3

    def translated(self, origin: Vec3) -> "Port":
        ox, oy, oz = origin
        x, y, z = self.pos
        return Port(self.id, self.side, (x + ox, y + oy, z + oz), self.width, self.height, self.depth, self.clearance)
@dataclass
class ModuleSpec:
    id: str
    source_path: Path
    source: dict[str, Any]
    rotation: int = 0
    mirror: str = "none"
    origin: Vec3 | None = None
    ports: dict[str, Port] = field(default_factory=dict)

    @property
    def source_size(self) -> Vec3:
        return tuple(int(v) for v in self.source["size"])

    @property
    def size(self) -> Vec3:
        return transformed_size(self.source_size, self.rotation)

@dataclass(frozen=True)
class Connection:
    a_module: str
    a_port: str
    b_module: str
    b_port: str
    mode: str = "attach"
    gap: int = 0
    width: int | None = None
    height: int | None = None

@dataclass
class ProjectPlan:
    id: str
    modules: dict[str, ModuleSpec]
    connections: list[Connection]
    facade_profile: dict[str, Any]
    roof: dict[str, Any]
    site: dict[str, Any]
    warnings: list[str] = field(default_factory=list)
def _connector_port(conn: dict[str, Any], size: Vec3) -> Port:
    w, h, d = size
    side = str(conn.get("side", "south")).lower()
    y = int(conn.get("y", 1))
    width = int(conn.get("width", 3))
    height = int(conn.get("height", 4))
    depth = int(conn.get("depth", 1))
    clearance = int(conn.get("clearance", 3))
    if side in ("north", "south"):
        x = resolve_coord(conn.get("center", "center"), w)
        z = 0 if side == "north" else d - 1
    elif side in ("west", "east"):
        z = resolve_coord(conn.get("center", "center"), d)
        x = 0 if side == "west" else w - 1
    else:
        raise ValueError(f"composition connector side must be cardinal, got {side}")
    return Port(str(conn["id"]), side, (x, y, z), width, height, depth, clearance)

def _explicit_port(data: dict[str, Any]) -> Port:
    pos = tuple(int(v) for v in data["pos"])
    side = str(data["side"]).lower()
    if side not in CARDINAL | VERTICAL:
        raise ValueError(f"Unsupported port side: {side}")
    return Port(str(data["id"]), side, pos, int(data.get("width", 3)), int(data.get("height", 4)), int(data.get("depth", 1)), int(data.get("clearance", 3)))
def transform_port(port: Port, source_size: Vec3, rotation: int, mirror: str) -> Port:
    pos = transform_pos(port.pos, source_size, rotation, mirror)
    side = port.side if port.side in VERTICAL else transform_direction(port.side, rotation, mirror)
    return Port(port.id, side, pos, port.width, port.height, port.depth, port.clearance)

def load_module(root: Path, entry: dict[str, Any]) -> ModuleSpec:
    source_path = root / entry["source"]
    source = load_json(source_path)
    rotation = int(entry.get("rotation", 0)) % 4
    mirror = str(entry.get("mirror", "none"))
    source_size = tuple(int(v) for v in source["size"])
    ports: dict[str, Port] = {}
    for conn in source.get("connectors", []):
        p = _connector_port(conn, source_size)
        p = transform_port(p, source_size, rotation, mirror)
        ports[p.id] = p
    for raw in entry.get("ports", []):
        p = _explicit_port(raw)
        p = transform_port(p, source_size, rotation, mirror)
        ports[p.id] = p
    origin = tuple(int(v) for v in entry["origin"]) if "origin" in entry else None
    return ModuleSpec(str(entry["id"]), source_path, source, rotation, mirror, origin, ports)

def load_project(root: Path, brief: dict[str, Any] | Path) -> ProjectPlan:
    if isinstance(brief, Path):
        brief = load_json(brief)
    modules = {m["id"]: load_module(root, m) for m in brief["modules"]}
    connections = []
    for c in brief.get("connections", []):
        a = c["from"]
        b = c["to"]
        connections.append(Connection(str(a[0]), str(a[1]), str(b[0]), str(b[1]), str(c.get("mode", "attach")), int(c.get("gap", 0)), c.get("width"), c.get("height")))
    facade = resolve_style(root, brief)
    roof = dict(brief.get("roof", {}))
    roof.setdefault("style", facade.get("default_roof", "gable"))
    roof.setdefault("state", facade.get("roof_state", "minecraft:dark_oak_planks"))
    roof.setdefault("gable_state", facade.get("gable_state", facade.get("wall_state", "minecraft:stone_bricks")))
    roof.setdefault("step_run", int(facade.get("roof_step_run", 2)))
    roof.setdefault("overhang", int(facade.get("roof_overhang", 1)))
    site = dict(brief.get("site", {}))
    site.setdefault("character", facade.get("site_character", "generic"))
    site.setdefault("vegetation_profile", facade.get("vegetation_profile", "temperate"))
    return ProjectPlan(str(brief["id"]), modules, connections, facade, roof, site)

def port_for(module: ModuleSpec, port_id: str) -> Port:
    try:
        return module.ports[port_id]
    except KeyError:
        raise KeyError(f"Module {module.id!r} has no port {port_id!r}") from None
