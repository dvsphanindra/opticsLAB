import numpy as np
import warnings
from .surface import Surface
from .custom_warnings import IntersectionWarning

class Plane(Surface):
	def __init__(self, center=(0, 0, 0), name=None, width=1.0, length=1.0, radius=None, xTilt=0.0, yTilt=0.0,
				 color='black',  mediumBefore="Air", mediumAfter="Air", parentCanvas=None):
		self.width = width / 2
		self.length = length / 2
		self.radius = radius
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter

		xx = np.linspace(-self.width, self.width, 1000)
		yy = np.linspace(-self.length, self.length, 1000)
		x_grid, y_grid = np.meshgrid(xx, yy)
		z_grid = np.zeros(np.shape(x_grid))

		#z_grid = np.zeros_like(x_grid)

		if self.radius is not None:
			mask = x_grid ** 2 + y_grid ** 2 > self.radius ** 2
			z_grid[mask] = np.nan

		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid,
						 name=name, xTilt=xTilt, yTilt=yTilt, color=color, parentCanvas=parentCanvas)
	
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
		local = self.inverse_transform(intersection)
		x, y, z = local

		if self.radius is not None:
			if x * x + y * y > self.radius * self.radius:
				return None
		else:
			if abs(x) > self.width or abs(y) > self.length:
				return None

		return intersection, ray.get_Color() #jay Edit
	
	def calculate_normalDirection(self, point):
		# TODO To check whether the intersection point is within the surface. Return the normal if within the surface
		return self.get_chiefNormalDirection()  # Normal Direction is the same everywhere for a plane


	def is_point_inside_volume(self, point, tol=1e-6):
		local = self.inverse_transform(point)
		x, y, z = local

		if self.radius is not None:
			return x * x + y * y <= self.radius * self.radius + tol
		return abs(x) <= self.width + tol and abs(y) <= self.length + tol


	def surface_error(self, point):
		local = self.inverse_transform(point)
		x, y, z = local

		if self.radius is not None:
			radial_error = max(0.0, np.sqrt(x * x + y * y) - self.radius)
			return abs(z) + radial_error

		x_err = max(0.0, abs(x) - self.width)
		y_err = max(0.0, abs(y) - self.length)
		return abs(z) + x_err + y_err