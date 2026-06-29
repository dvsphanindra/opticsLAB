"""
OpticsLAB - Main Window File.
Simple and clean code for managing panels, menus, and 3D simulation window.
"""

import os
import sys
import numpy as np
import vispy.app
vispy.app.use_app("wx")
import vispy.scene.cameras as cams

import wx
import wx.lib.agw.aui as aui

# Setup folder paths so Python can find all project modules easily
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OPTICS_LAB_DIR = os.path.dirname(BASE_DIR)
WORKSPACE_ROOT = os.path.dirname(OPTICS_LAB_DIR)
PANELS_DIR = os.path.join(BASE_DIR, "panels")

for path in (WORKSPACE_ROOT, OPTICS_LAB_DIR, BASE_DIR):
    if os.path.exists(path):
        while path in sys.path:
            sys.path.remove(path)

for path in reversed([WORKSPACE_ROOT, OPTICS_LAB_DIR]):
    if os.path.exists(path):
        sys.path.insert(0, path)
sys.path.append(BASE_DIR)

if os.path.isdir(PANELS_DIR):
    if PANELS_DIR not in sys.path:
        sys.path.append(PANELS_DIR)
    for folder in os.listdir(PANELS_DIR):
        full_folder_path = os.path.join(PANELS_DIR, folder)
        if os.path.isdir(full_folder_path):
            if full_folder_path not in sys.path:
                sys.path.append(full_folder_path)

os.environ.setdefault("WXSUPPRESS_SIZER_FLAGS_CHECK", "1")

from opticsLAB_support import (
    DEFAULT_PRESETS, color_to_vispy, remove_visual, resolve_template_name
)
from opticsLAB_GUI import MyFrame_opticsLAB_GUI
from tool_opticsLAB import ToolOpticsLABMixin
from menu_opticsLAB import MenuOpticsLABMixin
from simulation_engine import SimulationEngine

from panel_project_folder_tree import ProjectFolderTreePanel
from panel_component import ComponentPanel
from panel_components_tree import ComponentsTreePanel
from panel_properties import PropertiesPanel
from panel_plots import PlotsPanel
from panel_simulation import SimulationPanel
from panel_findcomponents import ComponentSearchDialog
from panel_BeamLauncher import panel_BeamLauncher

try:
    from opticsLAB.raytracing.component.opticalPrimitives.Point import Point as OptPoint
except ImportError:
    from raytracing.component.opticalPrimitives.Point import Point as OptPoint


# Main application window frame
class OpticsLABFrame(ToolOpticsLABMixin, MenuOpticsLABMixin, MyFrame_opticsLAB_GUI):
    
    # Map of panel names to their corresponding menu items
    PANE_MENU_MAP = {
        "panel_project_folder_tree": "menuItem_view_project_tree",
        "panel_beam_launcher": "menuItem_view_beam_launcher",
        "panel_tree": "menuItem_view_components",
        "panel_components_tree": "menuItem_view_tree",
        "panel_properties": "menuItem_view_properties",
        "panel_plots": "menuItem_view_plots",
        "panel_simulation": "menuItem_view_simulation"
    }

    # Initialize the main window and set up all controls
    def __init__(self, parent=None):
        super().__init__(parent)
        self.SetTitle("OpticsLAB")
        self.SetSize(wx.Size(1280, 800))
        self.SetMinSize(wx.Size(900, 600))

        self.zoom_level = 1.0
        self.active_components = {}
        self.active_component_configs = {}
        self.ray_visuals = []
        self.last_traced_rays = []
        self.default_presets = DEFAULT_PRESETS
        self.current_project_filepath = None
        self.undo_stack = []
        self.redo_stack = []

        # Default settings for camera and project metadata
        self.project_info = {
            "Name": "OpticsLAB Workspace",
            "Designer": "Optical Engineer",
            "Approver": "Lead Architect",
            "Description": "Optical Simulation Project",
            "Vispy_elevation": 30.0,
            "Vispy_azimuth": 30.0,
            "Vispy_zoom": 1.0,
            "Vispy_camera": "Turntable (3D Orbit)",
            "vispy_camera": "Turntable (3D Orbit)",
            "Vispy_bg_color": "lightsteelblue"
        }

        # Setup simulation engine and layout manager
        self.engine = SimulationEngine(self)
        self._mgr = aui.AuiManager(self)
        self._mgr.SetAGWFlags(aui.AUI_MGR_DEFAULT | aui.AUI_MGR_TRANSPARENT_HINT | aui.AUI_MGR_LIVE_RESIZE | aui.AUI_MGR_ALLOW_FLOATING | aui.AUI_MGR_HINT_FADE)
        self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)

        # Create menu items for Project Folder Tree and Beam Launcher
        self.menuItem_view_project_tree = wx.MenuItem(self.menu_View, wx.ID_ANY, "Show Project Folder Tree\tCtrl+6", "", wx.ITEM_CHECK)
        self.menu_View.Insert(0, self.menuItem_view_project_tree)
        self.menuItem_view_project_tree.Check(True)
        self.Bind(wx.EVT_MENU, lambda event: self._toggle_pane("panel_project_folder_tree", event.IsChecked()), id=self.menuItem_view_project_tree.GetId())

        self.menuItem_view_beam_launcher = wx.MenuItem(self.menu_View, wx.ID_ANY, "Show Beam Launcher Panel\tCtrl+7", "", wx.ITEM_CHECK)
        self.menu_View.Insert(1, self.menuItem_view_beam_launcher)
        self.menuItem_view_beam_launcher.Check(True)
        self.Bind(wx.EVT_MENU, lambda event: self._toggle_pane("panel_beam_launcher", event.IsChecked()), id=self.menuItem_view_beam_launcher.GetId())

        # Add side panels and update recent files menu
        self._add_panels()
        self.update_recent_files_menu()

        # Setup status bar at the bottom
        status_bar = self.GetStatusBar()
        if status_bar is None:
            status_bar = self.CreateStatusBar(2)
        status_bar.SetFieldsCount(2)
        status_bar.SetStatusWidths([-1, 200])
        status_bar.SetStatusText("OpticsLAB Ready", 0)
        
        self._mgr.Update()
        self.Centre(wx.BOTH)
        wx.CallAfter(self.show_project_properties)

    # Adds all side panels and center simulation canvas into dockable areas
    def _add_panels(self):
        panes_list = [
            (ProjectFolderTreePanel(self), "panel_project_folder_tree", "Project Folder", aui.AuiPaneInfo().Left().Layer(1).Position(0).BestSize((300, 240))),
            (ComponentPanel(self), "panel_tree", "Components", aui.AuiPaneInfo().Left().Layer(1).Position(1).BestSize((300, -1))),
            (ComponentsTreePanel(self), "panel_components_tree", "Components Tree", aui.AuiPaneInfo().Left().Layer(1).Position(2).BestSize((300, 240))),
            (panel_BeamLauncher(self), "panel_beam_launcher", "Beam Launcher", aui.AuiPaneInfo().Left().Layer(1).Position(3).BestSize((300, 280))),
            (PropertiesPanel(self), "panel_properties", "Properties", aui.AuiPaneInfo().Right().Layer(1).BestSize((280, -1))),
            (PlotsPanel(self), "panel_plots", "Plots", aui.AuiPaneInfo().Bottom().Layer(0).BestSize((-1, 220))),
            (SimulationPanel(self), "panel_simulation", "3D Simulation View", aui.AuiPaneInfo().Center().Layer(0).Position(0).BestSize((600, 400)))
        ]
        
        for panel_object, name_string, caption_title, pane_info in panes_list:
            setattr(self, name_string, panel_object)
            info = pane_info.Name(name_string).Caption(caption_title).CloseButton(True).MaximizeButton(True).MinimizeButton(True).Dockable(True).Floatable(True).Movable(True)
            self._mgr.AddPane(panel_object, info)
            
        self._default_perspective = self._mgr.SavePerspective()

    # Makes sure View menu checkmarks match whether panels are visible or hidden
    def sync_pane_menu_checks(self):
        for pane_name, menu_attr in self.PANE_MENU_MAP.items():
            if hasattr(self, menu_attr):
                item = getattr(self, menu_attr)
                if item:
                    pane = self._mgr.GetPane(pane_name)
                    if pane.IsOk():
                        is_visible = pane.IsShown() and not pane.IsMinimized()
                        item.Check(is_visible)

    # When user clicks close button on a panel frame, uncheck its menu item
    def OnPaneClose(self, event):
        pane = event.GetPane()
        if pane:
            pane_name = pane.name
            if pane_name in self.PANE_MENU_MAP:
                menu_attr = self.PANE_MENU_MAP[pane_name]
                if hasattr(self, menu_attr):
                    item = getattr(self, menu_attr)
                    if item:
                        item.Check(False)
        event.Skip()

    # Shows or hides a panel when selected from the View menu
    def _toggle_pane(self, pane_name, show=None):
        pane = self._mgr.GetPane(pane_name)
        if pane.IsOk():
            if show is None:
                new_state = not pane.IsShown()
            else:
                new_state = bool(show)
            
            if new_state == True:
                if pane.IsMinimized():
                    self._mgr.RestorePane(pane)
                pane.Show(True)
            else:
                pane.Show(False)
            
            self._mgr.Update()
            self.sync_pane_menu_checks()

    # Keeps component order synced with the listbox
    def sync_component_order_from_listbox(self):
        lb = self.panel_tree.listBox_lst_components
        names = []
        for i in range(lb.GetCount()):
            names.append(lb.GetString(i))
            
        new_comps = {}
        new_configs = {}
        for name in names:
            if name in self.active_components:
                new_comps[name] = self.active_components[name]
            if name in self.active_component_configs:
                new_configs[name] = self.active_component_configs[name]
                
        self.active_components = new_comps
        self.active_component_configs = new_configs
        self.panel_components_tree.update_tree()

    # Handles menu clicks for creating optical presets
    def OnComponentMenuSelection(self, event):
        item_id = event.GetId()
        item = self.GetMenuBar().FindItemById(item_id)
        if item:
            self.show_component_properties(item.GetItemLabelText())

    # Updates component settings and recreates its 3D visual object
    def update_component_instance(self, target_name, data, record_undo=True):
        if record_undo == True:
            self.push_undo_state()
            
        old_comp = self.active_components.pop(target_name, None)
        if old_comp:
            remove_visual(old_comp)

        new_name = str(data.get("name", target_name))
        if new_name != target_name:
            self.active_component_configs.pop(target_name, None)
        self.active_component_configs[new_name] = data.copy()

        canvas = self.panel_simulation.canvas_obj
        center_val = data.get("center", [0.0, 0.0, 0.0])
        opt_center = OptPoint(center_val[0], center_val[1], center_val[2])
        radius_val = float(data.get("radius", 1.0))
        color_val = color_to_vispy(data.get("color", "#00ff00ff"))
        type_str = str(data.get("type", new_name)).lower()

        comp_obj = self.engine.instantiate_component(
            comp_name=new_name,
            name_lower=type_str,
            data=data,
            opt_center=opt_center,
            radius=radius_val,
            vis_color=color_val,
            canvas=canvas
        )
        self.active_components[new_name] = comp_obj
        
        lb = self.panel_tree.listBox_lst_components
        if target_name != new_name:
            idx = lb.FindString(target_name)
            if idx != wx.NOT_FOUND:
                lb.SetString(idx, new_name)
            elif lb.FindString(new_name) == wx.NOT_FOUND:
                lb.Append(new_name)
        else:
            if lb.FindString(new_name) == wx.NOT_FOUND:
                lb.Append(new_name)

        if canvas:
            canvas.canvas.update()
        self.run_simulation(user_initiated=False)
        self.panel_components_tree.update_tree()

    # Changes 3D viewport camera type
    def configure_canvas_camera(self, camera_type="turntable", fov=30, elevation=30, azimuth=30):
        if not hasattr(self, "panel_simulation"):
            return
        if not self.panel_simulation.canvas_obj:
            return
            
        canvas = self.panel_simulation.canvas_obj
        cam_str = str(camera_type).lower()
        
        try:
            if "arcball" in cam_str:
                cam = cams.ArcballCamera(fov=fov)
            elif "pan" in cam_str or "2d" in cam_str:
                cam = cams.PanZoomCamera()
            else:
                cam = cams.TurntableCamera(fov=fov, up='y')
                if hasattr(cam, "elevation"):
                    cam.elevation = elevation
                if hasattr(cam, "azimuth"):
                    cam.azimuth = azimuth
                    
            if not hasattr(cam, "_distance") or getattr(cam, "_distance", None) is None:
                try:
                    setattr(cam, "_distance", 10.0)
                except Exception:
                    pass
            canvas.view.camera = cam
            canvas.canvas.update()
        except Exception as exc:
            print("Error configuring camera:", exc)

    # Runs light ray simulation
    def run_simulation(self, user_initiated=True):
        self.engine.run_simulation(user_initiated=user_initiated)

    # Resets camera back to default origin
    def reset_simulation_view(self):
        if hasattr(self, "panel_simulation") and self.panel_simulation.canvas_obj:
            canvas = self.panel_simulation.canvas_obj
            self.configure_canvas_camera("turntable")
            canvas.view.camera.center = (0, 0, 0)
            self.zoom_level = 1.0
            canvas.canvas.update()
            self.GetStatusBar().SetStatusText("Simulation view reset to origin.", 0)

    # Ask user to save work before closing app
    def OnCloseWindow(self, event):
        if len(self.active_components) > 0 or len(self.undo_stack) > 0:
            dlg = wx.MessageDialog(self, "Do you want to save project changes before exiting?", "Save & Close Confirmation", wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            dlg.Destroy()
            
            if res == wx.ID_YES:
                self.OnFileSave(None)
            elif res == wx.ID_CANCEL:
                if event.CanVeto():
                    event.Veto()
                return
        else:
            dlg = wx.MessageDialog(self, "Are you sure you want to close OpticsLAB?", "Confirm Exit", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            dlg.Destroy()
            if res != wx.ID_YES:
                if event.CanVeto():
                    event.Veto()
                return
                
        self._mgr.UnInit()
        event.Skip()

    # Shows project properties in inspector
    def show_project_properties(self):
        if hasattr(self, "panel_properties"):
            self.panel_properties.show_project_properties()

    # Applies workspace settings to viewport
    def apply_project_properties(self, data=None):
        if hasattr(self, "panel_properties"):
            self.panel_properties.apply_project_properties(data)

    # Displays single ray properties
    def show_ray_properties(self, parent_comp_name, ray_idx):
        if hasattr(self, "panel_properties"):
            self.panel_properties.show_ray_properties(parent_comp_name, ray_idx)

    # Updates single ray parameters
    def update_ray_instance(self, parent_comp_name, ray_idx, data, record_undo=True):
        if record_undo == True:
            self.push_undo_state()
            
        if parent_comp_name not in self.active_components:
            return
            
        comp = self.active_components[parent_comp_name]
        if not hasattr(comp, "get_Rays") or not callable(comp.get_Rays):
            return
            
        rays = comp.get_Rays()
        if 0 <= ray_idx < len(rays):
            ray = rays[ray_idx]
            ray.color = color_to_vispy(data.get("color", "#00ff00ff"))
            if "wavelength" in data:
                ray.wavelength = float(data["wavelength"])
            if "length" in data:
                ray.length = float(data["length"])
            if "center" in data and hasattr(ray, "translate"):
                try:
                    center_arr = np.array(data["center"], dtype=float)
                    ray.translate(center_arr)
                except Exception:
                    pass
            if "direction" in data and hasattr(ray, "set_Direction_Cosines"):
                try:
                    dir_arr = np.array(data["direction"], dtype=float)
                    ray.set_Direction_Cosines(dir_arr)
                except Exception:
                    pass
            if hasattr(ray, "create_Vector"):
                try:
                    ray.create_Vector()
                except Exception:
                    pass
                    
            canvas = getattr(self.panel_simulation, "canvas_obj", None)
            if canvas:
                canvas.canvas.update()
            self.run_simulation(user_initiated=False)
            self.panel_components_tree.update_tree()

    # Opens component properties panel
    def show_component_properties(self, comp_name, instantiate=True):
        if hasattr(self, "panel_properties"):
            self.panel_properties.show_component_properties(comp_name, instantiate=instantiate)

    # Opens search dialog to find components or presets
    def on_search_find_components(self, event=None):
        active_list = list(self.active_components.keys())
        preset_list = list(self.default_presets.keys())
        
        dlg = ComponentSearchDialog(self, active_list, preset_list)
        if dlg.ShowModal() == wx.ID_OK and dlg.selected_item:
            sel = dlg.selected_item
            if sel in self.active_components:
                lb = self.panel_tree.listBox_lst_components
                idx = lb.FindString(sel)
                if idx != wx.NOT_FOUND:
                    lb.SetSelection(idx)
                self.show_component_properties(sel, instantiate=False)
                self.GetStatusBar().SetStatusText(f"Found active component: {sel}", 0)
            else:
                self.show_component_properties(sel, instantiate=True)
                self.GetStatusBar().SetStatusText(f"Selected preset template: {sel}", 0)
        dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = OpticsLABFrame()
    frame.Show(True)
    app.MainLoop()
