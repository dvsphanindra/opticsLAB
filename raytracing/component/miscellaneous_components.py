import numpy as np
from .primitives.lineVector import LineVector

from vispy import scene

from vispy.visuals.transforms import STTransform

from vispy.scene.visuals import XYZAxis

from .primitives.constants import Z_AXIS_DIRECTION

class OpticalAxis(LineVector):
	def __init__(self, length=100, color='tomato', parentCanvas=None):
		"""
		Creates the Optical Axis of the openPyOpticalBench for rendering
		:param length: Length of the optical axis. Defaut: 100
		:param color: Color to be shown when the optical Axis is being visualized (Optional)
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		TODO: Replace with infinite line
		"""
		start=(0,0,-length/2)
		super().__init__(start=start, direction=Z_AXIS_DIRECTION, name='Optical Axis', dc=False, length=length, color=color, parentCanvas=parentCanvas)


class XYZAxis_Labeled(XYZAxis):
	def __init__(self, label=True, labels=("X", "Y", "Z"), pos=None, parentCanvas=None, **kwargs):
		kwargs.setdefault('parent', parentCanvas.view.scene)
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
			scene.Text(labels[0], font_size=50, bold=True, color='red', parent=parentCanvas.view.scene, pos=self.x)
			scene.Text(labels[1], font_size=50, bold=True, color='green', parent=parentCanvas.view.scene, pos=self.y)
			scene.Text(labels[2], font_size=50, bold=True, color='blue', parent=parentCanvas.view.scene, pos=self.z)
			
# class Point_Object(Point):
# 	def __init__(self, x, y, z, name=''):
# 		super().__init__(x, y, z)
# 		self._name = name
#
# 	@property
# 	def name(self):
# 		return self._name
#
# 	@name.setter
# 	def name(self, name=''):
# 		assert isinstance(name, str), "Only strings are allowed as names"
# 		self._name = name

def display_point(point, marker='•', size=80, color='yellow', parentCanvas=None):
	"""
	Displays a point on the given parent object. If the parent object is not given, returns the visual.
	:param point: Point which should be displayed
	:param marker: The text of the marker to be displayed. Default is '•'
	:param size: Size of the marker. Default is 80
	:param color: Color of the marker. Default is 'yellow'
	:param parentCanvas: Canvas on which the object is to be rendered. Default is None
	:return: If the scene object is None, then the visual for the point will be returned
	"""
	point_visual = scene.Text(marker, font_size=size, bold=True, color=color, parent=parentCanvas.view.scene, pos=point)
	if parentCanvas is None: return point_visual
