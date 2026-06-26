from ..primitives.plane import Plane
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point

class RectangularSurface(Plane):
	def __init__(self, center, name=None, length=1.0, width=1.0, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green", parentCanvas=None):
		"""
		Creates a plane surface with the given center and normal with the specified media
		:param center: Center of the plane with respect to the opticsLab coordinates passed as a Point object.
		:param: name: Name of the surface for debugging purposes (optional)
		:param length: length of the plane. Default: 1
		:param width: width of the plane. Default: 1
		:param xTilt: tilt of the plane with respect to opticsLab X axis
		:param yTilt: tilt of the plane with respect to opticsLab Y axis
		:param mediumAfter: Medium after the surface
		:param mediumBefore: Medium before the surface (optional). Default: "Air"
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		"""
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		assert isinstance(center, Point), "RectangularSurface class: center is not a Point object"
		super().__init__(center=center, width=width,  name=name, length=length, xTilt=xTilt, yTilt=yTilt, color=color, parentCanvas=parentCanvas)
