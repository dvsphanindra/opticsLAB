import numpy as np
from .surface import Surface


class Spherical_Surface(Surface):
    def __init__(self, radius_of_curvature=100.0, aperture_radius=10.0,
                 center=(0, 0, 0), name=None, xTilt=0.0, yTilt=0.0,
                 color='black', mediumBefore="Air", mediumAfter="Air",
                 parentCanvas=None, n_r=100, n_theta=100):

        self.R = float(radius_of_curvature)
        self.aperture_radius = float(aperture_radius)
        self.mediumBefore = mediumBefore
        self.mediumAfter = mediumAfter

        r = np.linspace(0.0, self.aperture_radius, n_r)
        theta = np.linspace(0.0, 2.0 * np.pi, n_theta)
        Rg, TH = np.meshgrid(r, theta)

        x_grid = Rg * np.cos(TH)
        y_grid = Rg * np.sin(TH)
        z_grid = self._sag(x_grid, y_grid)

        super().__init__(
            center=center,
            x_grid=x_grid,
            y_grid=y_grid,
            z_grid=z_grid,
            name=name,
            xTilt=xTilt,
            yTilt=yTilt,
            color=color,
            parentCanvas=parentCanvas
        )

    def _sag(self, x, y):
        rho2 = x*x + y*y
        R = self.R

        inside = R*R - rho2
        if np.any(inside < 0):
            if isinstance(inside, np.ndarray):
                inside = np.maximum(inside, 0.0)
            else:
                inside = max(inside, 0.0)

        # Branch chosen so z(0,0)=0
        return R - np.sign(R) * np.sqrt(inside)

    def function(self, x, y):
        rho2 = x*x + y*y
        if not isinstance(x, np.ndarray) and not isinstance(y, np.ndarray):
            if rho2 > self.aperture_radius**2:
                return None
        return self._sag(x, y)

    def is_point_inside_volume(self, point, tol=1e-6):
        local = self.inverse_transform(point)
        x, y, z = local
        if x*x + y*y > self.aperture_radius**2 + tol:
            return False
        z_expected = self._sag(x, y)
        return abs(z - z_expected) <= tol

    def surface_error(self, point):
        local = self.inverse_transform(point)
        x, y, z = local

        radial_error = max(0.0, np.sqrt(x*x + y*y) - self.aperture_radius)
        z_expected = self._sag(x, y)
        return abs(z - z_expected) + radial_error

    def calculate_normalDirection(self, point):
        local = self.inverse_transform(point)
        x, y, z = local

        sphere_center_local = np.array([0.0, 0.0, self.R], dtype=float)

        # Outward normal from sphere center to surface point
        normal_local = np.array([x, y, z], dtype=float) - sphere_center_local
        nrm = np.linalg.norm(normal_local)
        if nrm < 1e-12:
            normal_local = np.array([0.0, 0.0, -1.0 if self.R > 0 else 1.0], dtype=float)
        else:
            normal_local /= nrm

        origin_global = self.transform(np.array([0.0, 0.0, 0.0]))
        tip_global = self.transform(normal_local)
        global_normal = tip_global - origin_global
        global_normal = global_normal / np.linalg.norm(global_normal)
        return global_normal

    def calculate_RayIntersection(self, ray, tol=1e-9):
        p0 = np.array(ray.get_StartPoint(), dtype=float)
        d0 = np.array(ray.get_Direction(), dtype=float)
        d0 = d0 / np.linalg.norm(d0)

        p_local = self.inverse_transform(p0)
        p1_local = self.inverse_transform(p0 + d0)
        d_local = p1_local - p_local
        d_local = d_local / np.linalg.norm(d_local)

        sphere_center = np.array([0.0, 0.0, self.R], dtype=float)
        oc = p_local - sphere_center

        A = np.dot(d_local, d_local)
        B = 2.0 * np.dot(d_local, oc)
        C = np.dot(oc, oc) - self.R*self.R

        disc = B*B - 4.0*A*C
        if disc < 0:
            return None

        sqrt_disc = np.sqrt(disc)
        roots = [(-B - sqrt_disc) / (2.0*A), (-B + sqrt_disc) / (2.0*A)]
        roots = [t for t in roots if t > 1e-6]

        if not roots:
            return None

        roots.sort()

        for t in roots:
            hit_local = p_local + t * d_local
            xh, yh, zh = hit_local

            if xh*xh + yh*yh <= self.aperture_radius**2 + tol:
                sag_here = self._sag(xh, yh)
                if abs(zh - sag_here) <= 1e-5:
                    intersectionPoint = self.transform(hit_local)
                    return intersectionPoint, ray.get_Color()

        return None