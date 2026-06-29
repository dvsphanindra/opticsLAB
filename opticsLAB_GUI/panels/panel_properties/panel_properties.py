"""
PropertyGrid inspector panel for optical component and project workspace attributes.
"""
import inspect
import re
import numpy as np
import wx
import wx.propgrid as pg
from panel_properties_GUI import panel_properties
from opticsLAB_support import (
    CubeColourProperty, color_to_wx, wx_color_to_hex, DEFAULT_PRESETS,
    color_to_vispy, next_unique_name, offset_preset_center, remove_visual,
    resolve_template_name, is_lens_name, is_ray_name, is_beam_name, is_screen_name
)

try:
    from opticsLAB.raytracing.component.primitives.constants import (
        X_AXIS_DC, Y_AXIS_DC, Z_AXIS_DC,
        X_AXIS_NEG_DC, Y_AXIS_NEG_DC, Z_AXIS_NEG_DC
    )
    from opticsLAB.raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
    from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
    from opticsLAB.raytracing.component.sources import Ray, Beam, CircularBeam
    from opticsLAB.raytracing.component.detectors import RectangularScreen
    from opticsLAB.raytracing.component.primitives.parabolicSurface import Parabolic_Surface
    from opticsLAB.raytracing.component.opticalPrimitives.convexParaboloid import Convex_Paraboloid
    from opticsLAB.raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
    from opticsLAB.raytracing.component.primitives.sphericalSurface import Spherical_Surface
    from opticsLAB.raytracing.component.primitives.plane import Plane
except ImportError:
    from raytracing.component.primitives.constants import (
        X_AXIS_DC, Y_AXIS_DC, Z_AXIS_DC,
        X_AXIS_NEG_DC, Y_AXIS_NEG_DC, Z_AXIS_NEG_DC
    )
    from raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
    from raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
    from raytracing.component.sources import Ray, Beam, CircularBeam
    from raytracing.component.detectors import RectangularScreen
    from raytracing.component.primitives.parabolicSurface import Parabolic_Surface
    from raytracing.component.opticalPrimitives.convexParaboloid import Convex_Paraboloid
    from raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
    from raytracing.component.primitives.sphericalSurface import Spherical_Surface
    from raytracing.component.primitives.plane import Plane

DIRECTION_PRESETS = {
    "Z_AXIS_DIRECTION": Z_AXIS_DC.tolist(),
    "X_AXIS_DIRECTION": X_AXIS_DC.tolist(),
    "Y_AXIS_DIRECTION": Y_AXIS_DC.tolist(),
    "Z_AXIS_NEG_DIRECTION": Z_AXIS_NEG_DC.tolist(),
    "X_AXIS_NEG_DIRECTION": X_AXIS_NEG_DC.tolist(),
    "Y_AXIS_NEG_DIRECTION": Y_AXIS_NEG_DC.tolist(),
}

PROPERTY_DESCRIPTIONS = {
    "name": "Name: Unique identification string for this optical component or element in the active scene.",
    "center": "Center (X, Y, Z): 3D global Cartesian origin coordinates defining the component's position in space.",
    "center_group": "Center (X, Y, Z): 3D global Cartesian origin coordinates defining the component's position in space.",
    "center_x": "Center X: Global X-axis coordinate displacement of the component origin.",
    "center_y": "Center Y: Global Y-axis coordinate displacement of the component origin.",
    "center_z": "Center Z: Global Z-axis coordinate displacement (along optical axis) of the component origin.",
    "direction": "Direction: Orientation vector or direction cosines defining propagation or surface normal vector.",
    "color": "Color: RGBA / Hex display color used for rendering the visual representation in the 3D scene.",
    "radius": "Radius: Clear aperture radius defining the circular outer boundary of the optical surface or lens.",
    "thickness": "Thickness: Center axial thickness along the optical propagation axis.",
    "mediumBefore": "Medium Before: Refractive index or material medium preceding this optical interface (e.g., Air, Vacuum).",
    "mediumAfter": "Medium After: Refractive index or material substrate following this optical interface (e.g., BK7, FusedSilica).",
    "R1": "R1 (Front Radius): Radius of curvature for the front optical surface (positive = convex, negative = concave).",
    "R2": "R2 (Back Radius): Radius of curvature for the rear optical surface.",
    "a": "Parabolic Coeff 'a': Quadratic coefficient defining surface sagittal profile curvature.",
    "b": "Parabolic Coeff 'b': Cross-sectional parameter for parabolic surface profiles.",
    "c": "Parabolic Coeff 'c': Axial scaling factor for parabolic surfaces.",
    "c_front": "Front Curvature: Vertex curvature factor for the front parabolic surface profile.",
    "c_back": "Back Curvature: Vertex curvature factor for the rear parabolic surface profile.",
    "radius_of_curvature": "Radius of Curvature: Spherical radius defining surface curvature magnitude.",
    "aperture_radius": "Aperture Radius: Clear physical boundary radius of the active optical aperture.",
    "xTilt": "X-Tilt: Rotational angular tilt around the local X-axis (degrees).",
    "yTilt": "Y-Tilt: Rotational angular tilt around the local Y-axis (degrees).",
    "length": "Length: Propagation physical length of ray lines or rectangular aperture dimensions.",
    "breath": "Breath: Lateral breadth dimension of rectangular beam patterns or screen aperture.",
    "width": "Width: Lateral width dimension of rectangular surfaces or detectors.",
    "wavelength": "Wavelength: Monochromatic ray wavelength specified in micrometers (um) or nanometers.",
    "noOfRays": "Number of Rays: Total count of discrete optical light rays generated in this beam source bundle.",
    "centerRay": "Center Ray: Boolean flag enabling an axial chief ray at the center of the circular beam distribution.",
    "project_name": "Project Name: Workspace title for the current optical design file.",
    "designer": "Designer: Author or optical engineer credited with this design.",
    "approver": "Approver: Reviewer or lead engineer assigned to approve this optical system design.",
    "description": "Description: Project notes, optical system specifications, and documentation details.",
    "vispy_elevation": "Camera Elevation: Initial 3D view camera polar elevation angle (degrees).",
    "vispy_azimuth": "Camera Azimuth: Initial 3D view camera azimuthal rotation angle (degrees).",
    "vispy_zoom": "Camera Zoom: Default viewport magnification factor.",
    "vispy_camera": "Camera Mode: Interactive 3D camera navigation model (e.g. Arcball, Turntable, Fly, PanZoom).",
    "vispy_bg_color": "Background Color: Viewport 3D canvas background rendering color.",
    "show_xyz_axis": "Show XYZ Axes: Toggle display of 3D Cartesian reference coordinate axes in the viewport.",
    "show_optical_axis": "Show Optical Axis: Toggle display of central reference optical Z-axis line in the scene.",
    "optical_axis_length": "Optical Axis Length: Total span length of the reference optical Z-axis indicator.",
    "optical_axis_color": "Optical Axis Color: Color used to render the central reference optical axis line."
}


def _find_prop(grid, name):
    if p := grid.GetProperty(name): return p
    if p := grid.GetProperty("center_group." + name): return p
    it = grid.GetIterator()
    while not it.AtEnd():
        prop = it.GetProperty()
        it.Next()
        if prop and (prop.GetName() == name or (hasattr(prop, "GetBaseName") and prop.GetBaseName() == name)):
            return prop
    return None


class PropertiesPanel(panel_properties):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.current_preset_data = {}
        self.is_project_settings = False
        self.m_propertyGrid2.Bind(pg.EVT_PG_SELECTED, self.OnPropertySelected)

    def update_description_box(self, prop=None, custom_text=None):
        widget = getattr(self, "textCtrl_description", None) or getattr(self, "staticText_description", None) or getattr(self, "m_staticText_description", None)
        if not widget: return

        text = custom_text
        if not text and not prop:
            prop = self.m_propertyGrid2.GetSelectedProperty()
        if not text and prop:
            name = prop.GetBaseName() if hasattr(prop, "GetBaseName") else prop.GetName().split(".")[-1]
            text = PROPERTY_DESCRIPTIONS.get(name, PROPERTY_DESCRIPTIONS.get(prop.GetName(), f"Parameter: {prop.GetLabel()}\nType: {prop.GetValueType()}\nCurrent Value: {prop.GetValue()}"))
        if not text:
            text = "Select any property above to inspect parameter documentation."

        if hasattr(widget, "SetLabel"): widget.SetLabel(text)
        elif hasattr(widget, "SetValue"): widget.SetValue(text)

        if hasattr(widget, "Wrap"):
            try: widget.Wrap(max(180, self.GetSize().x - 30))
            except Exception: pass
        self.Layout()

    def OnPropertySelected(self, event):
        self.update_description_box(event.GetProperty())
        event.Skip()

    def m_propertyGrid2OnPropertyGridChanged(self, event):
        self.OnPropertyChanged(event)
        self.update_description_box(event.GetProperty())

    def show_project_properties(self):
        self.show_project_settings(getattr(self.frame, "project_info", {}))
        self.update_description_box(custom_text="Project Workspace Settings: Global viewport parameters, camera orientation, and design metadata.")
        if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
            self.frame.GetStatusBar().SetStatusText("Project Settings displayed.", 0)

    def apply_project_properties(self, data=None):
        data = getattr(self.frame, "project_info", {}) if data is None else data
        if hasattr(self.frame, "project_info"):
            self.frame.project_info.update(data)
        if hasattr(self.frame, "panel_components_tree") and hasattr(self.frame.panel_components_tree, "root"):
            try:
                self.frame.panel_components_tree.treeCtrl_projectComponents.SetItemText(
                    self.frame.panel_components_tree.root, data.get("name", "OpticsLAB Workspace")
                )
            except Exception: pass

        if hasattr(self.frame, "panel_simulation") and (canvas := self.frame.panel_simulation.canvas_obj):
            if hasattr(self.frame, "configure_canvas_camera"):
                self.frame.configure_canvas_camera(
                    camera_type=data.get("vispy_camera", "turntable"),
                    elevation=float(data.get("vispy_elevation", 30.0)),
                    azimuth=float(data.get("vispy_azimuth", 30.0))
                )

            zoom = float(data.get("vispy_zoom", 1.0))
            self.frame.zoom_level = zoom
            try:
                if hasattr(canvas.view.camera, "fov"): canvas.view.camera.fov = 30.0 / max(zoom, 0.01)
            except Exception: pass

            try: canvas.canvas.bgcolor = color_to_vispy(data.get("vispy_bg_color", "#000000ff"))
            except Exception: pass

            show_xyz = bool(data.get("show_xyz_axis", True))
            show_opt = bool(data.get("show_optical_axis", True))
            opt_len = float(data.get("optical_axis_length", 100.0))
            opt_col = color_to_vispy(data.get("optical_axis_color", "#ff6347ff"))

            try:
                for child in list(canvas.view.scene.children):
                    cls_name = child.__class__.__name__
                    if "XYZAxis" in cls_name or cls_name == "Text":
                        child.visible = show_xyz
                    elif "OpticalAxis" in cls_name or "LineVector" in cls_name or getattr(child, "name", "") == "Optical Axis":
                        child.visible = show_opt
                        if hasattr(child, "set_data"):
                            half_len = opt_len / 2.0
                            try: child.set_data(pos=np.array([[0, 0, -half_len], [0, 0, half_len]], dtype=np.float32), color=opt_col)
                            except Exception: pass
            except Exception as exc:
                print("Error updating scene visuals:", exc)

            canvas.canvas.update()
        if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
            self.frame.GetStatusBar().SetStatusText("Updated project & viewport settings.", 0)

    def show_ray_properties(self, parent_comp_name, ray_idx):
        active_comps = getattr(self.frame, "active_components", {})
        if parent_comp_name not in active_comps: return
        comp = active_comps[parent_comp_name]
        if not hasattr(comp, "get_Rays") or not callable(comp.get_Rays): return
        rays = comp.get_Rays()
        if not (0 <= ray_idx < len(rays)): return
        ray = rays[ray_idx]

        self.is_project_settings = False
        self.is_ray_settings = True
        self.current_ray_target = (parent_comp_name, ray_idx)

        start_pt = ray.lineStart_point if hasattr(ray, "lineStart_point") else np.array([0.0, 0.0, 0.0])
        dir_vec = ray.get_Direction_Cosines() if hasattr(ray, "get_Direction_Cosines") else np.array([0.0, 0.0, 1.0])

        preset = {
            "name": f"{parent_comp_name} - Ray {ray_idx + 1}",
            "center": start_pt.tolist() if hasattr(start_pt, "tolist") else list(start_pt),
            "direction": dir_vec.tolist() if hasattr(dir_vec, "tolist") else list(dir_vec),
            "wavelength": float(getattr(ray, "wavelength", 0.55)),
            "length": float(getattr(ray, "length", 15.0)),
            "color": wx_color_to_hex(getattr(ray, "color", "green"))
        }
        self.current_preset_data = preset.copy()
        self.set_properties(preset["name"], preset)
        self.update_description_box(custom_text=f"Inspecting parameters for individual light ray: {preset['name']}")
        if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
            self.frame.GetStatusBar().SetStatusText(f"Ray properties loaded: {preset['name']}", 0)

    def show_component_properties(self, comp_name, instantiate=True):
        self.is_ray_settings = False
        base_name = resolve_template_name(comp_name) or comp_name
        active_comps = getattr(self.frame, "active_components", {})
        default_presets = getattr(self.frame, "default_presets", DEFAULT_PRESETS)
        active_configs = getattr(self.frame, "active_component_configs", {})

        if instantiate and resolve_template_name(comp_name):
            unique_name = next_unique_name(base_name, active_comps)
            preset = offset_preset_center(default_presets[base_name].copy(), active_comps)
            preset["name"] = unique_name
            active_configs[unique_name] = preset
            self.set_properties(unique_name, preset)
            if hasattr(self.frame, "update_component_instance"):
                self.frame.update_component_instance(unique_name, preset)
            self.update_description_box(custom_text=f"Component Properties: {unique_name} ({base_name}). Select parameters below to inspect documentation.")
            return

        preset = active_configs.get(comp_name, default_presets.get(resolve_template_name(comp_name), {"name": comp_name, "center": [0.0, 0.0, 0.0], "radius": 1.0, "color": "#00ff00ff"}))
        self.set_properties(comp_name, preset)
        self.update_description_box(custom_text=f"Component Properties: {comp_name}. Select parameters below to inspect documentation.")
        if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
            self.frame.GetStatusBar().SetStatusText(f"Properties loaded: {comp_name}", 0)

    def show_project_settings(self, project_data):
        self.is_ray_settings = False
        self.is_project_settings = True
        self.current_preset_data = project_data.copy()
        grid = self.m_propertyGrid2
        grid.Clear()

        grid.Append(pg.PropertyCategory("Project Settings"))
        grid.Append(pg.StringProperty("project_name", value=str(project_data.get("name", "OpticsLAB Project"))))
        grid.Append(pg.StringProperty("designer", value=str(project_data.get("designer", "Unassigned"))))
        grid.Append(pg.StringProperty("approver", value=str(project_data.get("approver", "Unassigned"))))
        grid.Append(pg.StringProperty("description", value=str(project_data.get("description", ""))))

        grid.Append(pg.PropertyCategory("3D Viewport & Axes Settings"))
        grid.Append(pg.FloatProperty("vispy_elevation", value=float(project_data.get("vispy_elevation", 30.0))))
        grid.Append(pg.FloatProperty("vispy_azimuth", value=float(project_data.get("vispy_azimuth", 30.0))))
        grid.Append(pg.FloatProperty("vispy_zoom", value=float(project_data.get("vispy_zoom", 1.0))))

        cam_presets = ["Arcball (3D Trackball)", "Turntable (3D Orbit)", "Fly (First Person)", "PanZoom (2D Flat)", "Perspective (3D Perspective)", "Magnify (Interactive Magnifier)"]
        cur_cam = str(project_data.get("vispy_camera", "Turntable (3D Orbit)"))
        sel_idx = next((idx for idx, name in enumerate(cam_presets) if cur_cam.lower() in name.lower() or name.lower().startswith(cur_cam.lower().split()[0])), 1)
        grid.Append(pg.EnumProperty("Camera Mode", "vispy_camera", pg.PGChoices(cam_presets), sel_idx))
        grid.Append(CubeColourProperty("vispy_bg_color", "vispy_bg_color", color_to_wx(project_data.get("vispy_bg_color", "#000000ff"))))

        grid.Append(pg.BoolProperty("show_xyz_axis", value=bool(project_data.get("show_xyz_axis", True))))
        grid.Append(pg.BoolProperty("show_optical_axis", value=bool(project_data.get("show_optical_axis", True))))
        grid.Append(pg.FloatProperty("optical_axis_length", value=float(project_data.get("optical_axis_length", 100.0))))
        grid.Append(CubeColourProperty("optical_axis_color", "optical_axis_color", color_to_wx(project_data.get("optical_axis_color", "#ff6347ff"))))

    def _resolve_backend_class(self, comp_type):
        name_lower = str(comp_type).lower()
        if is_lens_name(name_lower):
            return ParabolicLens if "parabolic" in name_lower else SphericalLens
        if is_ray_name(name_lower): return Ray
        if is_beam_name(name_lower):
            return Beam if "rect" in name_lower or "random" in name_lower else CircularBeam
        if is_screen_name(name_lower): return RectangularScreen
        if "parabolic surface" in name_lower: return Parabolic_Surface
        if "convex paraboloid" in name_lower: return Convex_Paraboloid
        if "parabolic" in name_lower or "paraboloid" in name_lower: return Concave_Paraboloid
        if "spherical" in name_lower: return Spherical_Surface
        return Plane

    def _fetch_backend_allowed_keys(self, comp_name, data):
        cls = None
        if hasattr(self.frame, "active_components") and comp_name in self.frame.active_components:
            if comp_obj := self.frame.active_components[comp_name]: cls = comp_obj.__class__
        if cls is None:
            cls = self._resolve_backend_class(str(data.get("type") or comp_name or ""))

        raw_params = set()
        for c in cls.mro():
            if hasattr(c, "__init__"):
                try:
                    for p in inspect.signature(c.__init__).parameters.keys():
                        if p not in ("self", "args", "kwargs"): raw_params.add(p)
                except (ValueError, TypeError): pass

        alias_map = {"startPoint": "center", "rayDirection": "direction", "beamDirection": "direction", "aperture_radius": "radius", "parentCanvas": None, "parent": None, "dc": None}
        allowed = {"name", "type"}
        for p in raw_params:
            if mapped := alias_map.get(p, p): allowed.add(mapped)
        return allowed

    def set_properties(self, comp_name, data):
        self._is_populating = True
        try:
            self.is_project_settings = False
            self.current_preset_data = data.copy()
            grid = self.m_propertyGrid2
            grid.Clear()

            grid.Append(pg.PropertyCategory("General Properties"))
            grid.Append(pg.StringProperty("name", value=str(data.get("name", comp_name))))

            grid.Append(pg.PropertyCategory("Component Parameters"))
            skip_keys, allowed_keys = {"name", "type", "doc"}, self._fetch_backend_allowed_keys(comp_name, data)

            for key, val in data.items():
                if key in skip_keys or key not in allowed_keys: continue
                if key == "color":
                    grid.Append(CubeColourProperty("color", "color", color_to_wx(val)))
                elif key == "center" and isinstance(val, (list, tuple)):
                    c_vals = [float(v) for v in val]
                    parent_center = grid.Append(pg.StringProperty("Center", "center_group", f"({c_vals[0]}, {c_vals[1]}, {c_vals[2]})"))
                    grid.AppendIn(parent_center, pg.FloatProperty("X", "center_x", value=c_vals[0]))
                    grid.AppendIn(parent_center, pg.FloatProperty("Y", "center_y", value=c_vals[1]))
                    grid.AppendIn(parent_center, pg.FloatProperty("Z", "center_z", value=c_vals[2]))
                elif key == "direction":
                    cur_vec = [float(v) for v in val] if isinstance(val, (list, tuple)) else [0.0, 0.0, 1.0]
                    sel_idx = next((idx for idx, p_vec in enumerate(DIRECTION_PRESETS.values()) if np.allclose(cur_vec, p_vec, atol=1e-2)), 0)
                    grid.Append(pg.EnumProperty("Direction", "direction", pg.PGChoices(list(DIRECTION_PRESETS.keys())), sel_idx))
                elif isinstance(val, bool): grid.Append(pg.BoolProperty(key, value=bool(val)))
                elif isinstance(val, int) and not isinstance(val, bool): grid.Append(pg.IntProperty(key, value=int(val)))
                elif isinstance(val, (float, np.floating)): grid.Append(pg.FloatProperty(key, value=float(val)))
                elif isinstance(val, (list, tuple)):
                    for idx, item in enumerate(val):
                        grid.Append(pg.FloatProperty(f"{key}_{idx}", value=float(item)) if isinstance(item, (int, float)) else pg.StringProperty(f"{key}_{idx}", value=str(item)))
                else: grid.Append(pg.StringProperty(key, value=str(val)))
        finally:
            self._is_populating = False

    def OnPropertyChanged(self, event):
        if getattr(self, "_is_populating", False): return
        prop = event.GetProperty()
        grid = self.m_propertyGrid2
        if prop:
            prop_name = prop.GetName()
            base_name = prop.GetBaseName() if hasattr(prop, "GetBaseName") else prop_name.split(".")[-1]
            if prop_name == "center_group" or base_name == "center_group":
                nums = re.findall(r"[-+]?\d*\.\d+|\d+", str(prop.GetValue()))
                if len(nums) >= 3:
                    try:
                        cx, cy, cz = float(nums[0]), float(nums[1]), float(nums[2])
                        self._is_populating = True
                        try:
                            if px := _find_prop(grid, "center_x"): px.SetValue(cx)
                            if py := _find_prop(grid, "center_y"): py.SetValue(cy)
                            if pz := _find_prop(grid, "center_z"): pz.SetValue(cz)
                        finally: self._is_populating = False
                    except Exception: pass
            elif base_name in ("center_x", "center_y", "center_z") or prop_name.endswith((".center_x", ".center_y", ".center_z")):
                try:
                    px, py, pz = _find_prop(grid, "center_x"), _find_prop(grid, "center_y"), _find_prop(grid, "center_z")
                    cx = float(px.GetValue()) if px else 0.0
                    cy = float(py.GetValue()) if py else 0.0
                    cz = float(pz.GetValue()) if pz else 0.0
                    self._is_populating = True
                    try:
                        if p_grp := _find_prop(grid, "center_group"): p_grp.SetValue(f"({cx}, {cy}, {cz})")
                    finally: self._is_populating = False
                except Exception: pass

        if getattr(self, "is_ray_settings", False):
            if not (data := self.get_current_grid_data()) or not hasattr(self, "current_ray_target"): return
            parent_comp_name, ray_idx = self.current_ray_target
            if hasattr(self.frame, "update_ray_instance"): self.frame.update_ray_instance(parent_comp_name, ray_idx, data)
            self.current_preset_data = data.copy()
        elif self.is_project_settings:
            if data := self.get_current_project_data(): self.frame.apply_project_properties(data)
        else:
            if not (data := self.get_current_grid_data()): return
            old_name = self.current_preset_data.get("name", data.get("name", "Component"))
            self.frame.update_component_instance(old_name, data)
            self.current_preset_data = data.copy()

    def get_current_project_data(self):
        grid = self.m_propertyGrid2
        if not grid.GetProperty("project_name"): return {}
        return {
            "name": str(grid.GetPropertyValue("project_name")),
            "designer": str(grid.GetPropertyValue("designer")),
            "approver": str(grid.GetPropertyValue("approver")),
            "description": str(grid.GetPropertyValue("description")),
            "vispy_elevation": float(grid.GetPropertyValue("vispy_elevation")),
            "vispy_azimuth": float(grid.GetPropertyValue("vispy_azimuth")),
            "vispy_zoom": float(grid.GetPropertyValue("vispy_zoom")),
            "vispy_camera": str(grid.GetPropertyValueAsString("vispy_camera")),
            "vispy_bg_color": wx_color_to_hex(grid.GetPropertyValue("vispy_bg_color")),
            "show_xyz_axis": bool(grid.GetPropertyValue("show_xyz_axis")),
            "show_optical_axis": bool(grid.GetPropertyValue("show_optical_axis")),
            "optical_axis_length": float(grid.GetPropertyValue("optical_axis_length")),
            "optical_axis_color": wx_color_to_hex(grid.GetPropertyValue("optical_axis_color"))
        }

    def get_current_grid_data(self):
        if self.is_project_settings: return self.get_current_project_data()
        grid = self.m_propertyGrid2
        if not grid.GetProperty("name"): return {}

        data = {"name": str(grid.GetPropertyValue("name"))}
        if self.current_preset_data.get("type"): data["type"] = self.current_preset_data["type"]
        it, center_coords = grid.GetIterator(), [None, None, None]

        while not it.AtEnd():
            prop = it.GetProperty()
            it.Next()
            if not prop or prop.IsCategory(): continue
            prop_name = prop.GetName()
            name = prop.GetBaseName() if hasattr(prop, "GetBaseName") else prop_name.split(".")[-1]
            val = prop.GetValue()

            if name in ("name", "center_group"): continue
            elif name in ("center_x", "center_y", "center_z"):
                center_coords[{"center_x": 0, "center_y": 1, "center_z": 2}[name]] = float(val) if val is not None else 0.0
            elif name == "direction":
                dir_str = str(grid.GetPropertyValueAsString(prop))
                if dir_str in DIRECTION_PRESETS: data["direction"] = DIRECTION_PRESETS[dir_str]
                else:
                    try: data["direction"] = DIRECTION_PRESETS[list(DIRECTION_PRESETS.keys())[int(val)]]
                    except Exception: data["direction"] = [0.0, 0.0, 1.0]
            elif name == "color": data["color"] = wx_color_to_hex(val)
            else:
                if isinstance(val, bool): data[name] = bool(val)
                elif isinstance(val, int): data[name] = int(val)
                elif isinstance(val, float): data[name] = float(val)
                elif val is not None:
                    val_str = str(val)
                    try: data[name] = float(val_str) if "." in val_str else int(val_str)
                    except ValueError: data[name] = val_str

        if any(c is None for c in center_coords) and (p_grp := _find_prop(grid, "center_group")):
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", str(p_grp.GetValue()))
            if len(nums) >= 3:
                try: center_coords = [float(nums[0]), float(nums[1]), float(nums[2])]
                except Exception: pass

        if any(c is not None for c in center_coords):
            data["center"] = [c if c is not None else 0.0 for c in center_coords]
        return data
