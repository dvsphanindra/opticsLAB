import numpy as np
from .surface import Surface

class Cylinder(Surface):
	def __init__(self, radius=1.0, length=1.0, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='green',name=None, parentCanvas=None):
		""" Creates the data of a cylinder oriented along z axis whose center, radius and length are given as inputs
		Based on the example given at: https://stackoverflow.com/a/49311446/2602319
		"""

		self.radius = radius
		self.length = length

		z = np.linspace(-length / 2, length / 2, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		theta_grid, z_grid = np.meshgrid(theta, z)
		x_grid = radius * np.cos(theta_grid)
		y_grid = radius * np.sin(theta_grid)
		
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt, name=name,
		                 color=color,parentCanvas=parentCanvas)

	def is_point_inside_volume(self, point):
		# Translate point to the cylinder's local coordinate system
		local_point = self.inverse_transform(point)
		x, y, z = local_point

		# Inside cylinder if x^2 + y^2 <= radius^2 and z is within length
		r_squared = x ** 2 + y ** 2

		# Optionally, you don't even need to check Z here because the
		# parabolic surfaces act as the top and bottom Z bounds!
		return r_squared <= (self.radius ** 2 + 1e-5)