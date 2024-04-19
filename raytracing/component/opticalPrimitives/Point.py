import numpy as np
from vispy import scene
from ..primitives.primitive_point import Primitive_point


class Point(Primitive_point):
	def __init__(self, x, y=None, z=None, parentCanvas=None):
		"""
		Point Object. Creates a numpy array so that it is readily usable for further calculations
		:param x: x coordinate of the Point or numpy array (x, y, z) or tuple (x, y, z)
		:param y: y coordinate of the Point
		:param z: z coordinate of the Point
		"""
		if not (isinstance(x, int) or isinstance(x, float) or "Point" in x.__str__()):
			x, y, z = x  # numpy array
		self.parentCanvas = parentCanvas
		super().__init__(x, y, z)
	
	def show(self, marker='•', size=80, color='yellow'):
		"""
		Displays the point on the parent object.
		:param marker: The text of the marker to be displayed. Default is '•'
		:param size: Size of the marker. Default is 80
		:param color: Color of the marker. Default is 'yellow'
		:return: If the scene object is None, then the visual for the point will be returned
		"""
		scene.Text(marker, font_size=size, bold=True, color=color, parent=self.parentCanvas.view.scene,
		           pos=self.coordinates)
