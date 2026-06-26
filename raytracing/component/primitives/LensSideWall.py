import numpy as np
from .surface import Surface

class LensSideWall(Surface):
    def __init__(self, lens, name="Edge", color=None, parentCanvas=None, n_theta=100, n_s=100):
        self.lens = lens
        self.name = name
        self.color = color
        self.parentCanvas = parentCanvas
        self.n_theta = n_theta
        self.n_s = n_s

        theta = np.linspace(0, 2*np.pi, n_theta)
        s = np.linspace(0, 1, n_s)

        TH, S = np.meshgrid(theta, s)

        # x = lens.radius * np.cos(TH)
        # y = lens.radius * np.sin(TH)
        #
        # z_front = lens.thickness/2 + lens.c_front * ((x/lens.a)**2 + (y/lens.b)**2)
        # z_back = -lens.thickness/2 + lens.c_back * ((x/lens.a)**2 + (y/lens.b)**2)
        #
        # z = (1.0 - S) * z_back + S * z_front

        x = lens.radius * np.cos(TH)
        y = lens.radius * np.sin(TH)

        z_front = -lens.thickness / 2 + lens._front_local_z(x, y)
        z_back = lens.thickness / 2 + lens._back_local_z(x, y)

        z = (1.0 - S) * z_front + S * z_back

        self.x_grid = x
        self.y_grid = y
        self.z_grid = z

        super().__init__(center=lens.center,
                    x_grid=self.x_grid,
                    y_grid=self.y_grid,
                    z_grid=self.z_grid,
                    name=name,
                    color=color,
                    parentCanvas=parentCanvas
                    )

    def translate(self, vector):
        super().translate(vector)

    def rotate_aboutX(self, angle, pivot=None):
        super().rotate_aboutX(angle, pivot=pivot)

    def rotate_aboutY(self, angle, pivot=None):
        super().rotate_aboutY(angle, pivot=pivot)

    def rotate_aboutZ(self, angle, pivot=None):
        super().rotate_aboutZ(angle, pivot=pivot)

    def _front_z(self, x, y):
        return -self.lens.thickness / 2.0 + self.lens._front_local_z(x, y)

    def _back_z(self, x, y):
        return self.lens.thickness / 2.0 + self.lens._back_local_z(x, y)

    def _local_gap(self, x, y):
        return self._back_z(x, y) - self._front_z(x, y)

    def is_point_inside_volume(self, point, tol=1e-6):
        p = np.array(point, dtype=float)

        local_front = self.lens._frame.inverse_transform(p)
        x, y, z = local_front

        r2 = x*x + y*y
        if r2 > self.lens.radius**2 + tol:
            return False

        zf = self._front_z(x, y)
        zb = self._back_z(x, y)

        zmin = min(zf, zb) - tol
        zmax = max(zf, zb) + tol
        return zmin <= z <= zmax

    def surface_error(self, point):
        p = np.array(point, dtype=float)
        local = self.lens._frame.inverse_transform(p)
        x, y, z = local

        radial_error = abs(np.sqrt(x*x + y*y) - self.lens.radius)

        zf = self._front_z(x, y)
        zb = self._back_z(x, y)
        between_error = 0.0
        if z < min(zf, zb):
            between_error = min(zf, zb) - z
        elif z > max(zf, zb):
            between_error = z - max(zf, zb)

        return radial_error + between_error

    def calculate_normalDirection(self, point):
        p = np.array(point, dtype=float)
        local = self.lens._frame.inverse_transform(p)
        x, y, z = local

        normal_local = np.array([x, y, 0.0], dtype=float)
        nrm = np.linalg.norm(normal_local)

        if nrm < 1e-12:
            normal_local = np.array([1.0, 0.0, 0.0], dtype=float)
        else:
            normal_local /= nrm

        origin = self.lens._frame.transform(np.array([0.0, 0.0, 0.0]))
        tip = self.lens._frame.transform(normal_local)
        normal_world = tip - origin
        normal_world = normal_world / np.linalg.norm(normal_world)
        return normal_world

    def calculate_RayIntersection(self, ray):
        """
        Approximate side-wall hit by intersecting the ray with the radial boundary
        r = lens.radius in the lens local frame, then checking z lies between front/back.
        """
        p0 = np.array(ray.get_StartPoint(), dtype=float)
        d0 = np.array(ray.get_Direction(), dtype=float)
        d0 = d0 / np.linalg.norm(d0)

        p_local = self.lens._frame.inverse_transform(p0)
        p1_local = self.lens._frame.inverse_transform(p0 + d0)
        d_local = p1_local - p_local
        d_local = d_local / np.linalg.norm(d_local)

        x0, y0, z0 = p_local
        dx, dy, dz = d_local

        A = dx*dx + dy*dy
        B = 2.0 * (x0*dx + y0*dy)
        C = x0*x0 + y0*y0 - self.lens.radius**2

        if abs(A) < 1e-14:
            return None

        # disc = B*B - 4.0*A*C
        # if disc < 0:
        #     return None
        disc = B*B - 4.0*A*C
        if disc < -1e-12:
            return None
        disc = max(0.0, disc) # Clamp to zero to prevent math domain errors

        roots = [(-B - np.sqrt(disc)) / (2.0*A), (-B + np.sqrt(disc)) / (2.0*A)]
        roots = [t for t in roots if t > 1e-6]

        if not roots:
            return None

        roots.sort()

        for t in roots:
            hit_local = p_local + t * d_local
            x, y, z = hit_local

            zf = self._front_z(x, y)
            zb = self._back_z(x, y)

            if min(zf, zb) - 1e-6 <= z <= max(zf, zb) + 1e-6:
                hit_world = self.lens._frame.transform(hit_local)
                return hit_world, self.color

    # print("ray start world =", ray.get_StartPoint())
    # print("ray dir world =", ray.get_Direction())
    # print("ray start local =", p_local)
    # print("ray dir local =", d_local)
    # print("roots =", roots)
    # print("candidate hit local =", hit_local)
    # print("front z, back z =", zf, zb)

        return None