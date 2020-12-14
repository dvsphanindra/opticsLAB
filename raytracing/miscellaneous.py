import numpy as np
from primitives import LineVector

from vispy import scene

from vispy.visuals.transforms import STTransform

from vispy.scene.visuals import XYZAxis

class OpticalAxis(LineVector):
	def __init__(self, length=100, color='tomato'):
		"""
		Creates the Optical Axis of the openPyOpticalBench for rendering
		:param length: Length of the optical axis. Defaut: 100
		:param color: Color to be shown when the optical Axis is being visualized (Optional)
		TODO: Replace with infinite line
		"""
		start=(0,0,-length/2)
		super().__init__(start, [0,0,1], length, color)


class XYZAxis_Labeled(XYZAxis):
	def __init__(self, label=True, labels=("X", "Y", "Z"), pos=None, parent=None, **kwargs):
		kwargs.setdefault('parent', parent)
		super().__init__(**kwargs)
		self.unfreeze()
		self.labeling = label
		self.position = pos
		if self.position is None:
			self.position = np.array([0, 0, 0])
			self.transform = STTransform(translate=self.position)
		
		self.x = self.position + [1.05, 0, 0]
		self.y = self.position + [0, 1.05, 0]
		self.z = self.position + [0, 0, 1.05]
		
		if self.labeling:
			scene.Text(labels[0], font_size=50, bold=True, color='red', parent=parent, pos=self.x)
			scene.Text(labels[1], font_size=50, bold=True, color='green', parent=parent, pos=self.y)
			scene.Text(labels[2], font_size=50, bold=True, color='blue', parent=parent, pos=self.z)
