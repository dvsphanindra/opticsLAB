"""
Matplotlib spot diagram and ray fan plotting panel for OpticsLAB.
Calculates coordinates and renders 2D plot diagrams directly without background threads.
All threading concepts have been removed for straightforward synchronous plotting.
"""
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from panel_plots_GUI import MyPanel1 as PanelPlots


class PlotsPanel(PanelPlots):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent

        self.spot_fig, self.spot_ax, self.spot_canvas = self._setup_canvas(self.panel_SpotDiagram)
        self.fan_fig, self.fan_ax, self.fan_canvas = self._setup_canvas(self.panel_RayFanDiagram)

        self.Layout()
        self.draw_default_plots()

    def _setup_canvas(self, target_panel):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(target_panel, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND)
        target_panel.SetSizer(sizer)
        return fig, ax, canvas

    def _format_axis(self, axis, title, spine_pos="zero"):
        axis.clear()
        axis.spines["left"].set_position(spine_pos)
        axis.spines["bottom"].set_position(spine_pos)
        axis.spines["right"].set_color("none")
        axis.spines["top"].set_color("none")
        axis.grid(True)
        axis.set_title(title, fontsize=10)

    def draw_default_plots(self):
        self._format_axis(self.spot_ax, "Spot Diagram (Ready)", "center")
        self.spot_canvas.draw()
        self._format_axis(self.fan_ax, "Ray Fan Diagram (Ready)", "center")
        self.fan_canvas.draw()

    # Updates 2D spot diagrams and ray fan graphs directly in the main window
    def update_plots(self, traced_rays=None):
        traced_rays = traced_rays or []
        result = self._compute_plot_data(traced_rays)
        self._on_plot_data_computed(result)

    # Calculates hit points and coordinates from traced light rays
    def _compute_plot_data(self, traced_rays):
        endpoints_x, endpoints_y = [], []
        for ray in traced_rays:
            coords = getattr(ray, "lineEnd_coordinates", getattr(ray, "endPoint", None))
            if coords is not None and len(coords) >= 2:
                endpoints_x.append(coords[0])
                endpoints_y.append(coords[1])
        
        sorted_pairs = sorted(zip(endpoints_y, endpoints_x)) if endpoints_x else []
        return endpoints_x, endpoints_y, sorted_pairs

    # Draws points and lines on the matplotlib canvas figures directly
    def _on_plot_data_computed(self, result):
        endpoints_x, endpoints_y, sorted_pairs = result
        if endpoints_x:
            self._format_axis(self.spot_ax, "Spot Diagram (Real Traces)", "zero")
            self.spot_ax.scatter(endpoints_x, endpoints_y, marker="+", color="blue", alpha=0.7)

            self._format_axis(self.fan_ax, "Ray Fan Diagram (Tangential)", "zero")
            self.fan_ax.plot([p[0] for p in sorted_pairs], [p[1] for p in sorted_pairs], color="red", linewidth=1.5, marker="o")
        else:
            self._format_axis(self.spot_ax, "Spot Diagram (No Hits)", "center")
            self._format_axis(self.fan_ax, "Ray Fan Diagram (No Hits)", "center")

        try:
            self.spot_canvas.draw()
            self.fan_canvas.draw()
        except Exception: pass
        
        if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
            msg = "Diagrams updated with ray trace data." if endpoints_x else "No ray intersection data available for diagrams."
            self.frame.GetStatusBar().SetStatusText(msg, 0)

    def button_refresh_diagramsOnButtonClick(self, event):
        self.update_plots(getattr(self.frame, "last_traced_rays", []))

    def button_savePlotOnButtonClick(self, event):
        fig = self.spot_fig if self.notebook.GetSelection() == 0 else self.fan_fig
        with wx.FileDialog(self, "Save Diagram Image", wildcard="PNG files (*.png)|*.png|JPEG files (*.jpg)|*.jpg", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    fig.savefig(dlg.GetPath(), bbox_inches="tight")
                    if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
                        self.frame.GetStatusBar().SetStatusText(f"Saved diagram image to: {dlg.GetPath()}", 0)
                except OSError as exc:
                    wx.MessageBox(f"Failed to save image: {exc}", "Error", wx.OK | wx.ICON_ERROR)
