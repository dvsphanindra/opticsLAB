import numpy as np
from primitives import Plane, Surface, Parabolic_Surface

class RectangularSurface(Plane):
	def __init__(self, center, length=1.0, width=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"""
		Creates a plane surface with the given center and normal with the specified media
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param length: length of the plane. Default: 1
		:param width: width of the plane. Default: 1
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"""
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		super().__init__(center=center, width=width, length=length, xTilt=xTilt, yTilt=yTilt, color=color)
		
class ConicSurface(Surface):
	def __init__(self, center, radius=1.0, RoC=2.0, K=1.0,  xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"""
		Creates a conic surface with the given center and normal with the specified media
		:param center: Center of the surface with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param RoC: Radius of Curvature of the conic. Default: 1.0
		:param K: Conic Constant. Sphere: K = 0; Oblate ellipsoids: K > 0; Prolate Ellipsoids: −1 < K < 0; Paraboloid: K = −1; Hyperboloids: K < −1
		:param xTilt: tilt of the surface with respect to pyOpticalBench X axis
		:param yTilt: tilt of the surface with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
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
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt, color=color)
		
class Convex_Paraboloid(Parabolic_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"""
		Creates a convex paraboloid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"""
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)

class Concave_Paraboloid(Parabolic_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"""
		Creates a convex paraboloid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"""
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=-1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)
		
"""
class Convex_Ellipsoid(Elliptic_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"" "
		Creates a convex ellipsoid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"" "
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)

class Concave_Ellipsoid(Elliptic_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"" "
		Creates a convex ellipsoid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"" "
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=-1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)
		
class Convex_Hyperboloid(Hyperboloid_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"" "
		Creates a convex hyperboloid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"" "
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)

class Concave_Hyperboloid(Hyperboloid_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"" "
		Creates a convex hyperboloid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"" "
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=-1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)
"""
