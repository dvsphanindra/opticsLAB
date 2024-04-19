import vispy
from vispy import scene
from vispy.color import Color
import sys
from .miscellaneous_components import XYZAxis_Labeled, OpticalAxis

class PyOptiCADCanvas:
	def __init__(self, bgColor="lightsteelblue"):
		self.bgColor = bgColor
		self.canvas = scene.SceneCanvas(keys='interactive', bgcolor=Color(color=self.bgColor, alpha=0.5))
		self.view = self.canvas.central_widget.add_view()
		self.view.camera = scene.TurntableCamera(up='y', fov=30)
		
		XYZAxis_Labeled(parentCanvas=self)
		
		self.opticalAxis=OpticalAxis(parentCanvas=self)
		
	def show(self):
		self.canvas.show()
		if sys.flags.interactive == 0:
			vispy.app.run()
