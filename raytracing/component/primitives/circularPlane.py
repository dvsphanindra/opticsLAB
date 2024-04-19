import numpy as np
from .surface import Surface


class Plane_Circular(Surface):
	def __init__(self, radius=1.0, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='black'):
		"""
		Creates the data for a circular plane whose center, radius are given as inputs
		"""
		# Generate the grid in cylindrical coordinates
		self.radius = radius
		
		r = np.linspace(0, self.radius, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		R, THETA = np.meshgrid(r, theta)
		
		# Convert to rectangular coordinates
		x_grid, y_grid = R * np.cos(THETA), R * np.sin(THETA)
		
		z_grid = np.zeros(np.shape(x_grid))
		
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt,
		                 color=color)
