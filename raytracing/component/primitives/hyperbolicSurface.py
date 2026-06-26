import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot
from .surface import Surface


class Hyperbolic_Surface(Surface):
    def __init__(self, radius=1.0, centerHoleRadius=0.0, R=8000.0, K=-1.1,
                 center=(0, 0, 0), mediumAfter="Air", mediumBefore="Air",
                 name=None, xTilt=0.0, yTilt=0.0, color='black',
                 parentCanvas=None, n_r=100, n_theta=100):

        self.mediumBefore = mediumBefore
        self.mediumAfter = mediumAfter
        self.radius = float(radius)
        self.centerHoleRadius = float(centerHoleRadius)
        self.Rc = float(R)
        self.K = float(K)

        if self.K >= -1.0:
            raise ValueError("Hyperbolic_Surface requires K < -1.0")

        r = np.linspace(self.centerHoleRadius, self.radius, n_r)
        theta = np.linspace(0.0, 2.0 * np.pi, n_theta)
        r_grid, theta_grid = np.meshgrid(r, theta)

        self.x_grid = r_grid * np.cos(theta_grid)
        self.y_grid = r_grid * np.sin(theta_grid)
        self.z_grid = self.function(self.x_grid, self.y_grid)

        super().__init__(
            center=center,
            x_grid=self.x_grid,
            y_grid=self.y_grid,
            z_grid=self.z_grid,
            name=name,
            xTilt=xTilt,
            yTilt=yTilt,
            color=color,
            parentCanvas=parentCanvas
        )

    def function(self, x, y):
        """
        Standard optical conic sag equation.
        For Hyperbolic_Surface, K must be < -1.
        This returns the same sag branch convention as ConicSurface.
        """
        is_array = isinstance(x, np.ndarray) or isinstance(y, np.ndarray)

        r2 = x * x + y * y

        if not is_array:
            if np.sqrt(r2) > self.radius:
                return None
            if np.sqrt(r2) < self.centerHoleRadius:
                return None

        c = 1.0 / self.Rc
        inside = 1.0 - (1.0 + self.K) * (c * c) * r2

        if isinstance(inside, np.ndarray):
            inside = np.maximum(inside, 0.0)
        else:
            if inside < 0.0:
                return None

        z = (c * r2) / (1.0 + np.sqrt(inside))
        return z

    def calculate_normalDirection(self, point):
        """
        Exact surface normal from the implicit conic equation:
            F(x,y,z) = c*(x^2 + y^2) + c*(K+1)*z^2 - 2*z = 0
        """
        x0, y0, z0 = self.inverse_transform(point)

        c = 1.0 / self.Rc

        local_normal = np.array([
            -c * x0,
            -c * y0,
            1.0 - c * (self.K + 1.0) * z0
        ], dtype=float)

        nrm = np.linalg.norm(local_normal)
        if nrm < 1e-15:
            return None

        local_normal /= nrm

        global_normal = self.rotate_vector(local_normal)
        global_normal = np.array(global_normal, dtype=float)
        global_normal /= np.linalg.norm(global_normal)

        return global_normal

    def calculate_RayIntersection(self, ray, max_iter=50, tol=1e-6):
        """
        Exact analytic ray / conic intersection with branch validation.
        This matches the working ConicSurface logic.
        """
        global_start = np.array(ray.get_StartPoint(), dtype=float)
        local_start = self.inverse_transform(global_start)

        global_dir = np.array(ray.get_Direction(), dtype=float)
        local_dir = self.inverse_transform(global_start + global_dir) - local_start
        local_dir = local_dir / np.linalg.norm(local_dir)

        x0, y0, z0 = local_start
        dx, dy, dz = local_dir

        c = 1.0 / self.Rc
        K = self.K

        # F(x,y,z) = c*(x^2 + y^2) + c*(K + 1)*z^2 - 2*z = 0
        # After substitution:
        # A*t^2 + 2*B*t + C = 0
        A = c * (dx * dx + dy * dy) + c * (K + 1.0) * dz * dz
        B = c * (x0 * dx + y0 * dy) + c * (K + 1.0) * z0 * dz - dz
        C = c * (x0 * x0 + y0 * y0) + c * (K + 1.0) * z0 * z0 - 2.0 * z0

        eps_t = 1e-5
        eps_disc = 1e-12
        eps_z = 1e-5

        if abs(A) < eps_disc:
            if abs(B) < eps_disc:
                return None
            roots = [-C / (2.0 * B)]
        else:
            discriminant = B * B - A * C
            if discriminant < -eps_disc:
                return None

            discriminant = max(0.0, discriminant)
            sqrt_disc = np.sqrt(discriminant)

            t1 = (-B + sqrt_disc) / A
            t2 = (-B - sqrt_disc) / A
            roots = [t1, t2]

        valid_roots = sorted([t for t in roots if t > eps_t])
        if not valid_roots:
            return None

        for t_local in valid_roots:
            local_intersection = local_start + t_local * local_dir
            x_hit, y_hit, z_hit = local_intersection

            r2_hit = x_hit * x_hit + y_hit * y_hit

            if r2_hit > self.radius * self.radius:
                continue
            if r2_hit < self.centerHoleRadius * self.centerHoleRadius:
                continue

            expected_z = self.function(x_hit, y_hit)
            if expected_z is None:
                continue

            expected_z = float(expected_z)

            if abs(z_hit - expected_z) > eps_z:
                continue

            intersectionPoint = self.transform(local_intersection)
            return intersectionPoint, ray.get_Color()

        return None

    def calculate_BeamIntersection(self, beam):
        return [self.calculate_RayIntersection(ray) for ray in beam.get_Rays()]

    def create_dummy_hole(self, centerHoleRadius):
        X = np.where(
            self.x_grid ** 2 + self.y_grid ** 2 <= centerHoleRadius ** 2,
            np.nan,
            self.x_grid
        )
        Y = np.where(
            self.x_grid ** 2 + self.y_grid ** 2 <= centerHoleRadius ** 2,
            np.nan,
            self.y_grid
        )

        self.visual = SurfacePlot(X, Y, self.z_grid, color=(0.3, 0.3, 1.0, 0.3))
        self.visual.transform = scene.transforms.MatrixTransform()

    def is_point_inside_volume(self, point):
        local_point = self.inverse_transform(point)
        x, y, z = local_point
        r_squared = x * x + y * y
        return r_squared <= (self.radius ** 2 + 1e-5)