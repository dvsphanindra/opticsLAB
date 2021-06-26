from ..primitives.parabolicSurface import Parabolic_Surface

class Concave_Paraboloid(Parabolic_Surface):
	def __init__(self, a, b, center, radius=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"""
		Creates a convex paraboloid surface with the given center and normal with the specified media
		:param a: surface axis along x direction
		:param b: surface axis along y direction
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
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
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
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
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
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
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
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
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param radius: radius of the surface. Default: 1.0
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"" "
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		c=-1
		super().__init__(a=a, b=b, c=c, center=center, radius=radius, xTilt=xTilt, yTilt=yTilt, color=color)
"""
