import numpy as np
from .surface import Surface

class Plane(Surface):
	def __init__(self, center=(0, 0, 0), width=1.0, length=1.0, xTilt=0.0, yTilt=0.0, color='black'):
		self.width = width / 2
		self.length = length / 2
		xx = np.linspace(-self.width, self.width, 10)
		yy = np.linspace(-self.length, self.length, 10)
		x_grid, y_grid = np.meshgrid(xx, yy)
		z_grid = np.zeros(np.shape(x_grid))
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt,
		                 color=color)
	
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
		# TODO Verify and confirm to the notation in: https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
		dotProduct = np.dot(self.get_chiefNormalDirection(), ray.get_Direction())
		# Test for parallelism
		assert dotProduct != 0, "Line and plane do not intersect or the line is contained in the plane"
		
		w = ray.get_StartPoint()  # - self.center
		si = - np.dot(self.get_chiefNormalDirection(), w) / dotProduct
		intersection = w + si * ray.get_Direction()  # + self.center
		# TODO TO check whether the intersection point is within the range. If within the range return the point
		return intersection
	
	def calculate_normalDirection(self, point):
		# TODO TO check whether the intersection point is within the range. If within the range return the normal
		return self.get_chiefNormalDirection()  # Normal Direction is the same everywhere for a plane
