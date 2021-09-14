import numpy as np
import warnings
from .surface import Surface
from .custom_warnings import IntersectionWarning

class Plane(Surface):
	def __init__(self, center=(0, 0, 0), name=None, width=1.0, length=1.0, xTilt=0.0, yTilt=0.0, color='black', parentCanvas=None):
		self.width = width / 2
		self.length = length / 2
		xx = np.linspace(-self.width, self.width, 10)
		yy = np.linspace(-self.length, self.length, 10)
		x_grid, y_grid = np.meshgrid(xx, yy)
		z_grid = np.zeros(np.shape(x_grid))
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, name=name, xTilt=xTilt, yTilt=yTilt, color=color, parentCanvas=parentCanvas)
	
	def calculate_BeamIntersectionPoints(self, beam):
		"""
		Calculates and returns the intersection points at which a beam hits the surface
		:param beam: Beam incident on this surface
		:return: Points of intersection of the beam with this surface. Returns None for those rays which intersect outside the surface.
		"""
		intersection = []
		for ray in beam.get_Rays():
			intersection.append(self.calculate_RayIntersection(ray=ray))
		return np.array(intersection)
	
	def calculate_RayIntersection(self, ray):
		"""
		Calculates and returns the intersection point at which a ray hits the surface
		:param ray: Ray incident on the surface
		:return: Point of intersection of the ray with this surface. Returns None if the ray intersects outside the surface.
		"""
		# Notation taken from: https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
		p0 = self.center; l0 = ray.get_StartPoint()
		l = ray.get_Direction(); n = self.get_chiefNormalDirection()
		dotProduct1 = np.dot(l, n)
		dotProduct2 = np.dot(p0 - l0, n)
		
		# Test for parallelism
		if dotProduct1 == 0:
			if dotProduct2 == 0:
				warnings.warn("Ray '{0}' is on the Surface '{1}'. Check for '!'.".format(ray.name, self.name), IntersectionWarning)
				return
			warnings.warn("Ray '{0}' and Surface '{1}' do not intersect. Check for '!'.".format(ray.name, self.name), IntersectionWarning)
			return None
		
		d = dotProduct2 / dotProduct1
		if not 0<d<1000:
			# d cannot be negative as ray cannot go backwards. TODO upper limit will be automatically handled if limits of surface are considered
			warnings.warn("Negative direction value. Ray '{0}' and Surface '{1}' do not intersect. Check for '!'.".format(ray.name, self.name), IntersectionWarning)
			return None
		intersection = l0 + (l * d)
		# TODO To check whether the intersection point is within the surface. Return the point if within the surface
		return intersection
	
	def calculate_normalDirection(self, point):
		# TODO To check whether the intersection point is within the surface. Return the normal if within the surface
		return self.get_chiefNormalDirection()  # Normal Direction is the same everywhere for a plane
