"""
Shared helpers, preset loaders, and color conversion routines for OpticsLAB.
"""
import json
import os
import re
import numpy as np
import wx
import wx.propgrid as pg
import wx.lib.agw.cubecolourdialog as CCD
from vispy.color import Color as VisColor

try:
    import tomllib
except ImportError:
    tomllib = None

try:
    import toml
except ImportError:
    toml = None

DEFAULT_PRESETS = {}

TREE_CATEGORY_LABELS = frozenset({
    "[project]", "[[components]]", "Optics System Layout", "Light Sources", "Detectors",
    "Optical Elements", "Lenses", "Mirrors & Surfaces", "Traced Rays",
})


# ---------------------------------------------------------------------------
# Colour Property Grid Editor
# ---------------------------------------------------------------------------
class CubeColourDialogAdapter(pg.PGEditorDialogAdapter):
    def DoShowDialog(self, propGrid, property):
        val = property.GetValue()
        colour = val if isinstance(val, wx.Colour) else val.GetColour() if hasattr(val, "GetColour") else wx.Colour(val)
        colour_data = wx.ColourData()
        colour_data.SetColour(colour)
        dlg = CCD.CubeColourDialog(propGrid, colour_data)
        res = False
        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(dlg.GetColourData().GetColour())
            res = True
        dlg.Destroy()
        return res


class CubeColourProperty(pg.ColourProperty):
    def __init__(self, label, name, value):
        super().__init__(label, name, value)
        self.SetEditor("TextCtrlAndButton")

    def GetEditorDialog(self):
        return CubeColourDialogAdapter()


# ---------------------------------------------------------------------------
# Recent Files Persistence
# ---------------------------------------------------------------------------
def get_recent_files_path():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "recent_projects.json")


def load_recent_files():
    path = get_recent_files_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as h:
                items = json.load(h)
                if isinstance(items, list):
                    return [f for f in items if isinstance(f, str) and os.path.exists(f) and os.path.splitext(f)[1].lower() in (".json", ".toml")][:10]
        except Exception:
            pass
    return []


def add_recent_file(filepath):
    if not filepath or not isinstance(filepath, str) or os.path.splitext(filepath)[1].lower() not in (".json", ".toml"):
        return load_recent_files()
    norm_path = os.path.abspath(filepath)
    recent = [f for f in load_recent_files() if f != norm_path]
    recent.insert(0, norm_path)
    recent = recent[:10]
    try:
        with open(get_recent_files_path(), "w", encoding="utf-8") as h:
            json.dump(recent, h, indent=4)
    except Exception as exc:
        print("Error saving recent files:", exc)
    return recent


# ---------------------------------------------------------------------------
# Serializers & Data Wrappers
# ---------------------------------------------------------------------------
def _extract_component_data(data):
    return data["components"][0] if isinstance(data, dict) and data.get("components") else data


def _wrap_component_data(data):
    type_name = data.get("type", data.get("name", "Component"))
    return {"components": [{"type": type_name, **{k: v for k, v in data.items() if k != "type"}}]}


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as handle:
        return _extract_component_data(json.load(handle))


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as handle:
        json.dump(_wrap_component_data(data), handle, indent=4)


def load_toml(filepath):
    if toml is not None:
        with open(filepath, "r", encoding="utf-8") as handle:
            return _extract_component_data(toml.load(handle))
    data = {}
    with open(filepath, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith(("#", "[")) or "=" not in line:
                continue
            key, value = [p.strip().strip('"').strip("'") for p in line.split("=", 1)]
            if value.startswith("[") and value.endswith("]"):
                data[key] = [float(i) if "." in i else int(i) if i.isdigit() else i.strip('"') for i in value[1:-1].split(",")]
            elif value.lower() in ("true", "false"):
                data[key] = value.lower() == "true"
            else:
                try:
                    data[key] = float(value) if "." in value else int(value)
                except ValueError:
                    data[key] = value
    return data


def save_toml(filepath, data):
    wrapped = _wrap_component_data(data)
    if toml is not None:
        with open(filepath, "w", encoding="utf-8") as handle:
            toml.dump(wrapped, handle)
    else:
        comp_data = wrapped["components"][0]
        with open(filepath, "w", encoding="utf-8") as handle:
            handle.write("[[components]]\n")
            for key, value in comp_data.items():
                val_str = str(value).lower() if isinstance(value, bool) else f"[{', '.join(map(str, value))}]" if isinstance(value, list) else str(value) if isinstance(value, (int, float)) else f'"{value}"'
                handle.write(f"{key} = {val_str}\n")


# ---------------------------------------------------------------------------
# Colour Conversions
# ---------------------------------------------------------------------------
def _parse_rgba_channels(color_val):
    if isinstance(color_val, wx.Colour):
        return [color_val.Red(), color_val.Green(), color_val.Blue(), color_val.Alpha()]
    if hasattr(color_val, "rgba"):
        rgba = color_val.rgba
        ch = [int(c * 255) if isinstance(c, (float, np.floating)) and c <= 1.0 else int(c) for c in rgba]
        return (ch + [0, 0, 0, 255])[:4]
    if isinstance(color_val, str) and color_val.startswith("#"):
        r = int(color_val[1:3], 16) if len(color_val) >= 3 else 0
        g = int(color_val[3:5], 16) if len(color_val) >= 5 else 0
        b = int(color_val[5:7], 16) if len(color_val) >= 7 else 0
        a = int(color_val[7:9], 16) if len(color_val) >= 9 else 255
        return [r, g, b, a]
    if hasattr(color_val, "__iter__") and not isinstance(color_val, (str, bytes)):
        ch = [int(c * 255) if isinstance(c, (float, np.floating)) and c <= 1.0 else int(c) for c in color_val]
        return (ch + [0, 0, 0, 255])[:4]
    c = wx.Colour(color_val) if isinstance(color_val, str) else wx.Colour("green")
    c = c if c.IsOk() else wx.Colour("green")
    return [c.Red(), c.Green(), c.Blue(), c.Alpha()]


def color_to_wx(color_val):
    return wx.Colour(*_parse_rgba_channels(color_val))


def wx_color_to_hex(color_val):
    ch = _parse_rgba_channels(color_val)
    return f"#{ch[0]:02x}{ch[1]:02x}{ch[2]:02x}{ch[3]:02x}"


def color_to_vispy(color_val):
    if isinstance(color_val, wx.Colour):
        return VisColor((color_val.Red() / 255.0, color_val.Green() / 255.0, color_val.Blue() / 255.0, color_val.Alpha() / 255.0))
    if isinstance(color_val, str):
        return VisColor(color_val)
    if hasattr(color_val, "__iter__") and not isinstance(color_val, (str, bytes)):
        ch = [float(c) for c in color_val]
        if any(c > 1.0 for c in ch):
            ch = [c / 255.0 for c in ch]
        r, g, b = ch[:3]
        a = ch[3] if len(ch) > 3 else 1.0
        return VisColor((r, g, b, a))
    return VisColor(str(color_val))


# ---------------------------------------------------------------------------
# Presets & Classification Helpers
# ---------------------------------------------------------------------------
def load_default_presets():
    preset_file = os.path.join(os.path.dirname(__file__), "data", "presets", "presets.toml")
    presets = {}
    if os.path.exists(preset_file):
        try:
            if tomllib is not None:
                with open(preset_file, "rb") as f:
                    data = tomllib.load(f)
            else:
                data = load_toml(preset_file)
            for comp in data.get("components", []):
                key = comp.get("type") or comp.get("name")
                if key:
                    comp_copy = comp.copy()
                    if "color" in comp_copy:
                        comp_copy["color"] = wx_color_to_hex(comp_copy["color"])
                    presets[key] = comp_copy
        except Exception as exc:
            print("Error loading presets:", exc)
    return presets


DEFAULT_PRESETS = load_default_presets()


def normalize_direction_dc(direction, default=(0.0, 0.0, 1.0)):
    vec = np.array(direction if direction is not None else default, dtype=float)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist() if norm > 0 else list(default)


def normalize_material_name(mat_name):
    if not mat_name or not isinstance(mat_name, str):
        return "BK7"
    s_lower = mat_name.strip().lower()
    mapping = {
        "air": "Air", "vacuum": "Air", "glass": "BK7", "bk7": "BK7", "n-bk7": "BK7",
        "sapphire": "sapphire", "sapphire-ewave": "sapphire-EWave",
        "fused silica": "fused silica", "fusedsilica": "fused silica", "silica": "fused silica",
        "mgf": "MgF", "n-sk4": "N-SK4", "nsk4": "N-SK4", "sk4": "N-SK4",
        "n-sf2": "N-SF2", "nsf2": "N-SF2", "sf2": "N-SF2", "f2": "F2"
    }
    return mapping.get(s_lower, "BK7")


def normalize_component_name(name):
    return re.sub(r"\s+", " ", str(name).strip())


def resolve_template_name(name):
    return norm if (norm := normalize_component_name(name)) in DEFAULT_PRESETS else None


def is_template_name(name):
    return resolve_template_name(name) is not None


def is_ray_name(name):
    lower = str(name).lower()
    return "ray" in lower and "beam" not in lower and "array" not in lower


def is_beam_name(name):
    return "beam" in str(name).lower()


def is_screen_name(name):
    lower = str(name).lower()
    return "screen" in lower or "detector" in lower


def is_lens_name(name):
    return "lens" in str(name).lower()


def is_light_source_name(name):
    return is_ray_name(name) or is_beam_name(name)


def template_base_name(name):
    match = re.match(r"^(.*?)(?:\s+\d+)?$", name.strip())
    return match.group(1) if match else name


def next_unique_name(base_name, existing_names):
    count = 1
    while (candidate := f"{base_name} {count}") in existing_names:
        count += 1
    return candidate


def component_z_value(comp):
    if comp is None or (center := getattr(comp, "center", None)) is None:
        return 0.0
    if hasattr(center, "get_coordinates"):
        try: return float(center.get_coordinates()[2])
        except Exception: pass
    if hasattr(center, "coordinates"):
        try: return float(center.coordinates[2])
        except Exception: pass
    if hasattr(center, "__getitem__"):
        try: return float(center[2])
        except Exception: pass
    return 0.0


def max_z_from_components(active_components):
    return max((component_z_value(c) for c in active_components.values()), default=0.0)


def offset_preset_center(preset, active_components, z_offset=1.5):
    if not active_components:
        return preset
    updated = preset.copy()
    z_value = max_z_from_components(active_components) + z_offset
    updated["center"] = [0.0, 0.0, z_value]
    if "z" in updated:
        updated["z"] = z_value
    return updated


def remove_visual(comp):
    if comp is None:
        return
    if hasattr(comp, "surfaces"):
        for surface in comp.surfaces:
            remove_visual(surface)
        if hasattr(comp, "_frame"):
            remove_visual(comp._frame)
        return
    if hasattr(comp, "get_Rays"):
        for ray in comp.get_Rays():
            remove_visual(ray)
        return
    visual = getattr(comp, "get_Visual", getattr(comp, "get_visual", lambda: getattr(comp, "lineVisual", None)))
    vis_obj = visual() if callable(visual) else visual
    if vis_obj is not None:
        vis_obj.parent = None