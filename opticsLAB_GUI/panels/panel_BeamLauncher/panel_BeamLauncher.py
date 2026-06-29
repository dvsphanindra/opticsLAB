import os
import sys
import numpy as np
import wx

# ---------------------------------------------------------------------------
# OS-Agnostic Package & Module Path Resolution
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = os.path.dirname(BASE_DIR)
GUI_DIR = os.path.dirname(PANELS_DIR)
OPTICS_LAB_DIR = os.path.dirname(GUI_DIR)
WORKSPACE_ROOT = os.path.dirname(OPTICS_LAB_DIR)

for p in (BASE_DIR, PANELS_DIR, GUI_DIR, OPTICS_LAB_DIR, WORKSPACE_ROOT):
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

import vispy.app

vispy.app.use_app("wx")
from vispy import scene

from panel_BeamLauncher_GUI import panel_BeamLauncher_GUI

try:
    from opticsLAB.raytracing.component.sources import Ray, CircularBeam, Beam
    from opticsLAB.raytracing.component.primitives.miscellaneous import deg2DC, dc2deg
    from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
    from opticsLAB.raytracing.component.OpticsLabCanvas import OpticsLabCanvas
    from opticsLAB.raytracing.component.primitives.constants import (
        X_AXIS_DIRECTION, Y_AXIS_DIRECTION, Z_AXIS_DIRECTION,
        X_AXIS_NEG_DIRECTION, Y_AXIS_NEG_DIRECTION, Z_AXIS_NEG_DIRECTION,
        X_AXIS_DC, Y_AXIS_DC, Z_AXIS_DC,
        X_AXIS_NEG_DC, Y_AXIS_NEG_DC, Z_AXIS_NEG_DC
    )
except ImportError:
    from raytracing.component.sources import Ray, CircularBeam, Beam
    from raytracing.component.primitives.miscellaneous import deg2DC, dc2deg
    from raytracing.component.opticalPrimitives.Point import Point
    from raytracing.component.OpticsLabCanvas import OpticsLabCanvas
    from raytracing.component.primitives.constants import (
        X_AXIS_DIRECTION, Y_AXIS_DIRECTION, Z_AXIS_DIRECTION,
        X_AXIS_NEG_DIRECTION, Y_AXIS_NEG_DIRECTION, Z_AXIS_NEG_DIRECTION,
        X_AXIS_DC, Y_AXIS_DC, Z_AXIS_DC,
        X_AXIS_NEG_DC, Y_AXIS_NEG_DC, Z_AXIS_NEG_DC
    )

try:
    from opticsLAB_GUI.opticsLAB_support import color_to_vispy, remove_visual
except ImportError:
    try:
        from opticsLAB_support import color_to_vispy, remove_visual
    except ImportError:
        def color_to_vispy(c): return c
        def remove_visual(comp): pass


class panel_BeamLauncher(panel_BeamLauncher_GUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent

        # Flag to prevent infinite feedback loops between Angles and DCs
        self._is_updating = False

        # Canvas initialization variables
        self.canvas_initialized = False
        self.canvas_obj = None

        # Active beams tracking
        self.beams_list = []
        self.active_beams_dict = {}  # maps TreeItemId -> {"beam": beam_obj, "config": config_dict, "title": str}
        self.selected_beam_item = None
        self.beam_counter = 0

        # Setup Tree Control in m_scrolledWindow1 for listing beams
        self.setup_tree_control()

        # Bind events for Angles (updating Angles calculates DC)

        self.textCtrl_XAngle.Bind(wx.EVT_TEXT, self.OnAngleChanged)
        self.textCtrl_YAngle.Bind(wx.EVT_TEXT, self.OnAngleChanged)
        self.textCtrl_ZAngle.Bind(wx.EVT_TEXT, self.OnAngleChanged)

        # Bind events for Direction Cosines (updating DC calculates Angles)
        self.textCtrl_DC_l.Bind(wx.EVT_TEXT, self.OnDCChanged)
        self.textCtrl_DC_m.Bind(wx.EVT_TEXT, self.OnDCChanged)
        self.textCtrl_DC_n.Bind(wx.EVT_TEXT, self.OnDCChanged)

        # Bind window size event to initialize 3D Vispy canvas
        self.Bind(wx.EVT_SIZE, self.OnSize)
        wx.CallAfter(self._ensure_canvas)

        # Initial control visibility setup
        self.update_panel_visibility()

    def setup_tree_control(self):
        """Replaces or overlays the dataview list with a hierarchical wx.TreeCtrl in m_scrolledWindow1."""
        if hasattr(self, "dataViewListCtrl_ActiveBeamList"):
            self.dataViewListCtrl_ActiveBeamList.Hide()

        sizer = self.m_scrolledWindow1.GetSizer()
        self.treeCtrl_ActiveBeams = wx.TreeCtrl(
            self.m_scrolledWindow1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | wx.BORDER_SUNKEN
        )
        sizer.Add(self.treeCtrl_ActiveBeams, 1, wx.EXPAND | wx.ALL, 5)
        self.root_node = self.treeCtrl_ActiveBeams.AddRoot("Active Beams")

        # Bind tree selection and context menu events
        self.treeCtrl_ActiveBeams.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelectionChanged)
        self.treeCtrl_ActiveBeams.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnTreeRightClick)
        self.treeCtrl_ActiveBeams.Bind(wx.EVT_KEY_DOWN, self.OnTreeKeyDown)

        self.m_scrolledWindow1.Layout()

    def _ensure_canvas(self):
        """Initializes the 3D OpticsLabCanvas with XYZ axis indicators."""
        if self.canvas_initialized or (size := self.m_panel6.GetSize()).x <= 0 or size.y <= 0:
            return
        try:
            self.canvas_obj = OpticsLabCanvas(parent=self.m_panel6, bgColor="lightsteelblue")
            sim_sizer = wx.BoxSizer(wx.VERTICAL)
            sim_sizer.Add(self.canvas_obj.canvas.native, 1, wx.EXPAND)
            self.m_panel6.SetSizer(sim_sizer)
            self.m_panel6.Layout()
            self.canvas_obj.canvas.show()
            self.canvas_initialized = True
        except Exception as exc:
            print("Error initializing OpticsLabCanvas inside panel_BeamLauncher:", exc)

    def OnSize(self, event):
        event.Skip()
        if not self.canvas_initialized:
            wx.CallAfter(self._ensure_canvas)

    def update_panel_visibility(self):
        """Controls visibility and enablement of input panels based on selected beam type."""
        selection = self.choice_BeamLauncherType.GetStringSelection()

        if selection == "Single Ray":
            self.panel_RayCount.Hide()
            self.panel_Circle_Radius_Beam.Hide()
            self.panel_Rectangle_beam.Hide()
        elif selection == "Circular":
            self.panel_RayCount.Show()
            self.panel_RayCount.Enable(True)
            self.panel_Circle_Radius_Beam.Show()
            self.panel_Rectangle_beam.Hide()
        elif selection == "Rectangle":
            self.panel_RayCount.Show()
            self.panel_RayCount.Enable(True)
            self.panel_Circle_Radius_Beam.Hide()
            self.panel_Rectangle_beam.Show()
        elif selection == "Random":
            self.panel_RayCount.Show()
            self.panel_RayCount.Enable(True)
            self.panel_Circle_Radius_Beam.Hide()
            self.panel_Rectangle_beam.Hide()

        self.panel_BeamLauncherControls.Layout()
        self.Layout()

    def choice_BeamLauncherType_OnChoice(self, event):
        self.update_panel_visibility()
        event.Skip()

    def choice_DirectionRaysOnChoice(self, event):
        """Updates angle and DC text fields when a standard direction preset is chosen."""
        selection = self.choice_DirectionRays.GetStringSelection()
        dir_map = {
            "X_AXIS_DIRECTION": (X_AXIS_DIRECTION, X_AXIS_DC),
            "Y_AXIS_DIRECTION": (Y_AXIS_DIRECTION, Y_AXIS_DC),
            "Z_AXIS_DIRECTION": (Z_AXIS_DIRECTION, Z_AXIS_DC),
            "X_AXIS_NEG_DIRECTION": (X_AXIS_NEG_DIRECTION, X_AXIS_NEG_DC),
            "Y_AXIS_NEG_DIRECTION": (Y_AXIS_NEG_DIRECTION, Y_AXIS_NEG_DC),
            "Z_AXIS_NEG_DIRECTION": (Z_AXIS_NEG_DIRECTION, Z_AXIS_NEG_DC),
        }
        if selection in dir_map:
            angles, dc = dir_map[selection]
            self._is_updating = True
            try:
                self.textCtrl_XAngle.ChangeValue(f"{angles[0]:.1f}")
                self.textCtrl_YAngle.ChangeValue(f"{angles[1]:.1f}")
                self.textCtrl_ZAngle.ChangeValue(f"{angles[2]:.1f}")
                self.textCtrl_DC_l.ChangeValue(f"{dc[0]:.1f}")
                self.textCtrl_DC_m.ChangeValue(f"{dc[1]:.1f}")
                self.textCtrl_DC_n.ChangeValue(f"{dc[2]:.1f}")
            finally:
                self._is_updating = False
        event.Skip()

    def button_SelectColor_OnClick(self, event):
        """Opens a color picker dialog to select ray/beam color."""
        dialog = wx.ColourDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            colour = dialog.GetColourData().GetColour()
            hex_color = f"#{colour.Red():02x}{colour.Green():02x}{colour.Blue():02x}"
            self.textCtrl_Color.SetValue(hex_color)
        dialog.Destroy()
        event.Skip()

    def beam_Calculations(self):
        """Calculates DCs from Angles and updates the GUI."""
        if self._is_updating:
            return

        try:
            self._is_updating = True

            val_x = self.textCtrl_XAngle.GetValue().strip()
            val_y = self.textCtrl_YAngle.GetValue().strip()
            val_z = self.textCtrl_ZAngle.GetValue().strip()

            x = float(val_x) if val_x and val_x != '-' else 0.0
            y = float(val_y) if val_y and val_y != '-' else 0.0
            z = float(val_z) if val_z and val_z != '-' else 0.0

            angles = np.array([x, y, z])
            dc = deg2DC(angles)

            self.textCtrl_DC_l.ChangeValue(f"{dc[0]:.1f}")
            self.textCtrl_DC_m.ChangeValue(f"{dc[1]:.1f}")
            self.textCtrl_DC_n.ChangeValue(f"{dc[2]:.1f}")

        except (ValueError, AssertionError):
            self.textCtrl_DC_l.ChangeValue("---")
            self.textCtrl_DC_m.ChangeValue("---")
            self.textCtrl_DC_n.ChangeValue("---")
        finally:
            self._is_updating = False

    def dc_Calculations(self):
        """Calculates Angles from DCs and updates the GUI."""
        if self._is_updating:
            return

        try:
            self._is_updating = True

            val_l = self.textCtrl_DC_l.GetValue().strip()
            val_m = self.textCtrl_DC_m.GetValue().strip()
            val_n = self.textCtrl_DC_n.GetValue().strip()

            l = float(val_l) if val_l and val_l != '-' else 0.0
            m = float(val_m) if val_m and val_m != '-' else 0.0
            n = float(val_n) if val_n and val_n != '-' else 0.0

            dc = np.array([l, m, n])
            angles = np.degrees(dc2deg(dc))

            self.textCtrl_XAngle.ChangeValue(f"{angles[0]:.1f}")
            self.textCtrl_YAngle.ChangeValue(f"{angles[1]:.1f}")
            self.textCtrl_ZAngle.ChangeValue(f"{angles[2]:.1f}")

        except (ValueError, AssertionError):
            self.textCtrl_XAngle.ChangeValue("---")
            self.textCtrl_YAngle.ChangeValue("---")
            self.textCtrl_ZAngle.ChangeValue("---")
        finally:
            self._is_updating = False

    def OnAngleChanged(self, event):
        self.beam_Calculations()
        event.Skip()

    def OnDCChanged(self, event):
        self.dc_Calculations()
        event.Skip()

    def OnTreeSelectionChanged(self, event):
        """Populates GUI input controls with selected beam's parameters for editing."""
        item = event.GetItem()
        if not item.IsOk():
            return

        # If a child ray node is selected, target its parent beam node
        parent = self.treeCtrl_ActiveBeams.GetItemParent(item)
        target_item = item if not parent.IsOk() or parent == self.root_node else parent

        if target_item in self.active_beams_dict:
            self.selected_beam_item = target_item
            config = self.active_beams_dict[target_item]["config"]

            # Load configuration into input fields
            beam_type = config.get("beam_type", "Single Ray")
            self.choice_BeamLauncherType.SetStringSelection(beam_type)
            self.update_panel_visibility()

            pos = config.get("position", {})
            self.textCtrl_XPosition.SetValue(str(pos.get("x", 0.0)))
            self.textCtrl_YPosition.SetValue(str(pos.get("y", 0.0)))
            self.textCtrl_ZPosition.SetValue(str(pos.get("z", 0.0)))

            self.textCtrl_wavelength.SetValue(str(config.get("wavelength", 0.55)))
            self.textCtrl_Ray_Count.SetValue(str(config.get("ray_count", 1)))
            self.textCtrl_Ray_Count1.SetValue(str(config.get("radius", 0.0)))
            self.textCtrl_rectangle_length.SetValue(str(config.get("rectangle_length", 1.0)))
            self.textCtrl_rectangle_breath.SetValue(str(config.get("rectangle_breath", 1.0)))
            self.textCtrl_Color.SetValue(str(config.get("raw_color", "green")))

            is_degrees = config.get("degrees_mode", True)
            self.checkBox_Degrees.SetValue(is_degrees)

            angles = config.get("angles", {})
            self.textCtrl_XAngle.SetValue(str(angles.get("x", 90.0)))
            self.textCtrl_YAngle.SetValue(str(angles.get("y", 90.0)))
            self.textCtrl_ZAngle.SetValue(str(angles.get("z", 0.0)))

            dc_vals = config.get("dc", {})
            self.textCtrl_DC_l.SetValue(str(dc_vals.get("l", 0.0)))
            self.textCtrl_DC_m.SetValue(str(dc_vals.get("m", 0.0)))
            self.textCtrl_DC_n.SetValue(str(dc_vals.get("n", 1.0)))

            self.button_Addbeam.SetLabel("Update")
        else:
            self.selected_beam_item = None
            self.button_Addbeam.SetLabel("Add")

        event.Skip()

    def OnTreeRightClick(self, event):
        """Shows context menu on right click for Editing or Removing a Beam."""
        item = event.GetItem()
        if not item.IsOk() or item == self.root_node:
            return

        self.treeCtrl_ActiveBeams.SelectItem(item)
        menu = wx.Menu()
        item_edit = menu.Append(wx.ID_ANY, "Edit Beam Parameters")
        item_remove = menu.Append(wx.ID_ANY, "Remove Beam")

        self.Bind(wx.EVT_MENU, lambda e: self.OnTreeSelectionChanged(event), item_edit)
        self.Bind(wx.EVT_MENU, lambda e: self.remove_beam_by_item(item), item_remove)

        self.PopupMenu(menu)
        menu.Destroy()

    def OnTreeKeyDown(self, event):
        """Removes selected beam on pressing Delete key."""
        if event.GetKeyCode() == wx.WXK_DELETE:
            item = self.treeCtrl_ActiveBeams.GetSelection()
            if item.IsOk():
                self.remove_beam_by_item(item)
        event.Skip()

    def remove_beam_by_item(self, item):
        """Removes beam visuals from scene and deletes entry from active tracking tree."""
        if not item.IsOk():
            return
        parent = self.treeCtrl_ActiveBeams.GetItemParent(item)
        target_item = item if not parent.IsOk() or parent == self.root_node else parent

        if target_item in self.active_beams_dict:
            beam_entry = self.active_beams_dict.pop(target_item)
            beam_obj = beam_entry["beam"]

            if beam_obj in self.beams_list:
                self.beams_list.remove(beam_obj)

            remove_visual(beam_obj)
            self.treeCtrl_ActiveBeams.Delete(target_item)
            self.selected_beam_item = None
            self.button_Addbeam.SetLabel("Add")

            total_rays = sum(len(b.get_Rays()) for b in self.beams_list)
            self.staticText_RayCount.SetLabel(f"     {total_rays}       ")

            if self.canvas_obj and hasattr(self.canvas_obj, "canvas"):
                self.canvas_obj.canvas.update()

    def button_remove_List_BeamOnButtonClick(self, event):
        """Handler for wxFormBuilder native Remove button click."""
        item = self.treeCtrl_ActiveBeams.GetSelection()
        if item.IsOk():
            self.remove_beam_by_item(item)
        elif self.selected_beam_item and self.selected_beam_item.IsOk():
            self.remove_beam_by_item(self.selected_beam_item)
        else:
            wx.MessageBox("Please select a beam from the Active Beams list to remove.", "Info", wx.OK | wx.ICON_INFORMATION)
        event.Skip()


    def print_gui_values(self, event=None):
        values = {
            "beam_type": self.choice_BeamLauncherType.GetStringSelection(),
            "ray_count": self.textCtrl_Ray_Count.GetValue(),
            "separation": self.m_textCtrl8.GetValue(),
            "wavelength": self.textCtrl_wavelength.GetValue(),
            "radius": self.textCtrl_Ray_Count1.GetValue(),
            "rectangle_length": self.textCtrl_rectangle_length.GetValue(),
            "rectangle_breath": self.textCtrl_rectangle_breath.GetValue(),
            "direction": self.choice_DirectionRays.GetStringSelection(),
            "position": {
                "x": self.textCtrl_XPosition.GetValue(),
                "y": self.textCtrl_YPosition.GetValue(),
                "z": self.textCtrl_ZPosition.GetValue(),
            },
            "degrees_mode": bool(self.checkBox_Degrees.GetValue()),
            "angles": {
                "x": self.textCtrl_XAngle.GetValue(),
                "y": self.textCtrl_YAngle.GetValue(),
                "z": self.textCtrl_ZAngle.GetValue(),
            },
            "dc": {
                "l": self.textCtrl_DC_l.GetValue(),
                "m": self.textCtrl_DC_m.GetValue(),
                "n": self.textCtrl_DC_n.GetValue(),
            },
            "color": self.textCtrl_Color.GetValue(),
            "total_ray_count_text": self.staticText_RayCount.GetLabel(),
        }
        return values

    def button_AddBeam_OnButtonClick(self, event):
        """Extracts parameters from GUI, constructs or updates beam object, renders on canvas, and updates tree view."""
        self.beam_Calculations()

        try:
            # Parse center position
            px = float(self.textCtrl_XPosition.GetValue().strip() or 0.0)
            py = float(self.textCtrl_YPosition.GetValue().strip() or 0.0)
            pz = float(self.textCtrl_ZPosition.GetValue().strip() or 0.0)
            center = Point((px, py, pz))

            # Parse wavelength & color
            wl_str = self.textCtrl_wavelength.GetValue().strip()
            wavelength = float(wl_str) if wl_str else 0.55
            raw_color = self.textCtrl_Color.GetValue().strip() or "green"
            color = color_to_vispy(raw_color)

            # Standard ray propagation length in scene
            ray_length = 15.0

            # Parse direction and DC mode (Degrees checkbox checked -> dc=False)
            is_degrees = bool(self.checkBox_Degrees.GetValue())
            use_dc = not is_degrees

            if use_dc:
                l = float(self.textCtrl_DC_l.GetValue().strip() or 0.0)
                m = float(self.textCtrl_DC_m.GetValue().strip() or 0.0)
                n = float(self.textCtrl_DC_n.GetValue().strip() or 1.0)
                beam_direction = np.array([l, m, n])
            else:
                ax = float(self.textCtrl_XAngle.GetValue().strip() or 90.0)
                ay = float(self.textCtrl_YAngle.GetValue().strip() or 90.0)
                az = float(self.textCtrl_ZAngle.GetValue().strip() or 0.0)
                beam_direction = np.array([ax, ay, az])

            beam_type = self.choice_BeamLauncherType.GetStringSelection()
            created_beam = None

            if beam_type == "Single Ray":
                ray = Ray(
                    startPoint=center,
                    rayDirection=beam_direction,
                    dc=use_dc,
                    wavelength=wavelength,
                    length=ray_length,
                    color=color,
                    parentCanvas=self.canvas_obj
                )
                created_beam = Beam(parentCanvas=self.canvas_obj)
                created_beam.addRay(ray)

            elif beam_type == "Circular":
                rad_str = self.textCtrl_Ray_Count1.GetValue().strip()
                radius = float(rad_str) if rad_str else 0.0

                rc_str = self.textCtrl_Ray_Count.GetValue().strip()
                no_of_rays = int(rc_str) if rc_str else 1

                created_beam = CircularBeam(
                    center=center,
                    radius=radius,
                    noOfRays=no_of_rays,
                    centerRay=True,
                    wavelength=wavelength,
                    beamDirection=beam_direction,
                    dc=use_dc,
                    length=ray_length,
                    color=color,
                    parentCanvas=self.canvas_obj
                )

            elif beam_type == "Rectangle":
                len_str = self.textCtrl_rectangle_length.GetValue().strip()
                rect_len = float(len_str) if len_str else 1.0

                br_str = self.textCtrl_rectangle_breath.GetValue().strip()
                rect_br = float(br_str) if br_str else 1.0

                rc_str = self.textCtrl_Ray_Count.GetValue().strip()
                no_of_rays = int(rc_str) if rc_str else 1

                nx = max(1, int(np.sqrt(no_of_rays)))
                ny = max(1, int(np.ceil(no_of_rays / nx)))
                xs = np.linspace(-rect_len / 2.0, rect_len / 2.0, nx)
                ys = np.linspace(-rect_br / 2.0, rect_br / 2.0, ny)

                ray_locations = []
                count = 0
                center_coords = center.get_coordinates()
                for x_off in xs:
                    for y_off in ys:
                        if count >= no_of_rays:
                            break
                        pt_pos = center_coords + np.array([x_off, y_off, 0.0])
                        ray_locations.append(Point(pt_pos))
                        count += 1

                created_beam = Beam(
                    rayLocations=ray_locations,
                    noOfRays=len(ray_locations),
                    wavelength=wavelength,
                    beamDirection=beam_direction,
                    dc=use_dc,
                    length=ray_length,
                    color=color,
                    parentCanvas=self.canvas_obj
                )

            elif beam_type == "Random":
                rc_str = self.textCtrl_Ray_Count.GetValue().strip()
                no_of_rays = int(rc_str) if rc_str else 1

                ray_locations = []
                center_coords = center.get_coordinates()
                for _ in range(no_of_rays):
                    rand_offset = (np.random.rand(3) - 0.5) * 2.0
                    ray_locations.append(Point(center_coords + rand_offset))

                created_beam = Beam(
                    rayLocations=ray_locations,
                    noOfRays=len(ray_locations),
                    wavelength=wavelength,
                    beamDirection=beam_direction,
                    dc=use_dc,
                    length=ray_length,
                    color=color,
                    parentCanvas=self.canvas_obj
                )

            if created_beam:
                config_data = {
                    "beam_type": beam_type,
                    "position": {"x": px, "y": py, "z": pz},
                    "wavelength": wavelength,
                    "raw_color": raw_color,
                    "degrees_mode": is_degrees,
                    "angles": {"x": self.textCtrl_XAngle.GetValue(), "y": self.textCtrl_YAngle.GetValue(), "z": self.textCtrl_ZAngle.GetValue()},
                    "dc": {"l": self.textCtrl_DC_l.GetValue(), "m": self.textCtrl_DC_m.GetValue(), "n": self.textCtrl_DC_n.GetValue()},
                    "ray_count": self.textCtrl_Ray_Count.GetValue(),
                    "radius": self.textCtrl_Ray_Count1.GetValue(),
                    "rectangle_length": self.textCtrl_rectangle_length.GetValue(),
                    "rectangle_breath": self.textCtrl_rectangle_breath.GetValue()
                }

                # If updating an existing selected beam
                if self.selected_beam_item and self.selected_beam_item.IsOk() and self.selected_beam_item in self.active_beams_dict:
                    old_entry = self.active_beams_dict[self.selected_beam_item]
                    remove_visual(old_entry["beam"])
                    if old_entry["beam"] in self.beams_list:
                        self.beams_list.remove(old_entry["beam"])

                    self.beams_list.append(created_beam)
                    self.treeCtrl_ActiveBeams.DeleteChildren(self.selected_beam_item)

                    beam_title = f"{old_entry['title'].split(':')[0]}: {beam_type} ({len(created_beam.get_Rays())} Rays)"
                    self.treeCtrl_ActiveBeams.SetItemText(self.selected_beam_item, beam_title)

                    for i, ray in enumerate(created_beam.get_Rays(), 1):
                        start_coords = np.round(ray.lineStart_point, 2)
                        dir_coords = np.round(ray.get_Direction_Cosines(), 2)
                        ray_info = f"Ray {i}: Start={start_coords.tolist()}, Dir={dir_coords.tolist()}"
                        self.treeCtrl_ActiveBeams.AppendItem(self.selected_beam_item, ray_info)

                    self.treeCtrl_ActiveBeams.Expand(self.selected_beam_item)
                    self.active_beams_dict[self.selected_beam_item] = {"beam": created_beam, "config": config_data, "title": beam_title}
                else:
                    # Creating a brand new beam
                    self.beams_list.append(created_beam)
                    self.beam_counter += 1

                    beam_title = f"Beam {self.beam_counter}: {beam_type} ({len(created_beam.get_Rays())} Rays)"
                    beam_node = self.treeCtrl_ActiveBeams.AppendItem(self.root_node, beam_title)

                    for i, ray in enumerate(created_beam.get_Rays(), 1):
                        start_coords = np.round(ray.lineStart_point, 2)
                        dir_coords = np.round(ray.get_Direction_Cosines(), 2)
                        ray_info = f"Ray {i}: Start={start_coords.tolist()}, Dir={dir_coords.tolist()}"
                        self.treeCtrl_ActiveBeams.AppendItem(beam_node, ray_info)

                    self.treeCtrl_ActiveBeams.Expand(beam_node)
                    self.active_beams_dict[beam_node] = {"beam": created_beam, "config": config_data, "title": beam_title}

                # Reset button label and selection
                self.selected_beam_item = None
                self.button_Addbeam.SetLabel("Add")

                # Update total ray count label
                total_rays = sum(len(b.get_Rays()) for b in self.beams_list)
                self.staticText_RayCount.SetLabel(f"     {total_rays}       ")

                # Refresh canvas & adjust view to center on new beam
                if self.canvas_obj and hasattr(self.canvas_obj, "canvas"):
                    try:
                        self.canvas_obj.view.camera.center = center.get_coordinates()
                    except Exception:
                        pass
                    self.canvas_obj.canvas.update()

        except Exception as err:
            wx.MessageBox(f"Error adding beam: {str(err)}", "Error", wx.OK | wx.ICON_ERROR)

        event.Skip()

    def textCtrl_Ray_CountOnTextEnter(self, event):
        event.Skip()

    def textCtrl_Ray_Count_OnTextEnter(self, event):
        event.Skip()

    def textCtrl_wavelengthOnTextEnter(self, event):
        event.Skip()

    def textCtrl_Position_OnTextEnter(self, event):
        event.Skip()

    def textCtrl_Angle_OnTextEnter(self, event):
        event.Skip()

    def textCtrl_DC_lOnTextEnter(self, event):
        event.Skip()

    def checkBox_Degrees_OnCheck(self, event):
        event.Skip()


class mainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="OpticsLAB - Beam Launcher Test Workspace",
                          pos=wx.DefaultPosition, size=wx.Size(950, 600),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.panel_BeamLauncher = panel_BeamLauncher(self)
        bSizer1.Add(self.panel_BeamLauncher, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Populate initial tracking entries based on default values
        self.panel_BeamLauncher.beam_Calculations()


if __name__ == "__main__":
    app = wx.App(False)
    GUI = mainFrame(None)
    GUI.Raise()
    GUI.Show(True)
    app.MainLoop()


