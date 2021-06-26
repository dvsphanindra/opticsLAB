from ..primitives.plane import Plane

class RectangularSurface(Plane):
	def __init__(self, center, length=1.0, width=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green"):
		"""
		Creates a plane surface with the given center and normal with the specified media
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param length: length of the plane. Default: 1
		:param width: width of the plane. Default: 1
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		"""
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		super().__init__(center=center, width=width, length=length, xTilt=xTilt, yTilt=yTilt, color=color)
