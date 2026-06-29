"""
Tool-related event handlers for OpticsLAB GUI toolbar actions.
"""
import wx
from opticsLAB_support import remove_visual


class ToolOpticsLABMixin:
    """
    Mixin class containing event handler callbacks for toolbar actions.
    """
    def tool_NewOnToolClicked(self, event): self.tool_clearOnToolClicked(event)
    def tool_saveOnToolClicked(self, event): self.OnFileSave(event)
    def tool_OpenOnToolClicked(self, event): self.OnFileOpenFile(event)
    def tool_RedoOnToolClicked(self, event): self.redo()
    def tool_undoOnToolClicked(self, event): self.undo()
    def tool_runOnToolClicked(self, event): self.run_simulation(user_initiated=True)
    def tool_findOnToolClicked(self, event): self.on_search_find_components(event)
    def tool_exportOnToolClicked(self, event): wx.MessageBox("Export feature not implemented yet.", "Info", wx.OK | wx.ICON_INFORMATION)
    def tool_helpOnToolClicked(self, event): wx.MessageBox("Help documentation coming soon.", "Help", wx.OK | wx.ICON_INFORMATION)

    def tool_zoomOnToolClicked(self, event):
        self.zoom_level = 0.5 if self.zoom_level > 2.0 else self.zoom_level + 0.2
        self.GetStatusBar().SetStatusText(f"Canvas zoom: {int(self.zoom_level * 100)}%", 0)
        if self.panel_simulation.canvas_obj:
            self.panel_simulation.canvas_obj.view.camera.fov = 30.0 / self.zoom_level
            self.panel_simulation.canvas_obj.canvas.update()

    def tool_clearOnToolClicked(self, event):
        if event is not None and self.active_components:
            if wx.MessageBox("Are you sure you want to clear all components and reset the workspace?", "Confirm Clear All", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING, self) != wx.YES:
                return

        self.push_undo_state()
        for comp in self.active_components.values():
            remove_visual(comp)
        self.active_components.clear()
        self.active_component_configs.clear()

        for vis in self.ray_visuals:
            if vis: vis.parent = None
        self.ray_visuals.clear()
        self.last_traced_rays.clear()

        self.panel_tree.listBox_lst_components.Clear()
        self.panel_properties.m_propertyGrid2.Clear()
        self.panel_properties.current_preset_data = {}
        self.panel_plots.draw_default_plots()
        self.reset_simulation_view()
        self.panel_components_tree.update_tree()
        self.show_project_properties()
        self.GetStatusBar().SetStatusText("System cleared and simulation view reset.", 0)

    def tool_ScreenshotOnToolClicked(self, event):
        if not (canvas_obj := self.panel_simulation.canvas_obj):
            return wx.MessageBox("Simulation canvas not initialized.", "Error", wx.OK | wx.ICON_ERROR)

        with wx.FileDialog(self, "Save Simulation Screenshot", wildcard="PNG Image (*.png)|*.png|JPEG Image (*.jpg)|*.jpg", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                try:
                    img_array = canvas_obj.canvas.render()
                    height, width, _ = img_array.shape
                    wx_img = wx.Image(width, height, img_array[:, :, :3].tobytes())
                    wx_type = wx.BITMAP_TYPE_JPEG if path.lower().endswith((".jpg", ".jpeg")) else wx.BITMAP_TYPE_PNG
                    wx_img.SaveFile(path, wx_type)
                    self.GetStatusBar().SetStatusText(f"Screenshot saved to: {path}", 0)
                except Exception as exc:
                    wx.MessageBox(f"Failed to save screenshot: {exc}", "Error", wx.OK | wx.ICON_ERROR)


ToolOpticsLAB = ToolOpticsLABMixin
