import numpy as np
from .surface import Surface


class Cylinder(Surface):
	def __init__(self, radius=1.0, length=1.0, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='black'):
		""" Creates the data of a cylinder oriented along z axis whose center, radius and length are given as inputs
		Based on the example given at: https://stackoverflow.com/a/49311446/2602319
		"""
		z = np.linspace(-length / 2, length / 2, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		theta_grid, z_grid = np.meshgrid(theta, z)
		x_grid = radius * np.cos(theta_grid)
		y_grid = radius * np.sin(theta_grid)
		
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt,
		                 color=color)
