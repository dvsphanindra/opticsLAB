import numpy as np
from ..primitives.surface import Surface

class ConicSurface(Surface):
	def __init__(self, center, radius=1.0, RoC=2.0, K=1.0, name=None, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green", parentCanvas=None):
		"""
		Creates a conic surface with the given center and normal with the specified media
		:param center: Center of the surface with respect to the pyOptiCAD coordinates
		:param radius: radius of the surface. Default: 1.0
		:param RoC: Radius of Curvature of the conic. Default: 1.0
		:param K: Conic Constant. Sphere: K = 0; Oblate ellipsoids: K > 0; Prolate Ellipsoids: −1 < K < 0; Paraboloid: K = −1; Hyperboloids: K < −1
		:param: name: Name of the surface for debugging purposes (optional)
		:param xTilt: tilt of the surface with respect to pyOptiCAD X axis
		:param yTilt: tilt of the surface with respect to pyOptiCAD Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		"""
		self.mediumBefore=mediumBefore
		self.mediumAfter=mediumAfter
		
		# Generate the grid in cylindrical coordinates
		self.radius = radius
		
		r = np.linspace(0, self.radius, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		R, THETA = np.meshgrid(r, theta)
		
		self.parameters = (RoC, K)
		
		# Convert to rectangular coordinates
		x_grid, y_grid = R * np.cos(THETA), R * np.sin(THETA)
		
		# p = RoC/(K+1)
		# z_grid = p - np.sqrt(p*p - ((x_grid**2+y_grid**2)/(K+1)))
		t=R**2/RoC
		z_grid = t / (1 + np.sqrt(1 - ((1 + K) * t / RoC)))
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, name=name, xTilt=xTilt, yTilt=yTilt, color=color, parentCanvas=parentCanvas)
