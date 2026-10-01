from __future__ import annotations
from copy import deepcopy
from typing import Any

from .model import ProjectPlan, port_for
from .solver import PlacedModule, project_bounds, world_port

Vec3=tuple[int,int,int]

def inject_reference_origins(brief:dict[str,Any])->dict[str,Any]:
    cfg=brief.get("reference_fit",{})
    if not cfg.get("enabled",False) or not cfg.get("apply_module_origins",False):
        return brief
    out=deepcopy(brief)
    targets={str(x["module"]):x for x in cfg.get("module_targets",[]) if "origin" in x}
    for module in out.get("modules",[]):
        target=targets.get(str(module["id"]))
        if target is not None and "origin" not in module:
            module["origin"]=[int(v) for v in target["origin"]]
    return out

def _max_abs(a,b):
    return max(abs(int(a[i])-int(b[i])) for i in range(min(len(a),len(b))))

def evaluate_reference_fit(plan:ProjectPlan,placed:dict[str,PlacedModule],brief:dict[str,Any]):
    cfg=dict(brief.get("reference_fit",{}))
    if not cfg.get("enabled",False):
        return {"enabled":False,"status":"DISABLED"}

    default_tol=max(0,int(cfg.get("tolerance",1)))
    strict=bool(cfg.get("strict",False))
    errors=[]
    checks=0
    max_error=0
    details=[]

    bounds=project_bounds(placed.values())
    actual_size=[bounds[3]-bounds[0]+1,bounds[4]-bounds[1]+1,bounds[5]-bounds[2]+1]
    if "target_size" in cfg:
        target=[int(v) for v in cfg["target_size"]]
        tol=max(0,int(cfg.get("size_tolerance",default_tol)))
        err=_max_abs(actual_size,target);checks+=1;max_error=max(max_error,err)
        details.append({"type":"project_size","target":target,"actual":actual_size,"error":err,"tolerance":tol})
        if err>tol:errors.append(f"project size error {err} > {tol}: actual={actual_size} target={target}")

    for item in cfg.get("module_targets",[]):
        mid=str(item["module"])
        if mid not in placed:
            errors.append(f"reference module target missing module {mid}");continue
        m=placed[mid];tol=max(0,int(item.get("tolerance",default_tol)))
        if "origin" in item:
            target=[int(v) for v in item["origin"]];actual=list(m.origin)
            err=_max_abs(actual,target);checks+=1;max_error=max(max_error,err)
            details.append({"type":"module_origin","module":mid,"target":target,"actual":actual,"error":err,"tolerance":tol})
            if err>tol:errors.append(f"{mid} origin error {err} > {tol}")
        if "size" in item:
            target=[int(v) for v in item["size"]];actual=list(m.size)
            err=_max_abs(actual,target);checks+=1;max_error=max(max_error,err)
            details.append({"type":"module_size","module":mid,"target":target,"actual":actual,"error":err,"tolerance":tol})
            if err>tol:errors.append(f"{mid} size error {err} > {tol}")

    for item in cfg.get("port_targets",[]):
        mid=str(item["module"]);pid=str(item["port"])
        if mid not in plan.modules or mid not in placed:
            errors.append(f"reference port target missing module {mid}");continue
        try:port=port_for(plan.modules[mid],pid)
        except KeyError:
            errors.append(f"reference port target missing port {mid}:{pid}");continue
        actual=list(world_port(placed[mid].origin,port).pos)
        target=[int(v) for v in item["target"]]
        tol=max(0,int(item.get("tolerance",default_tol)))
        err=_max_abs(actual,target);checks+=1;max_error=max(max_error,err)
        details.append({"type":"port","module":mid,"port":pid,"target":target,"actual":actual,"error":err,"tolerance":tol})
        if err>tol:errors.append(f"{mid}:{pid} anchor error {err} > {tol}")

    for item in cfg.get("facade_targets",[]):
        mid=str(item["module"]);side=str(item["side"]).lower()
        if mid not in placed:
            errors.append(f"reference facade target missing module {mid}");continue
        m=placed[mid];actual_len=m.size[0] if side in ("north","south") else m.size[2]
        actual_h=m.size[1];tol=max(0,int(item.get("tolerance",default_tol)))
        if "length" in item:
            target=int(item["length"]);err=abs(actual_len-target);checks+=1;max_error=max(max_error,err)
            details.append({"type":"facade_length","module":mid,"side":side,"target":target,"actual":actual_len,"error":err,"tolerance":tol})
            if err>tol:errors.append(f"{mid}:{side} facade length error {err} > {tol}")
        if "height" in item:
            target=int(item["height"]);err=abs(actual_h-target);checks+=1;max_error=max(max_error,err)
            details.append({"type":"facade_height","module":mid,"side":side,"target":target,"actual":actual_h,"error":err,"tolerance":tol})
            if err>tol:errors.append(f"{mid}:{side} facade height error {err} > {tol}")

    status="PASS" if not errors else ("FAIL" if strict else "ADVISORY")
    if strict and errors:
        raise ValueError("Reference fit failed: "+"; ".join(errors))
    return {
        "enabled":True,"status":status,"strict":strict,"checks":checks,"max_error":max_error,
        "errors":errors,"details":details
    }
