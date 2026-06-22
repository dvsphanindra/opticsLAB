import numpy as np
from abc import ABC, abstractmethod
from .. import Point
from ..primitives.cylinder import Cylinder
from ..primitives.LensSideWall import LensSideWall
from ..sources import Ray
from ..miscellaneous_components import display_point
from ..materialProperties import refractiveIndex


class Lens(ABC):
    def __init__(self, center=(0, 0, 0), radius=1.0,
                 thickness=1.0, name=None,                mediumAfter="Air", mediumBefore="Air",
                 color=None, parentCanvas=None):
        """
        General parent lens class.
        Child classes must:
        1. Build self.front and self.back in _build_surfaces()
        2. Implement _front_local_z(x, y) and _back_local_z(x, y)
        """
        if hasattr(center, 'get_coordinates'):
            self.center = np.array(center.get_coordinates(), dtype=float)
        else:
            self.center = np.array(center, dtype=float)

        self.radius = radius
        self.thickness = thickness
        self.mediumBefore = mediumBefore
        self.mediumAfter = mediumAfter
        self.color = color
        self.name= name
        self.parentCanvas = parentCanvas

        self.front = None
        self.back = None

        self._build_surfaces()

        self._frame = Cylinder(
            radius=self.radius,
            length=self.thickness,
            center=self.center,
            name="LensFrame",
            color=self.color,
            parentCanvas=None
        )

        self.edge = LensSideWall(
            lens=self,
            name="Edge",
            color=self.color,
            parentCanvas=self.parentCanvas
        )

        self.surfaces = [self.front, self.edge, self.back]

    @abstractmethod
    def _build_surfaces(self):
        """
        Child creates self.front and self.back here.
        """
        pass

    @abstractmethod
    def _front_local_z(self, x, y):
        """
        Sag of front surface in lens local coordinates.
        """
        pass

    @abstractmethod
    def _back_local_z(self, x, y):
        """
        Sag of back surface in lens local coordinates.
        """
        pass

    def translate(self, vector):
        vec = np.array(vector.get_coordinates(), dtype=float) if (
            hasattr(vector, 'get_coordinates')) else np.array(vector, dtype=float)

        self.center += vec
        self._frame.translate(vec)

        for surface in self.surfaces:
            surface.translate(vec)

    def rotate_aboutX(self, angle):
        self._frame.rotate_aboutX(angle, pivot=self.center)
        for surface in self.surfaces:
            surface.rotate_aboutX(angle, pivot=self.center)

    def rotate_aboutY(self, angle):
        self._frame.rotate_aboutY(angle, pivot=self.center)
        for surface in self.surfaces:
            surface.rotate_aboutY(angle, pivot=self.center)

    def rotate_aboutZ(self, angle):
        self._frame.rotate_aboutZ(angle, pivot=self.center)
        for surface in self.surfaces:
            surface.rotate_aboutZ(angle, pivot=self.center)

    def calculate_RayIntersection(self, ray):
        """
        Returns the closest valid intersection with the solid lens.
        Mostly useful for debugging/inspection. For optics, use calculate_RefractedRay().
        """
        valid_intersections = []

        for surface in self.surfaces:
            hit_data = surface.calculate_RayIntersection(ray)
            if hit_data is None:
                continue

            hit_point, color = hit_data

            is_valid = True
            for other_surface in self.surfaces:
                if other_surface is surface:
                    continue
                if not other_surface.is_point_inside_volume(hit_point):
                    is_valid = False
                    break

            if is_valid:
                dist = np.linalg.norm(np.array(hit_point) - np.array(ray.get_StartPoint()))
                if dist > 1e-6:
                    valid_intersections.append((dist, hit_point, color, surface))

        if not valid_intersections:
            return None

        valid_intersections.sort(key=lambda x: x[0])
        _, hit_point, color, hit_surface = valid_intersections[0]
        return hit_point, hit_surface

    def calculate_normalDirection(self, point):
        """
        Delegates normal calculation to the surface that best matches the point.
        Requires each surface to implement surface_error(point).
        """
        best_surface = None
        min_error = float('inf')

        for surface in self.surfaces:
            if not hasattr(surface, "surface_error"):
                continue

            error = surface.surface_error(point)
            if error < min_error:
                min_error = error
                best_surface = surface

        if best_surface is not None:
            return best_surface.calculate_normalDirection(point)

        return None

    def _find_first_face_hit(self, ray):
        """
        Find the first optical face (front/back) hit by the incoming ray.
        Edge is used only as aperture/bounds check.
        """
        hits = []

        for face in [self.front, self.back]:
            result = face.calculate_RayIntersection(ray)
            if result is None:
                continue

            hit_point, color = result

            if not self.edge.is_point_inside_volume(hit_point):
                continue

            dist = np.linalg.norm(np.array(hit_point) - np.array(ray.get_StartPoint()))
            if dist > 1e-6:
                hits.append((dist, face, hit_point))

        if not hits:
            return None

        hits.sort(key=lambda x: x[0])
        return hits[0]

    def _refract_at_surface(self, ray, surface, intersectionPoint):
        """
        Refract one ray at one surface using Snell's law.
        Falls back to reflection on total internal reflection.
        """
        incidentDir = np.array(ray.get_Direction(), dtype=float)
        incidentDir = incidentDir / np.linalg.norm(incidentDir)

        normalDir = np.array(surface.calculate_normalDirection(intersectionPoint), dtype=float)
        normalDir = normalDir / np.linalg.norm(normalDir)

        n1 = refractiveIndex(ray.get_Wavelength(), surface.mediumBefore)
        n2 = refractiveIndex(ray.get_Wavelength(), surface.mediumAfter)

        cos_i = -np.dot(normalDir, incidentDir)

        if cos_i < 0:
            normalDir = -normalDir
            cos_i = -np.dot(normalDir, incidentDir)
            #n1, n2 = n2, n1

        eta = n1 / n2
        k = 1.0 - eta**2 * (1.0 - cos_i**2)

        eps = 1e-5

        display_point(intersectionPoint, marker='o', color=ray.get_Color(), parentCanvas=self.parentCanvas)
        ray.update_Ray(intersectionPoint)

        if k < 0:
            newDir = incidentDir + 2.0 * cos_i * normalDir
            newDir = newDir / np.linalg.norm(newDir)
            new_start = np.array(intersectionPoint) + eps * normalDir
        else:
            newDir = eta * incidentDir + (eta * cos_i - np.sqrt(k)) * normalDir
            newDir = newDir / np.linalg.norm(newDir)
            new_start = np.array(intersectionPoint) - eps * normalDir

        return Ray(
            Point(new_start),
            rayDirection=newDir,
            wavelength=ray.get_Wavelength(),
            color=ray.get_Color(),
            dc=True,
            parentCanvas=self.parentCanvas
        )


    def calculate_RefractedRay(self, ray):
        """
        Trace the ray through the lens:
        1. Find entry face.
        2. Refract into lens.
        3. Find opposite face.
        4. Refract out of lens.
        """
        first_hit = self._find_first_face_hit(ray)

        if first_hit is None:
            fail_mark = ray.get_StartPoint() + ray.get_Direction() * 0.5
            display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
            return None

        _, entry_surface, p1 = first_hit

        ray_inside = self._refract_at_surface(ray, entry_surface, p1)
        if ray_inside is None:
            return None

        exit_surface = self.back if entry_surface is self.front else self.front

        second_hit = exit_surface.calculate_RayIntersection(ray_inside)
        if second_hit is None:
            return ray_inside

        p2, color2 = second_hit

        if not self.edge.is_point_inside_volume(p2):
            return ray_inside

        ray_out = self._refract_at_surface(ray_inside, exit_surface, p2)
        return ray_out

