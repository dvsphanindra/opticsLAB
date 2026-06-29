"""
3D Vispy simulation canvas viewport panel for OpticsLAB.
"""
import inspect
import wx
from panel_simulation_GUI import MyPanel_simulation

try:
    from opticsLAB.raytracing.component.OpticsLabCanvas import OpticsLabCanvas
except ImportError:
    from raytracing.component.OpticsLabCanvas import OpticsLabCanvas


class SimulationPanel(MyPanel_simulation):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame = parent
        self.canvas_initialized = False
        self.canvas_obj = None
        self.Bind(wx.EVT_SIZE, self.OnSize)
        wx.CallAfter(self._ensure_canvas)

    def _ensure_canvas(self):
        if self.canvas_initialized or (size := self.m_panel1.GetSize()).x <= 0 or size.y <= 0:
            return
        try:
            kwargs = {"parent": self.m_panel1, "size": (size.x, size.y), "app": "wx", "bgColor": "lightsteelblue"}
            sig = inspect.signature(OpticsLabCanvas.__init__)
            valid_args = {k: v for k, v in kwargs.items() if k in sig.parameters or (sig.parameters.get(k) and sig.parameters[k].kind == inspect.Parameter.VAR_KEYWORD)}
            self.canvas_obj = OpticsLabCanvas(**valid_args)
            
            sim_sizer = wx.BoxSizer(wx.VERTICAL)
            sim_sizer.Add(self.canvas_obj.canvas.native, 1, wx.EXPAND)
            self.m_panel1.SetSizer(sim_sizer)
            self.m_panel1.Layout()
            self.canvas_obj.canvas.show()
            self.canvas_initialized = True
            self.frame.apply_project_properties(self.frame.project_info)
        except Exception as exc:
            print("Error initializing OpticsLabCanvas inside SimulationPanel:", exc)

    def OnSize(self, event):
        event.Skip()
        if not self.canvas_initialized:
            wx.CallAfter(self._ensure_canvas)
