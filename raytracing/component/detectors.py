# import numpy as np
# from .primitives.plane import Plane
#
#
# class RectangularScreen(Plane):
# 	def __init__(self, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='white', parent=None):
# 		# TODO to adjust dimensions automatically according to the width and height of the rays incident on the plane
# 		super().__init__(center=center, width=1.0, length=1.0, xTilt=xTilt, yTilt=yTilt, color=color)
#
# 	def calculate_BeamIntersectionPoints(self, beam):
# 		"""
# 		Calculates and returns the intersection points at which a beam hits the surface. Overridden method from parent class to return colors for plotting
# 		:param beam: Beam incident on this surface
# 		:return: Points of intersection of the beam with this surface. Returns None for those rays which intersect outside the surface.
# 		Additionally returns the colors of the beam for plotting
# 		"""
# 		intersection = []
# 		intersectionColours = []
# 		for ray in beam.get_Rays():
# 			_, __ = self.calculate_RayIntersection(ray=ray)
# 			intersection.append(_)
# 			intersectionColours.append(__)
# 		# TODO to move colors to screen and disable limits checking for screen plane
# 		return np.array(intersection), intersectionColours
#
# 	def calculate_RayIntersection(self, ray):
# 		"""
# 		Calculates and returns the intersection point at which a ray hits the surface
# 		:param ray: Ray incident on the surface
# 		:return: Point of intersection of the ray with this surface. Returns None if the ray intersects outside the surface.
# 		        Additionally returns the colors of the beam for plotting
# 		"""
# 		dotProduct = np.dot(self.get_chiefNormalDirection(), ray.get_Direction())
# 		# Test for parallelism
# 		assert dotProduct != 0, "Line and plane do not intersect or the line is contained in the plane"
#
# 		w = ray.get_StartPoint() - self.center
# 		si = - np.dot(self.get_chiefNormalDirection(), w) / dotProduct
# 		if si < 0:
# 			return None, ray.get_Color()
# 		intersection = w + si * ray.get_Direction() + self.center
# 		ray.update_Ray(intersection)  # Extend the ray to meet the screen
# 		# TODO TO check whether the intersection point is within the range. If within the range return the normal
# 		return intersection, ray.get_Color()
#
#
#
#
#
import numpy as np
from vispy.color import Color
from .primitives.plane import Plane


class RectangularScreen(Plane):
    def __init__(self, center=(0, 0, 0), width=2.0, height=2.0,
                 xTilt=0.0, yTilt=0.0,
                 color=Color('green', alpha=1.0), parent=None):

        self.width = width
        self.height = height

        super().__init__(
            center=center,
            width=width,
            length=height,
            xTilt=xTilt,
            yTilt=yTilt,
            color=color,
            parentCanvas=parent
        )

    def calculate_BeamIntersectionPoints(self, beam):
        intersection = []
        intersectionColours = []

        for ray in beam.get_Rays():
            hit, hit_color = self.calculate_RayIntersection(ray=ray)
            intersection.append(hit)
            intersectionColours.append(hit_color)

        return np.array(intersection, dtype=object), intersectionColours

    def calculate_RayIntersection(self, ray):
        dotProduct = np.dot(self.get_chiefNormalDirection(), ray.get_Direction())

        if abs(dotProduct) < 1e-12:
            return None

        w = ray.get_StartPoint() - self.center
        si = -np.dot(self.get_chiefNormalDirection(), w) / dotProduct

        if si < 0:
            return None

        intersection = w + si * ray.get_Direction() + self.center

        return intersection

    def stop_ray_on_screen(self, ray):
        hit = self.calculate_RayIntersection(ray)
        if hit is None:
            return None

        last_exit_point = np.array(ray.get_StartPoint(), dtype=float)
        hit = np.array(hit, dtype=float)
        hit_distance = np.linalg.norm(hit - last_exit_point)

        ray.length = hit_distance

        if hasattr(ray, 'update_visual'):
            ray.update_visual()
        else:
            ray.update_Ray(hit)

        return hit