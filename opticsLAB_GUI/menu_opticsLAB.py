"""
Menu-related event handlers and workspace file management for OpticsLAB GUI menu bar selections.
"""
import copy
import json
import os
import subprocess
import sys
import webbrowser
import wx

from opticsLAB_support import (
    add_recent_file, color_to_vispy, load_recent_files, load_toml,
    remove_visual, resolve_template_name, save_toml
)

try:
    from opticsLAB.raytracing.component.opticalPrimitives.Point import Point as OptPoint
except ImportError:
    from raytracing.component.opticalPrimitives.Point import Point as OptPoint


class MenuOpticsLABMixin:
    """
    Mixin class containing event handler callbacks for menu bar items and workspace file management.
    """
    # File Menu Delegates
    def menuItem_newOnMenuSelection(self, event): self.tool_clearOnToolClicked(event)
    def menuItem_openFileOnMenuSelection(self, event): self.OnFileOpenFile(event)
    def menuItem_closeFileOnMenuSelection(self, event): wx.MessageBox("Close File selected.", "Info", wx.OK | wx.ICON_INFORMATION)
    def menuItem_openFolderOnMenuSelection(self, event): self.OnFileOpenFolder(event)
    def menuItem_closefolderOnMenuSelection(self, event): self.OnFileCloseFolder(event)
    def menuItem_saveOnMenuSelection(self, event): self.OnFileSave(event)
    def menuItem_saveAsOnMenuSelection(self, event): self.OnFileSaveAs(event)
    def menuItem_exitOnMenuSelection(self, event): self.Close()

    # View & Layout Menu Delegates
    def menuItem_view_project_treeOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_project_folder_tree", is_checked)

    def menuItem_view_beam_launcherOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_beam_launcher", is_checked)

    def menuItem_view_componentsOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_tree", is_checked)

    def menuItem_view_treeOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_components_tree", is_checked)

    def menuItem_view_propertiesOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_properties", is_checked)

    def menuItem_view_plotsOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_plots", is_checked)

    def menuItem_view_simulationOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self._toggle_pane("panel_simulation", is_checked)

    def menuItem_view_fullScreenOnMenuSelection(self, event):
        is_checked = event.IsChecked()
        self.ShowFullScreen(is_checked)

    def menuItem_ModeOnMenuSelection(self, event):
        wx.MessageBox("Dark / Light Mode toggling functionality.", "Info", wx.OK | wx.ICON_INFORMATION)
    def menuItem_save_LayoutOnMenuSelection(self, event):
        with wx.FileDialog(self, "Save Workspace Layout", wildcard="Layout files (*.layout)|*.layout", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    perspective = self._mgr.SavePerspective()
                    with open(dlg.GetPath(), "w", encoding="utf-8") as h:
                        h.write(perspective)
                    self.GetStatusBar().SetStatusText(f"Layout saved: {dlg.GetPath()}", 0)
                except Exception as exc:
                    wx.MessageBox(f"Failed to save layout: {exc}", "Error", wx.OK | wx.ICON_ERROR)

    def menuItem_Load_LayoutOnMenuSelection(self, event):
        with wx.FileDialog(self, "Load Workspace Layout", wildcard="Layout files (*.layout)|*.layout", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    with open(dlg.GetPath(), "r", encoding="utf-8") as h:
                        perspective = h.read().strip()
                    if perspective:
                        self._mgr.LoadPerspective(perspective)
                        self._mgr.Update()
                        if hasattr(self, "sync_pane_menu_checks"):
                            self.sync_pane_menu_checks()
                        self.GetStatusBar().SetStatusText(f"Layout loaded: {dlg.GetPath()}", 0)
                except Exception as exc:
                    wx.MessageBox(f"Failed to load layout: {exc}", "Error", wx.OK | wx.ICON_ERROR)

    def menuItem_reset_Layout1OnMenuSelection(self, event):
        if hasattr(self, "_default_perspective") and self._default_perspective:
            self._mgr.LoadPerspective(self._default_perspective)
            self._mgr.Update()
            if hasattr(self, "sync_pane_menu_checks"):
                self.sync_pane_menu_checks()
        self.reset_simulation_view()
        self.GetStatusBar().SetStatusText("Workspace layout reset to default.", 0)

    # Component Creation Menu Delegates (Forwarded directly)
    def menuItem_parabolicMirrorOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_sphericalMirrorOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_concaveParaboloidOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_convexParaboloidOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_parabolicSurfaceOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_sphericalSurfaceOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_concaveLensOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_convexLensOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_parabolicLensOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_sphericalLensOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_rayOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_rectangularScreenOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_sourceRayOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_CircularBeamOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_rectOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    def menuItem_randomBeamOnMenuSelection(self, event):
        self.OnComponentMenuSelection(event)

    # Edit & Search Menu Delegates
    def menuItem_undoOnMenuSelection(self, event):
        self.undo()

    def menuItem_redoOnMenuSelection(self, event):
        self.redo()

    def menuItem_selectAllOnMenuSelection(self, event):
        wx.MessageBox("Select All functionality.", "Info", wx.OK | wx.ICON_INFORMATION)

    def menuItem_deselectAllOnMenuSelection(self, event):
        wx.MessageBox("Deselect All functionality.", "Info", wx.OK | wx.ICON_INFORMATION)

    def menuItem_find_componentsOnMenuSelection(self, event):
        self.on_search_find_components(event)

    # Help & Test Cases Delegates
    def menuItem_DocumentationOnMenuSelection(self, event):
        webbrowser.open("https://github.com")

    def menuItem_aboutOnMenuSelection(self, event):
        wx.MessageBox("OpticsLAB - wxPython + VisPy optics simulation GUI", "About OpticsLAB", wx.OK | wx.ICON_INFORMATION)
    
    def menuItem_telescopeexmpOnMenuSelection(self, event):
        script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "opticsLAB", "raytracing", "testCases", "test_telescope_new.py")
        subprocess.Popen([sys.executable, script])

    def menuItem_cooketripletOnMenuSelection(self, event):
        script = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "opticsLAB", "raytracing", "testCases", "optics_dsn_book_test_cases", "test_cooke_triplet_lens.py")
        subprocess.Popen([sys.executable, script])

    # ---------------------------------------------------------------------------
    # Workspace & File Operations
    # ---------------------------------------------------------------------------
    def update_recent_files_menu(self):
        if not hasattr(self, "menu_recent") or not self.menu_recent: return
        for item in list(self.menu_recent.GetMenuItems()): self.menu_recent.DestroyItem(item)

        recent_files = load_recent_files()
        if not recent_files:
            dummy = wx.MenuItem(self.menu_recent, wx.ID_ANY, "(No recent project files)", "", wx.ITEM_NORMAL)
            dummy.Enable(False)
            self.menu_recent.Append(dummy)
            return

        for idx, filepath in enumerate(recent_files[:10]):
            label = f"&{idx+1} {os.path.basename(filepath)}"
            menu_id = wx.NewIdRef()
            self.menu_recent.Append(wx.MenuItem(self.menu_recent, menu_id, label, filepath, wx.ITEM_NORMAL))
            self.Bind(wx.EVT_MENU, lambda e, p=filepath: self._open_recent_path(p), id=menu_id)

    def _open_recent_path(self, filepath):
        if not os.path.exists(filepath):
            wx.MessageBox(f"File no longer exists: {filepath}", "Error", wx.OK | wx.ICON_ERROR)
            add_recent_file("")
            self.update_recent_files_menu()
            return

        ext = os.path.splitext(filepath)[1].lower()
        if ext not in (".json", ".toml"):
            wx.MessageBox(f"Unsupported project file type: {filepath}", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            with open(filepath, "r", encoding="utf-8") as handle:
                raw_data = json.load(handle) if ext == ".json" else load_toml(filepath)
            self.load_project_data(raw_data, filepath)
        except Exception as exc:
            wx.MessageBox(f"Failed to load recent file: {exc}", "Error", wx.OK | wx.ICON_ERROR)

    def _add_source_menu_items(self): pass

    def OnFileOpenFolder(self, event):
        with wx.DirDialog(self, "Open Project Workspace Folder", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.panel_project_folder_tree.load_directory(dlg.GetPath())
                self.GetStatusBar().SetStatusText(f"Workspace loaded: {dlg.GetPath()}", 0)

    def OnFileCloseFolder(self, event):
        self.panel_project_folder_tree.clear_directory()
        self.GetStatusBar().SetStatusText("Workspace folder closed", 0)

    def OnFileOpenFile(self, event):
        with wx.FileDialog(self, "Open Project or Component Configuration File", wildcard="Config files (*.json;*.toml)|*.json;*.toml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    path = dlg.GetPath()
                    with open(path, "r", encoding="utf-8") as h:
                        raw_data = json.load(h) if path.endswith(".json") else load_toml(path)
                    self.load_project_data(raw_data, path)
                except Exception as exc:
                    wx.MessageBox(f"Failed to load file: {exc}", "Error", wx.OK | wx.ICON_ERROR)

    def push_undo_state(self):
        self.undo_stack.append({"project": copy.deepcopy(self.project_info), "configs": copy.deepcopy(self.active_component_configs)})
        if len(self.undo_stack) > 50: self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return self.GetStatusBar().SetStatusText("Nothing to undo", 0)
        self.redo_stack.append({"project": copy.deepcopy(self.project_info), "configs": copy.deepcopy(self.active_component_configs)})
        self._restore_snapshot(self.undo_stack.pop())
        self.GetStatusBar().SetStatusText("Undo performed", 0)

    def redo(self):
        if not self.redo_stack:
            return self.GetStatusBar().SetStatusText("Nothing to redo", 0)
        self.undo_stack.append({"project": copy.deepcopy(self.project_info), "configs": copy.deepcopy(self.active_component_configs)})
        self._restore_snapshot(self.redo_stack.pop())
        self.GetStatusBar().SetStatusText("Redo performed", 0)

    def _restore_snapshot(self, snapshot):
        for comp in list(self.active_components.values()): remove_visual(comp)
        self.active_components.clear()
        self.active_component_configs.clear()
        self.panel_tree.listBox_lst_components.Clear()

        self.project_info.update(snapshot.get("project", {}))
        self.apply_project_properties(self.project_info)
        canvas = self.panel_simulation.canvas_obj

        for comp_name, config in snapshot.get("configs", {}).items():
            opt_center = OptPoint(*config.get("center", [0.0, 0.0, 0.0]))
            radius = float(config.get("radius", 1.0))
            vis_color = color_to_vispy(config.get("color", "#00ff00ff"))
            base_class_name = resolve_template_name(comp_name) or comp_name
            if comp := self.engine.instantiate_component(base_class_name, base_class_name.lower(), config, opt_center, radius, vis_color, canvas):
                self.active_components[comp_name] = comp
                self.active_component_configs[comp_name] = config.copy()
                self.panel_tree.listBox_lst_components.Append(comp_name)

        if canvas: canvas.canvas.update()
        self.panel_components_tree.update_tree()
        self.show_project_properties()
        self.run_simulation(user_initiated=False)

    def load_project_data(self, raw_data, path=""):
        if isinstance(raw_data, dict) and ("project" in raw_data or "components" in raw_data):
            self.tool_clearOnToolClicked(None)
            if path:
                self.current_project_filepath = path
                add_recent_file(path)
                self.update_recent_files_menu()

            if proj := raw_data.get("project", {}):
                self.project_info.update(proj)
                self.apply_project_properties(self.project_info)

            for comp_data in raw_data.get("components", []):
                self.update_component_instance(comp_data.get("name", "Component"), comp_data, record_undo=False)

            self.show_project_properties()
            self.GetStatusBar().SetStatusText(f"Loaded project workspace from: {path}", 0)
        else:
            comp_data = raw_data.get("components", [raw_data])[0] if isinstance(raw_data, dict) and "components" in raw_data else raw_data
            self.panel_properties.set_properties(comp_data.get("name", "Component"), comp_data)
            self.GetStatusBar().SetStatusText(f"Loaded component config from: {path}", 0)

    def OnFileSave(self, event, data=None):
        if data is not None or not self.current_project_filepath: return self.OnFileSaveAs(event, data=data)
        if canvas := self.panel_simulation.canvas_obj:
            try:
                self.project_info["vispy_elevation"] = float(getattr(canvas.view.camera, "elevation", 30.0))
                self.project_info["vispy_azimuth"] = float(getattr(canvas.view.camera, "azimuth", 30.0))
            except Exception: pass
            self.project_info["vispy_zoom"] = float(self.zoom_level)

        components_list = [{**config, "type": resolve_template_name(name) or name} for name, config in self.active_component_configs.items()]
        project_payload = {"project": self.project_info.copy(), "components": components_list}

        try:
            path = self.current_project_filepath
            if path.endswith(".json"):
                with open(path, "w", encoding="utf-8") as handle: json.dump(project_payload, handle, indent=4)
            else:
                save_toml(path, project_payload)
            add_recent_file(path)
            self.update_recent_files_menu()
            self.GetStatusBar().SetStatusText(f"Project saved directly to: {path}", 0)
        except Exception as exc:
            wx.MessageBox(f"Failed to save project: {exc}", "Error", wx.OK | wx.ICON_ERROR)

    def OnFileSaveAs(self, event, data=None):
        if data is not None:
            with wx.FileDialog(self, "Save Component Configuration", wildcard="TOML (*.toml)|*.toml|JSON (*.json)|*.json", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    try:
                        path = dlg.GetPath()
                        if path.endswith(".json"):
                            with open(path, "w", encoding="utf-8") as h: json.dump(data, h, indent=4)
                        else: save_toml(path, data)
                        self.GetStatusBar().SetStatusText(f"Saved component config: {path}", 0)
                    except OSError as exc: wx.MessageBox(f"Failed to save component: {exc}", "Error", wx.OK | wx.ICON_ERROR)
            return

        if canvas := self.panel_simulation.canvas_obj:
            try:
                self.project_info["vispy_elevation"] = float(getattr(canvas.view.camera, "elevation", 30.0))
                self.project_info["vispy_azimuth"] = float(getattr(canvas.view.camera, "azimuth", 30.0))
            except Exception: pass
            self.project_info["vispy_zoom"] = float(self.zoom_level)

        components_list = [{**config, "type": resolve_template_name(name) or name} for name, config in self.active_component_configs.items()]
        project_payload = {"project": self.project_info.copy(), "components": components_list}

        with wx.FileDialog(self, "Save Project Workspace", wildcard="JSON (*.json)|*.json|TOML (*.toml)|*.toml", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    path = dlg.GetPath()
                    if path.endswith(".json"):
                        with open(path, "w", encoding="utf-8") as handle: json.dump(project_payload, handle, indent=4)
                    else: save_toml(path, project_payload)
                    self.current_project_filepath = path
                    add_recent_file(path)
                    self.update_recent_files_menu()
                    self.GetStatusBar().SetStatusText(f"Saved project workspace: {path}", 0)
                except Exception as exc: wx.MessageBox(f"Failed to save project: {exc}", "Error", wx.OK | wx.ICON_ERROR)


MenuOpticsLAB = MenuOpticsLABMixin
