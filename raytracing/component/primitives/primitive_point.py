import numpy as np


class Primitive_point:
	def __init__(self, x, y, z):
		"""
		Primitive Point Object. Creates a numpy array so that it is readily usable for further calculations
		:param x: x coordinate of the Point
		:param y: y coordinate of the Point
		:param z: z coordinate of the Point
		"""
		self.coordinates = np.array((x, y, z))
	
	def get_coordinates(self):
		return self.coordinates
