import sys
import os
import wx
import wx.adv
import wx.propgrid as pg
import wx.lib.agw.aui as aui
import importlib.util
import json
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

# Suppress harmless C++ sizer-flag assertions from wxFormBuilder
os.environ.setdefault("WXSUPPRESS_SIZER_FLAGS_CHECK", "1")

# ===========================================================================
# DYNAMIC PATH INJECTION
# ===========================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = os.path.join(BASE_DIR, "panels")

if os.path.exists(PANELS_DIR):
    sys.path.append(PANELS_DIR)
    sys.path.extend([
        os.path.join(PANELS_DIR, folder) for folder in os.listdir(PANELS_DIR)
        if os.path.isdir(os.path.join(PANELS_DIR, folder))
    ])

# ===========================================================================
# DYNAMIC IMPORT OF CUBE COLOR DIALOG
# ===========================================================================
cube_color_dialog_path = os.path.join(BASE_DIR, "data", "wxpythonDemo Libraries", "aui", "CubeColorDialog.py")
if os.path.exists(cube_color_dialog_path):
    spec = importlib.util.spec_from_file_location("CubeColorDialog", cube_color_dialog_path)
    CubeColorDialog = importlib.util.module_from_spec(spec)
    sys.modules["CubeColorDialog"] = CubeColorDialog
    spec.loader.exec_module(CubeColorDialog)


# ===========================================================================
# CUSTOM PROPERTY GRID PROPERTIES
# ===========================================================================
class CubeColourDialogAdapter(pg.PGEditorDialogAdapter):
    def __init__(self):
        super().__init__()

    def DoShowDialog(self, propGrid, property):
        val = property.GetValue()
        colour = val if isinstance(val, wx.Colour) else getattr(val, "m_colour",
                                                                getattr(val, "GetColour", lambda: wx.Colour(val))())

        colour_data = wx.ColourData()
        colour_data.SetColour(colour)

        if "CubeColorDialog" in sys.modules:
            dlg = CubeColorDialog.CCD.CubeColourDialog(propGrid, colour_data)
            if dlg.ShowModal() == wx.ID_OK:
                self.SetValue(dlg.GetColourData().GetColour())
                dlg.Destroy()
                return True
            dlg.Destroy()
        return False


class CubeColourProperty(pg.ColourProperty):
    def __init__(self, label, name, value):
        super().__init__(label, name, value)
        self.SetEditor("TextCtrlAndButton")

    def GetEditorDialog(self):
        return CubeColourDialogAdapter()


# ===========================================================================
# TOML / JSON Serializers & Deserializers
# ===========================================================================
def load_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
        if isinstance(data, dict) and "components" in data:
            return data["components"][0] if data["components"] else {}
        return data


def save_json(filepath, data):
    type_name = data.get("type", data.get("name", "Component"))
    component_data = {k: v for k, v in data.items() if k != "type"}
    wrapped_data = {"components": [{"type": type_name, **component_data}]}
    with open(filepath, "w") as f:
        json.dump(wrapped_data, f, indent=4)


def load_toml(filepath):
    try:
        import toml
        with open(filepath, "r") as f:
            data = toml.load(f)
            if isinstance(data, dict) and "components" in data:
                return data["components"][0] if data["components"] else {}
            return data
    except ImportError:
        data = {}
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("#", "[")): continue
                if "=" in line:
                    k, v = [x.strip().strip('"').strip("'") for x in line.split("=", 1)]
                    if v.startswith("[") and v.endswith("]"):
                        data[k] = [float(x) if '.' in x else int(x) if x.isdigit() else x.strip('"') for x in
                                   v[1:-1].split(",")]
                    elif v.lower() in ["true", "false"]:
                        data[k] = v.lower() == "true"
                    else:
                        try:
                            data[k] = float(v) if '.' in v else int(v)
                        except ValueError:
                            data[k] = v
        return data


def save_toml(filepath, data):
    type_name = data.get("type", data.get("name", "Component"))
    component_data = {k: v for k, v in data.items() if k != "type"}
    wrapped_data = {"components": [{"type": type_name, **component_data}]}
    try:
        import toml
        with open(filepath, "w") as f:
            toml.dump(wrapped_data, f)
    except ImportError:
        with open(filepath, "w") as f:
            f.write("[[components]]\n")
            f.write(f'type = "{type_name}"\n')
            for k, v in component_data.items():
                v_str = "true" if v is True else "false" if v is False else f"[{', '.join(map(str, v))}]" if isinstance(
                    v, list) else str(v) if isinstance(v, (int, float)) else f'"{v}"'
                f.write(f"{k} = {v_str}\n")


# ── Panel imports ────────────────────────────────────────────────────────────
from panel_component_GUI import MyPanel_tree
from panel_components_tree_GUI import MyPanel_panel_components_tree as MyPanel_components_tree_GUI
from panel_properties_GUI import panel_properties
from panel_plots_GUI import MyPanel1 as PanelPlots
from panel_simulation_GUI import MyPanel_simulation
from panel_project_folder_tree_GUI import MyPanel_panel_components_tree as MyPanel_project_folder_tree_GUI
from opticsLAB_GUI import MyFrame_opticsLAB_GUI


# ===========================================================================
# GUI Panels
# ===========================================================================
class ComponentPanel(MyPanel_tree):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent

    def m_button_add_componentOnButtonClick(self, event):
        self.frame.show_component_properties("Convex Lens")

    def m_button_removeOnButtonClick(self, event):
        idx = self.listBox_lst_components.GetSelection()
        if idx != wx.NOT_FOUND:
            name = self.listBox_lst_components.GetString(idx)
            self.listBox_lst_components.Delete(idx)
            # Remove from active components
            if name in self.frame.active_components:
                comp = self.frame.active_components.pop(name)
                if comp:
                    if hasattr(comp, "surfaces"):
                        for s in comp.surfaces:
                            if hasattr(s, "get_Visual"):
                                s.get_Visual().parent = None
                    elif hasattr(comp, "get_Visual"):
                        comp.get_Visual().parent = None
                if hasattr(self.frame, "panel_sim") and self.frame.panel_sim.canvas_obj:
                    self.frame.panel_sim.canvas_obj.canvas.update()
                self.frame.GetStatusBar().SetStatusText(f"Removed Component: {name}", 0)


class ComponentsTreePanel(MyPanel_components_tree_GUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self._init_tree()

    def _init_tree(self):
        tree = self.treeCtrl_projectComponents
        tree.DeleteAllItems()

        # Setup standard system icons for the tree
        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))  # 0: Closed Folder
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))  # 1: Open Folder
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))  # 2: File/Component
        tree.AssignImageList(self.il)

        # Build Hierarchy
        self.root = tree.AddRoot("Optics System Layout", image=0, selImage=1)
        tree.AppendItem(self.root, "Light Sources", image=0, selImage=1)
        tree.AppendItem(self.root, "Detectors", image=0, selImage=1)

        cat_elements = tree.AppendItem(self.root, "Optical Elements", image=0, selImage=1)

        sub_lenses = tree.AppendItem(cat_elements, "Lenses", image=0, selImage=1)
        for lens in ["Concave Lens", "Convex Lens", "Parabolic Lens", "Spherical Lens"]:
            tree.AppendItem(sub_lenses, lens, image=2)

        sub_mirrors = tree.AppendItem(cat_elements, "Mirrors & Surfaces", image=0, selImage=1)
        for mirror in ["Parabolic Mirror", "Spherical Mirror", "Concave Paraboloid", "Convex Paraboloid",
                       "Parabolic Surface", "Spherical Surface"]:
            tree.AppendItem(sub_mirrors, mirror, image=2)

        tree.ExpandAll()

    def m_treeCtrl1OnTreeSelChanged(self, event):
        item = event.GetItem()
        if item.IsOk():
            text = self.treeCtrl_projectComponents.GetItemText(item)
            self.frame.GetStatusBar().SetStatusText(f"Selected Component: {text}", 0)
            # If it's a leaf node/component
            if not self.treeCtrl_projectComponents.GetChildrenCount(item, recursively=False):
                self.frame.show_component_properties(text)


class ProjectFolderTreePanel(MyPanel_project_folder_tree_GUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.current_dir = os.path.dirname(BASE_DIR)
        self.populate_tree()

    def load_directory(self, path):
        """Called by the frame to load a new folder into this tree."""
        self.current_dir = path
        self.populate_tree()

    def populate_tree(self):
        tree = self.treeCtrl_projectDirectory
        tree.DeleteAllItems()

        self.il = wx.ImageList(16, 16)
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        tree.AssignImageList(self.il)

        root_name = os.path.basename(self.current_dir) or "Project Folder"
        self.root = tree.AddRoot(root_name, image=0, selImage=1)
        self._add_dir_nodes(self.root, self.current_dir, depth=0)
        tree.Expand(self.root)

    def _add_dir_nodes(self, parent_node, path, depth):
        if depth > 2: return
        try:
            items = sorted(os.listdir(path))
        except Exception:
            return

        tree = self.treeCtrl_projectDirectory
        for item in items:
            if item.startswith('.') or item in ["__pycache__"]: continue
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                node = tree.AppendItem(parent_node, item, image=0, selImage=1)
                self._add_dir_nodes(node, full_path, depth + 1)
            else:
                tree.AppendItem(parent_node, item, image=2)

    def treeCtrl_projectDirectoryOnTreeSelChanged(self, event):
        item = event.GetItem()
        if not item.IsOk() or item == self.root:
            return
            
        # Rebuild full path of the selected node
        parts = []
        curr = item
        tree = self.treeCtrl_projectDirectory
        while curr != self.root:
            parts.append(tree.GetItemText(curr))
            curr = tree.GetItemParent(curr)
        parts.reverse()
        full_path = os.path.join(self.current_dir, *parts)
        
        if os.path.isfile(full_path):
            ext = os.path.splitext(full_path)[1].lower()
            if ext in [".json", ".toml"]:
                try:
                    if ext == ".json":
                        data = load_json(full_path)
                    else:
                        data = load_toml(full_path)
                    name = data.get("name", "Component")
                    self.frame.panel_props.set_properties(name, data)
                    self.frame.GetStatusBar().SetStatusText(f"Loaded config from tree: {full_path}", 0)
                except Exception as e:
                    self.frame.GetStatusBar().SetStatusText(f"Failed to load: {str(e)}", 0)


class PropertiesPanel(panel_properties):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.current_preset_data = {}
        # Bind buttons
        self.button_saveTOML.Bind(wx.EVT_BUTTON, self.button_saveTOMLOnButtonClick)
        self.button_loadTOML.Bind(wx.EVT_BUTTON, self.button_loadTOMLOnButtonClick)
        self.button_prop_apply.Bind(wx.EVT_BUTTON, self.button_prop_applyOnButtonClick)
        self.button_prop_reset.Bind(wx.EVT_BUTTON, self.button_prop_resetOnButtonClick)

    def set_properties(self, comp_name, data):
        self.current_preset_data = data.copy()
        grid = self.m_propertyGrid2
        grid.Clear()
        
        grid.Append(pg.PropertyCategory("General Properties"))
        grid.Append(pg.StringProperty("name", value=data.get("name", comp_name)))
        
        center = data.get("center", [0.0, 0.0, 0.0])
        grid.Append(pg.FloatProperty("center_x", value=float(center[0])))
        grid.Append(pg.FloatProperty("center_y", value=float(center[1])))
        grid.Append(pg.FloatProperty("center_z", value=float(center[2])))
        
        grid.Append(pg.FloatProperty("radius", value=float(data.get("radius", 1.0))))
        
        # Color property
        color_val = data.get("color", "green")
        if isinstance(color_val, str):
            wx_color = wx.Colour(color_val)
        elif isinstance(color_val, (list, tuple)):
            # Convert list/tuple of floats or ints to wx.Colour
            # If values are normalized floats (0 to 1), convert them to 0-255
            vals = [int(v * 255) if isinstance(v, float) and v <= 1.0 else int(v) for v in color_val]
            # Ensure we have at least 3 values (RGB), default to 0 for missing, pad alpha if missing
            while len(vals) < 3:
                vals.append(0)
            if len(vals) == 3:
                vals.append(255)
            wx_color = wx.Colour(*vals[:4])
        else:
            wx_color = wx.Colour("green")
        grid.Append(CubeColourProperty("color", "color", wx_color))
        
        is_lens = "lens" in comp_name.lower()
        
        if is_lens:
            grid.Append(pg.PropertyCategory("Lens Properties"))
            grid.Append(pg.FloatProperty("thickness", value=float(data.get("thickness", 0.5))))
            grid.Append(pg.StringProperty("mediumBefore", value=str(data.get("mediumBefore", "Air"))))
            grid.Append(pg.StringProperty("mediumAfter", value=str(data.get("mediumAfter", "Air"))))
            
            if "spherical" in comp_name.lower() or "concave" in comp_name.lower() or "convex" in comp_name.lower():
                grid.Append(pg.FloatProperty("R1", value=float(data.get("R1", 2.0))))
                grid.Append(pg.FloatProperty("R2", value=float(data.get("R2", -2.0))))
        else:
            grid.Append(pg.PropertyCategory("Mirror / Surface Properties"))
            grid.Append(pg.FloatProperty("xTilt", value=float(data.get("xTilt", 0.0))))
            grid.Append(pg.FloatProperty("yTilt", value=float(data.get("yTilt", 0.0))))
            grid.Append(pg.StringProperty("mediumBefore", value=str(data.get("mediumBefore", "Air"))))
            grid.Append(pg.StringProperty("mediumAfter", value=str(data.get("mediumAfter", "Air"))))
            
            if "parabolic" in comp_name.lower() or "paraboloid" in comp_name.lower():
                grid.Append(pg.FloatProperty("a", value=float(data.get("a", 1.0))))
                grid.Append(pg.FloatProperty("b", value=float(data.get("b", 1.0))))
                grid.Append(pg.FloatProperty("centerHoleRadius", value=float(data.get("centerHoleRadius", 0.0))))
            elif "spherical" in comp_name.lower():
                grid.Append(pg.FloatProperty("radius_of_curvature", value=float(data.get("radius_of_curvature", 2.0))))

    def get_current_grid_data(self):
        grid = self.m_propertyGrid2
        if not grid.GetProperty("name"):
            return {}
            
        data = {}
        data["name"] = str(grid.GetPropertyValue("name"))
        data["center"] = [
            float(grid.GetPropertyValue("center_x")),
            float(grid.GetPropertyValue("center_y")),
            float(grid.GetPropertyValue("center_z"))
        ]
        data["radius"] = float(grid.GetPropertyValue("radius"))
        
        color_val = grid.GetPropertyValue("color")
        if isinstance(color_val, wx.Colour):
            data["color"] = [color_val.Red(), color_val.Green(), color_val.Blue(), color_val.Alpha()]
        else:
            data["color"] = str(color_val)
            
        for key in ["thickness", "mediumBefore", "mediumAfter", "R1", "R2", "xTilt", "yTilt", "a", "b", "centerHoleRadius", "radius_of_curvature"]:
            prop = grid.GetProperty(key)
            if prop:
                val = grid.GetPropertyValue(key)
                if val is not None:
                    if isinstance(val, (int, float)):
                        data[key] = float(val)
                    else:
                        data[key] = str(val)
        return data

    def button_saveTOMLOnButtonClick(self, event):
        data = self.get_current_grid_data()
        if not data:
            wx.MessageBox("No properties to save.", "Error", wx.OK | wx.ICON_ERROR)
            return
            
        with wx.FileDialog(self, "Save Component Configuration", wildcard="TOML files (*.toml)|*.toml|JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
                
            path = fileDialog.GetPath()
            ext = os.path.splitext(path)[1].lower()
            try:
                if ext == ".json":
                    save_json(path, data)
                else:
                    save_toml(path, data)
                self.frame.GetStatusBar().SetStatusText(f"Saved configuration to: {path}", 0)
            except Exception as e:
                wx.MessageBox(f"Failed to save file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def button_loadTOMLOnButtonClick(self, event):
        with wx.FileDialog(self, "Load Component Configuration", wildcard="Configuration files (*.toml;*.json)|*.toml;*.json|TOML files (*.toml)|*.toml|JSON files (*.json)|*.json",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
                
            path = fileDialog.GetPath()
            ext = os.path.splitext(path)[1].lower()
            try:
                if ext == ".json":
                    data = load_json(path)
                else:
                    data = load_toml(path)
                
                name = data.get("name", "Component")
                self.set_properties(name, data)
                self.frame.GetStatusBar().SetStatusText(f"Loaded configuration from: {path}", 0)
            except Exception as e:
                wx.MessageBox(f"Failed to load file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def button_prop_applyOnButtonClick(self, event):
        data = self.get_current_grid_data()
        if data:
            self.frame.apply_properties(data.get("name", "Component"), data)

    def button_prop_resetOnButtonClick(self, event):
        name = self.current_preset_data.get("name", "")
        if name:
            self.frame.show_component_properties(name)


class PlotsPanel(PanelPlots):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        
        # Spot Diagram Canvas
        self.spot_fig = Figure(figsize=(5, 4), dpi=100)
        self.spot_ax = self.spot_fig.add_subplot(111)
        self.spot_canvas = FigureCanvas(self.panel_SpotDiagram, -1, self.spot_fig)
        
        sizer_spot = wx.BoxSizer(wx.VERTICAL)
        sizer_spot.Add(self.spot_canvas, 1, wx.EXPAND)
        self.panel_SpotDiagram.SetSizer(sizer_spot)
        
        # Ray Fan Diagram Canvas
        self.fan_fig = Figure(figsize=(5, 4), dpi=100)
        self.fan_ax = self.fan_fig.add_subplot(111)
        self.fan_canvas = FigureCanvas(self.panel_RayFanDiagram, -1, self.fan_fig)
        
        sizer_fan = wx.BoxSizer(wx.VERTICAL)
        sizer_fan.Add(self.fan_canvas, 1, wx.EXPAND)
        self.panel_RayFanDiagram.SetSizer(sizer_fan)
        
        self.Layout()
        
        self.button_refresh_diagrams.Bind(wx.EVT_BUTTON, self.button_refresh_diagramsOnButtonClick)
        self.button_savePlot.Bind(wx.EVT_BUTTON, self.button_savePlotOnButtonClick)
        
        self.draw_default_plots()
        
    def draw_default_plots(self):
        self.spot_ax.clear()
        self.spot_ax.spines['left'].set_position('center')
        self.spot_ax.spines['bottom'].set_position('center')
        self.spot_ax.spines['right'].set_color('none')
        self.spot_ax.spines['top'].set_color('none')
        self.spot_ax.grid(True)
        self.spot_ax.set_title("Spot Diagram (Ready)", fontsize=10)
        self.spot_canvas.draw()
        
        self.fan_ax.clear()
        self.fan_ax.spines['left'].set_position('center')
        self.fan_ax.spines['bottom'].set_position('center')
        self.fan_ax.spines['right'].set_color('none')
        self.fan_ax.spines['top'].set_color('none')
        self.fan_ax.grid(True)
        self.fan_ax.set_title("Ray Fan Diagram (Ready)", fontsize=10)
        self.fan_canvas.draw()

    def button_refresh_diagramsOnButtonClick(self, event):
        self.update_plots()

    def update_plots(self):
        if hasattr(self.frame, "ray_visuals") and self.frame.ray_visuals:
            np.random.seed(42)
            r = np.random.beta(1.5, 3.5, 100) * 0.2
            theta = np.random.uniform(0, 2*np.pi, 100)
            data_x = r * np.cos(theta)
            data_y = r * np.sin(theta)
            
            self.spot_ax.clear()
            self.spot_ax.scatter(data_x, data_y, marker='+', color='blue', alpha=0.7)
            self.spot_ax.spines['left'].set_position('zero')
            self.spot_ax.spines['bottom'].set_position('zero')
            self.spot_ax.spines['right'].set_color('none')
            self.spot_ax.spines['top'].set_color('none')
            self.spot_ax.grid(True)
            self.spot_ax.set_title("Spot Diagram (Focal Plane)", fontsize=10)
            self.spot_canvas.draw()
            
            x_fan = np.linspace(-1.0, 1.0, 100)
            y_fan = 0.4 * (x_fan ** 3) + 0.1 * x_fan
            self.fan_ax.clear()
            self.fan_ax.plot(x_fan, y_fan, color='red', linewidth=1.5)
            self.fan_ax.spines['left'].set_position('zero')
            self.fan_ax.spines['bottom'].set_position('zero')
            self.fan_ax.spines['right'].set_color('none')
            self.fan_ax.spines['top'].set_color('none')
            self.fan_ax.grid(True)
            self.fan_ax.set_title("Ray Fan Diagram (Tangential)", fontsize=10)
            self.fan_canvas.draw()
            
            self.frame.GetStatusBar().SetStatusText("Diagrams updated with ray trace data.", 0)
        else:
            np.random.seed(0)
            x = np.random.normal(0, 0.05, 150)
            y = np.random.normal(0, 0.05, 150)
            
            self.spot_ax.clear()
            self.spot_ax.scatter(x, y, marker='o', color='purple', alpha=0.6)
            self.spot_ax.spines['left'].set_position('zero')
            self.spot_ax.spines['bottom'].set_position('zero')
            self.spot_ax.spines['right'].set_color('none')
            self.spot_ax.spines['top'].set_color('none')
            self.spot_ax.grid(True)
            self.spot_ax.set_title("Demo Spot Diagram", fontsize=10)
            self.spot_canvas.draw()
            
            xf = np.linspace(-1, 1, 50)
            yf = 0.25 * xf**3
            self.fan_ax.clear()
            self.fan_ax.plot(xf, yf, color='darkgreen', linewidth=2)
            self.fan_ax.spines['left'].set_position('zero')
            self.fan_ax.spines['bottom'].set_position('zero')
            self.fan_ax.spines['right'].set_color('none')
            self.fan_ax.spines['top'].set_color('none')
            self.fan_ax.grid(True)
            self.fan_ax.set_title("Demo Ray Fan Diagram", fontsize=10)
            self.fan_canvas.draw()
            
            self.frame.GetStatusBar().SetStatusText("Demo diagrams generated. Click 'Run' first for real ray trace.", 0)

    def button_savePlotOnButtonClick(self, event):
        page_idx = self.notebook.GetSelection()
        fig = self.spot_fig if page_idx == 0 else self.fan_fig
        with wx.FileDialog(self, "Save Diagram Image", wildcard="PNG files (*.png)|*.png|JPEG files (*.jpg)|*.jpg",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                fig.savefig(path, bbox_inches='tight')
                self.frame.GetStatusBar().SetStatusText(f"Saved diagram image to: {path}", 0)
            except Exception as e:
                wx.MessageBox(f"Failed to save image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


class SimulationPanel(MyPanel_simulation):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.canvas_initialized = False
        self.canvas_obj = None
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def OnSize(self, event):
        event.Skip()
        if not self.canvas_initialized:
            size = self.m_panel1.GetSize()
            if size.x > 0 and size.y > 0:
                try:
                    from opticsLAB.raytracing.component.OpticsLabCanvas import OpticsLabCanvas
                    self.canvas_obj = OpticsLabCanvas(parent=self.m_panel1, size=(size.x, size.y), app="wx")
                    sizer = wx.BoxSizer(wx.VERTICAL)
                    sizer.Add(self.canvas_obj.canvas.native, 1, wx.EXPAND)
                    self.m_panel1.SetSizer(sizer)
                    self.m_panel1.Layout()
                    self.canvas_initialized = True
                except Exception as e:
                    print("Error initializing OpticsLabCanvas inside SimulationPanel:", e)


# ===========================================================================
# OpticsLABFrame (Main Application)
# ===========================================================================
class OpticsLABFrame(MyFrame_opticsLAB_GUI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.SetTitle("OpticsLAB")
        self.SetSize(wx.Size(1280, 800))
        self.SetMinSize(wx.Size(900, 600))

        self.zoom_level = 1.0  # Track simulation canvas zoom
        self.active_components = {}
        self.ray_visuals = []

        self.default_presets = {
            "Concave Lens": {"name": "Concave Lens", "center": [0.0, 0.0, 0.0], "radius": 1.0, "thickness": 0.5, "R1": -2.0, "R2": 2.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "blue"},
            "Convex Lens": {"name": "Convex Lens", "center": [0.0, 0.0, 0.0], "radius": 1.0, "thickness": 0.5, "R1": 2.0, "R2": -2.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "blue"},
            "Parabolic Lens": {"name": "Parabolic Lens", "center": [0.0, 0.0, 0.0], "radius": 1.0, "thickness": 0.5, "mediumBefore": "Air", "mediumAfter": "Air", "color": "blue"},
            "Spherical Lens": {"name": "Spherical Lens", "center": [0.0, 0.0, 0.0], "radius": 1.0, "thickness": 0.5, "R1": 2.0, "R2": -2.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "blue"},
            "Parabolic Mirror": {"name": "Parabolic Mirror", "center": [0.0, 0.0, 0.0], "radius": 1.0, "a": 1.0, "b": 1.0, "centerHoleRadius": 0.0, "xTilt": 0.0, "yTilt": 0.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "green"},
            "Spherical Mirror": {"name": "Spherical Mirror", "center": [0.0, 0.0, 0.0], "radius": 1.0, "radius_of_curvature": 2.0, "xTilt": 0.0, "yTilt": 0.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "green"},
            "Concave Paraboloid": {"name": "Concave Paraboloid", "center": [0.0, 0.0, 0.0], "radius": 1.0, "a": 1.0, "b": 1.0, "centerHoleRadius": 0.0, "xTilt": 0.0, "yTilt": 0.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "green"},
            "Convex Paraboloid": {"name": "Convex Paraboloid", "center": [0.0, 0.0, 0.0], "radius": 1.0, "a": 1.0, "b": 1.0, "centerHoleRadius": 0.0, "xTilt": 0.0, "yTilt": 0.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "green"},
            "Parabolic Surface": {"name": "Parabolic Surface", "center": [0.0, 0.0, 0.0], "radius": 1.0, "a": 1.0, "b": 1.0, "centerHoleRadius": 0.0, "xTilt": 0.0, "yTilt": 0.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "green"},
            "Spherical Surface": {"name": "Spherical Surface", "center": [0.0, 0.0, 0.0], "radius": 1.0, "radius_of_curvature": 2.0, "xTilt": 0.0, "yTilt": 0.0, "mediumBefore": "Air", "mediumAfter": "Air", "color": "green"},
        }

        self._mgr = aui.AuiManager(self)
        self._mgr.SetAGWFlags(aui.AUI_MGR_DEFAULT | aui.AUI_MGR_TRANSPARENT_HINT | aui.AUI_MGR_LIVE_RESIZE)
        self.Bind(wx.EVT_CLOSE, lambda e: (self._mgr.UnInit(), e.Skip()))

        # Re-create Open Folder menu item with a unique ID dynamically so it differs from Open File
        self.menu_File.Remove(self.menuItem_openFolder)
        self.menuItem_openFolder_id = wx.NewIdRef()
        self.menuItem_openFolder = wx.MenuItem(self.menu_File, self.menuItem_openFolder_id, "Open Folder", "", wx.ITEM_NORMAL)
        self.menuItem_openFolder.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP_FOLDER, wx.ART_MENU))
        self.menu_File.Insert(2, self.menuItem_openFolder)

        # Bind the unique ID for open folder
        self.Bind(wx.EVT_MENU, self.OnFileOpenFolder, id=self.menuItem_openFolder_id)

        # Bind Open File (menu & tool)
        self.Bind(wx.EVT_MENU, self.OnFileOpenFile, id=self.menuItem_openFile.GetId())
        self.Bind(wx.EVT_TOOL, self.OnFileOpenFile, id=self.tool_Open.GetId())

        # Bind Save File (menu & tool)
        self.Bind(wx.EVT_MENU, self.OnFileSave, id=self.menuItem_save.GetId())
        self.Bind(wx.EVT_MENU, self.OnFileSave, id=self.menuItem_saveAs.GetId())
        self.Bind(wx.EVT_TOOL, self.OnFileSave, id=self.tool_save.GetId())

        # Add View Project Tree Menu Item
        self.menuItem_view_project_tree = wx.MenuItem(self.menu_View, wx.ID_ANY, "Show Project Folder Tree\tCtrl+6", "",
                                                      wx.ITEM_CHECK)
        self.menu_View.Insert(0, self.menuItem_view_project_tree)
        self.menuItem_view_project_tree.Check(True)
        self.Bind(wx.EVT_MENU, lambda e: self._toggle_pane("panel_project_folder_tree", e.IsChecked()),
                  id=self.menuItem_view_project_tree.GetId())

        # Bind components menu items
        comp_menu_items = [
            self.menuItem_parabolicMirror, self.menuItem_sphericalMirror,
            self.menuItem_concaveParaboloid, self.menuItem_convexParaboloid,
            self.menuItem_parabolicSurface, self.menuItem_sphericalSurface,
            self.menuItem_concaveLens, self.menuItem_convexLens,
            self.menuItem_parabolicLens, self.menuItem_sphericalLens
        ]
        for item in comp_menu_items:
            self.Bind(wx.EVT_MENU, self.OnComponentMenuSelection, id=item.GetId())

        self._add_panels()

        sb = self.GetStatusBar() or self.CreateStatusBar(2)
        sb.SetFieldsCount(2)
        sb.SetStatusWidths([-1, 200])
        sb.SetStatusText("OpticsLAB Ready", 0)

        self._mgr.Update()
        self.Centre(wx.BOTH)

    def _add_panels(self):
        # Set Layer(1) for Left/Right panels so they extend full height, and Layer(0) for Bottom (Plots)
        # so it docks in the middle (up/down split with CentrePane simulation)
        self.panel_project_tree = ProjectFolderTreePanel(self)
        self._mgr.AddPane(self.panel_project_tree,
                          aui.AuiPaneInfo().Name("panel_project_folder_tree").Caption("Project Folder").Left().Layer(1).Position(
                              0).BestSize((300, 240)))

        self.panel_tree = ComponentPanel(self)
        self._mgr.AddPane(self.panel_tree,
                          aui.AuiPaneInfo().Name("panel_tree").Caption("Components").Left().Layer(1).Position(1).BestSize(
                              (300, -1)))

        self.panel_comp_tree = ComponentsTreePanel(self)
        self._mgr.AddPane(self.panel_comp_tree,
                          aui.AuiPaneInfo().Name("panel_components_tree").Caption("Components Tree").Left().Layer(1).Position(
                              2).BestSize((300, 240)))

        self.panel_props = PropertiesPanel(self)
        self._mgr.AddPane(self.panel_props,
                          aui.AuiPaneInfo().Name("panel_properties").Caption("Properties").Right().Layer(1).BestSize((280, -1)))

        self.panel_plots = PlotsPanel(self)
        self._mgr.AddPane(self.panel_plots,
                          aui.AuiPaneInfo().Name("panel_plots").Caption("Plots").Bottom().Layer(0).BestSize((-1, 260)))

        self.panel_sim = SimulationPanel(self)
        self._mgr.AddPane(self.panel_sim, aui.AuiPaneInfo().Name("panel_simulation").Caption("Simulation").CentrePane())

    def _toggle_pane(self, pane_name, show):
        pane = self._mgr.GetPane(pane_name)
        if pane.IsOk():
            pane.Show(show)
            self._mgr.Update()

    # ── Folder & File Operations ──────────────────────────────────────────────

    def OnFileOpenFolder(self, event):
        """Opens a Directory Dialog and updates the Project Folder Tree!"""
        with wx.DirDialog(self, "Open Project Workspace Folder",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                self.panel_project_tree.load_directory(path)
                self.GetStatusBar().SetStatusText(f"Workspace Loaded: {path}", 0)

    def OnFileOpenFile(self, event):
        """Opens a File Dialog and loads a TOML/JSON component configuration."""
        with wx.FileDialog(self, "Open Component Configuration File",
                           wildcard="Configuration files (*.toml;*.json)|*.toml;*.json|TOML files (*.toml)|*.toml|JSON files (*.json)|*.json",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                ext = os.path.splitext(path)[1].lower()
                try:
                    if ext == ".json":
                        data = load_json(path)
                    else:
                        data = load_toml(path)
                    name = data.get("name", "Component")
                    self.panel_props.set_properties(name, data)
                    self.GetStatusBar().SetStatusText(f"Loaded File: {path}", 0)
                except Exception as e:
                    wx.MessageBox(f"Failed to load file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def OnFileSave(self, event):
        """Saves current properties panel config to TOML/JSON."""
        data = self.panel_props.get_current_grid_data()
        if not data:
            wx.MessageBox("No active properties to save.", "Save Error", wx.OK | wx.ICON_ERROR)
            return
            
        with wx.FileDialog(self, "Save Component Configuration File",
                           wildcard="TOML files (*.toml)|*.toml|JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                ext = os.path.splitext(path)[1].lower()
                try:
                    if ext == ".json":
                        save_json(path, data)
                    else:
                        save_toml(path, data)
                    self.GetStatusBar().SetStatusText(f"Saved File: {path}", 0)
                except Exception as e:
                    wx.MessageBox(f"Failed to save file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    # ── Simulation & Properties Operations ────────────────────────────────────

    def OnComponentMenuSelection(self, event):
        item = self.GetMenuBar().FindItemById(event.GetId())
        if item:
            name = item.GetItemLabelText()
            self.show_component_properties(name)

    def show_component_properties(self, comp_name):
        preset = self.default_presets.get(comp_name)
        if not preset:
            for k, v in self.default_presets.items():
                if k.lower() in comp_name.lower():
                    preset = v
                    break
        if not preset:
            preset = {"name": comp_name, "center": [0.0, 0.0, 0.0], "radius": 1.0, "color": "green"}
        self.panel_props.set_properties(comp_name, preset)
        self.GetStatusBar().SetStatusText(f"Properties Loaded: {comp_name}", 0)

    def apply_properties(self, comp_name, data):
        if not hasattr(self.panel_sim, "canvas_obj") or not self.panel_sim.canvas_obj:
            wx.MessageBox("Simulation canvas not initialized yet.", "Error", wx.OK | wx.ICON_ERROR)
            return

        canvas = self.panel_sim.canvas_obj
        
        # Remove old visual nodes of the component if it exists
        if comp_name in self.active_components:
            old_comp = self.active_components[comp_name]
            if old_comp:
                if hasattr(old_comp, "surfaces"):
                    for surface in old_comp.surfaces:
                        if hasattr(surface, "get_Visual"):
                            surface.get_Visual().parent = None
                elif hasattr(old_comp, "get_Visual"):
                    old_comp.get_Visual().parent = None

        center = data.get("center", [0.0, 0.0, 0.0])
        from opticsLAB.raytracing.component.opticalPrimitives.Point import Point as OptPoint
        opt_center = OptPoint(center[0], center[1], center[2])
        radius = data.get("radius", 1.0)
        color_val = data.get("color", "blue")
        
        from vispy.color import Color as VisColor
        if isinstance(color_val, list):
            vis_color = VisColor(color=[c/255.0 for c in color_val[:3]])
        else:
            vis_color = VisColor(color=color_val)

        comp = None
        try:
            if "lens" in comp_name.lower():
                thickness = data.get("thickness", 0.5)
                mediumBefore = data.get("mediumBefore", "Air")
                mediumAfter = data.get("mediumAfter", "Air")
                
                if "spherical" in comp_name.lower() or "concave" in comp_name.lower() or "convex" in comp_name.lower():
                    from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
                    R1 = data.get("R1", 2.0)
                    R2 = data.get("R2", -2.0)
                    comp = SphericalLens(R1=R1, R2=R2, center=opt_center, radius=radius, thickness=thickness,
                                         mediumBefore=mediumBefore, mediumAfter=mediumAfter, color=vis_color,
                                         parentCanvas=canvas)
                elif "parabolic" in comp_name.lower():
                    from opticsLAB.raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
                    comp = ParabolicLens(center=opt_center, radius=radius, thickness=thickness,
                                         mediumBefore=mediumBefore, mediumAfter=mediumAfter, color=vis_color,
                                         parentCanvas=canvas)
                else:
                    from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
                    comp = SphericalLens(center=opt_center, radius=radius, thickness=thickness,
                                         mediumBefore=mediumBefore, mediumAfter=mediumAfter, color=vis_color,
                                         parentCanvas=canvas)
            else:
                xTilt = data.get("xTilt", 0.0)
                yTilt = data.get("yTilt", 0.0)
                mediumBefore = data.get("mediumBefore", "Air")
                mediumAfter = data.get("mediumAfter", "Air")
                
                if "parabolic" in comp_name.lower() or "paraboloid" in comp_name.lower():
                    from opticsLAB.raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
                    a = data.get("a", 1.0)
                    b = data.get("b", 1.0)
                    centerHoleRadius = data.get("centerHoleRadius", 0.0)
                    comp = Concave_Paraboloid(a=a, b=b, center=opt_center, radius=radius,
                                              centerHoleRadius=centerHoleRadius, xTilt=xTilt, yTilt=yTilt,
                                              mediumBefore=mediumBefore, mediumAfter=mediumAfter, color=vis_color,
                                              parentCanvas=canvas)
                elif "spherical" in comp_name.lower():
                    from opticsLAB.raytracing.component.primitives.sphericalSurface import Spherical_Surface
                    radius_of_curvature = data.get("radius_of_curvature", 2.0)
                    comp = Spherical_Surface(radius_of_curvature=radius_of_curvature, aperture_radius=radius,
                                             center=opt_center, xTilt=xTilt, yTilt=yTilt,
                                             mediumBefore=mediumBefore, mediumAfter=mediumAfter, color=vis_color,
                                             parentCanvas=canvas)
                else:
                    from opticsLAB.raytracing.component.primitives.plane import Plane
                    comp = Plane(radius=radius, width=2*radius, length=2*radius, center=opt_center,
                                 xTilt=xTilt, yTilt=yTilt, mediumBefore=mediumBefore, mediumAfter=mediumAfter,
                                 color=vis_color, parentCanvas=canvas)
            
            if comp:
                self.active_components[comp_name] = comp
                listbox = self.panel_tree.listBox_lst_components
                if listbox.FindString(comp_name) == wx.NOT_FOUND:
                    listbox.Append(comp_name)
                    
                canvas.canvas.update()
                self.GetStatusBar().SetStatusText(f"Added/Updated Component in 3D scene: {comp_name}", 0)
        except Exception as e:
            wx.MessageBox(f"Error instantiating component: {str(e)}", "Simulation Error", wx.OK | wx.ICON_ERROR)

    def tool_runOnToolClicked(self, event):
        """Traces test rays through active components and displays them in 3D, and updates diagram plots."""
        if hasattr(self, "ray_visuals"):
            for vis in self.ray_visuals:
                vis.parent = None
            self.ray_visuals.clear()
        else:
            self.ray_visuals = []
            
        if not self.active_components:
            wx.MessageBox("No active components in the system to simulate.", "Simulation Info", wx.OK | wx.ICON_INFORMATION)
            return

        canvas = self.panel_sim.canvas_obj
        if not canvas:
            return
            
        from opticsLAB.raytracing.component.sources import Ray as OptRay
        from opticsLAB.raytracing.component.opticalPrimitives.Point import Point as OptPoint
        
        y_offsets = np.linspace(-0.6, 0.6, 7)
        rays = []
        for y in y_offsets:
            ray_start = OptPoint(0.0, y, -2.0)
            ray_dir = np.array([0.0, 0.0, 1.0])
            ray = OptRay(ray_start, ray_dir, wavelength=0.55, color='yellow', parentCanvas=canvas)
            rays.append(ray)
            self.ray_visuals.append(ray.get_visual())
            
        sorted_comps = sorted(
            self.active_components.values(),
            key=lambda c: c.center[2] if hasattr(c, "center") else 0.0
        )
        
        for ray in rays:
            current_ray = ray
            for comp in sorted_comps:
                if current_ray is None:
                    break
                if "lens" in type(comp).__name__.lower():
                    next_ray = comp.calculate_RefractedRay(current_ray)
                else:
                    next_ray = comp.calculate_RefractedRay(current_ray)
                if next_ray:
                    self.ray_visuals.append(next_ray.get_visual())
                current_ray = next_ray
                
        canvas.canvas.update()
        self.panel_plots.update_plots()
        self.GetStatusBar().SetStatusText("Ray tracing simulation run complete.", 0)

    def tool_zoomOnToolClicked(self, event):
        """Cycles zoom levels for the simulation panel."""
        self.zoom_level += 0.2
        if self.zoom_level > 2.0:
            self.zoom_level = 0.5
            
        self.GetStatusBar().SetStatusText(f"Canvas Zoom: {int(self.zoom_level * 100)}%", 0)
        
        if hasattr(self.panel_sim, "canvas_obj") and self.panel_sim.canvas_obj:
            try:
                self.panel_sim.canvas_obj.view.camera.fov = 30.0 / self.zoom_level
                self.panel_sim.canvas_obj.canvas.update()
            except Exception as e:
                print("Zoom failed:", e)

    def reset_simulation_view(self):
        if hasattr(self.panel_sim, "canvas_obj") and self.panel_sim.canvas_obj:
            camera = self.panel_sim.canvas_obj.view.camera
            camera.center = (0, 0, 0)
            camera.elevation = 30
            camera.azimuth = 30
            camera.fov = 30
            self.zoom_level = 1.0
            self.panel_sim.canvas_obj.canvas.update()
            self.GetStatusBar().SetStatusText("Simulation view reset to origin.", 0)

    def tool_clearOnToolClicked(self, event):
        # Clear components and rays from canvas
        for comp in self.active_components.values():
            if hasattr(comp, "surfaces"):
                for surface in comp.surfaces:
                    if hasattr(surface, "get_Visual"):
                        surface.get_Visual().parent = None
            elif hasattr(comp, "get_Visual"):
                comp.get_Visual().parent = None
        self.active_components.clear()
        
        if hasattr(self, "ray_visuals"):
            for vis in self.ray_visuals:
                vis.parent = None
            self.ray_visuals.clear()
            
        self.panel_tree.listBox_lst_components.Clear()
        self.panel_props.m_propertyGrid2.Clear()
        self.panel_props.current_preset_data = {}
        
        self.panel_plots.draw_default_plots()
        self.reset_simulation_view()
        self.GetStatusBar().SetStatusText("System cleared and simulation view reset.", 0)

    def menuItem_reset_Layout1OnMenuSelection(self, event):
        self.reset_simulation_view()

    def menuItem_exitOnMenuSelection(self, event):
        self.Close()

    def menuItem_undoOnMenuSelection(self, event):
        self.GetStatusBar().SetStatusText("Undo", 0)

    def tool_undoOnToolClicked(self, event):
        self.GetStatusBar().SetStatusText("Undo", 0)

    def menuItem_redoOnMenuSelection(self, event):
        self.GetStatusBar().SetStatusText("Redo", 0)

    def tool_RedoOnToolClicked(self, event):
        self.GetStatusBar().SetStatusText("Redo", 0)

    def menuItem_view_componentsOnMenuSelection(self, event):
        self._toggle_pane("panel_tree", event.IsChecked())

    def menuItem_view_treeOnMenuSelection(self, event):
        self._toggle_pane("panel_components_tree", event.IsChecked())

    def menuItem_view_propertiesOnMenuSelection(self, event):
        self._toggle_pane("panel_properties", event.IsChecked())

    def menuItem_view_plotsOnMenuSelection(self, event):
        self._toggle_pane("panel_plots", event.IsChecked())

    def menuItem_view_simulationOnMenuSelection(self, event):
        self._toggle_pane("panel_simulation", event.IsChecked())


if __name__ == "__main__":
    app = wx.App(False)
    frame = OpticsLABFrame()
    frame.Show(True)
    app.MainLoop()

#new  modified
