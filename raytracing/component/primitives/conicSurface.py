import numpy as np
from raytracing.component.primitives.surface import Surface
from vispy import scene
from vispy.scene.visuals import SurfacePlot

# class ConicSurface(Surface):
# 	def __init__(self, center, radius=1.0, RoC=2.0, K=1.0, name=None, xTilt=0.0, yTilt=0.0, mediumAfter="Air", mediumBefore="Air", color="green", parentCanvas=None):
# 		"""
# 		Creates a conic surface with the given center and normal with the specified media
# 		:param center: Center of the surface with respect to the opticsLab coordinates
# 		:param radius: radius of the surface. Default: 1.0
# 		:param RoC: Radius of Curvature of the conic. Default: 1.0
# 		:param K: Conic Constant. Sphere: K = 0; Oblate ellipsoids: K > 0; Prolate Ellipsoids: −1 < K < 0; Paraboloid: K = −1; Hyperboloids: K < −1
# 		:param: name: Name of the surface for debugging purposes (optional)
# 		:param xTilt: tilt of the surface with respect to opticsLab X axis
# 		:param yTilt: tilt of the surface with respect to opticsLab Y axis
# 		:param mediumAfter: Medium after the surface
# 		:param mediumBefore: Medium before the surface (optional). Default: "Air"
# 		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "green"
# 		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
# 		"""
# 		self.mediumBefore=mediumBefore
# 		self.mediumAfter=mediumAfter
#
# 		# Generate the grid in cylindrical coordinates
# 		self.radius = radius
#
# 		r = np.linspace(0, self.radius, 100)
# 		theta = np.linspace(0, 2 * np.pi, 100)
# 		R, THETA = np.meshgrid(r, theta)
#
# 		self.parameters = (RoC, K)
#
# 		# Convert to rectangular coordinates
# 		x_grid, y_grid = R * np.cos(THETA), R * np.sin(THETA)
#
# 		# p = RoC/(K+1)
# 		# z_grid = p - np.sqrt(p*p - ((x_grid**2+y_grid**2)/(K+1)))
# 		t=R**2/RoC
# 		z_grid = t / (1 + np.sqrt(1 - ((1 + K) * t / RoC)))
# 		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, name=name, xTilt=xTilt, yTilt=yTilt, color=color, parentCanvas=parentCanvas)

class ConicSurface(Surface):
	def __init__(self, radius=1.0, RoC=8000.0, K=0.0, centerHoleRadius=0.0,
				 center=(0, 0, 0), mediumAfter="Air", mediumBefore="Air",
				 name=None, xTilt=0.0, yTilt=0.0, color='black',
				 parentCanvas=None, n_r=100, n_theta=100):
		"""
        A general optical conic surface defined by vertex radius R and conic constant K.
        - K > 0     : Oblate ellipsoid
        - K = 0     : Sphere
        - -1 < K < 0: Prolate ellipsoid
        - K = -1    : Paraboloid
        - K < -1    : Hyperboloid
        """
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		self.radius = radius
		self.centerHoleRadius = centerHoleRadius
		self.Rc = float(RoC)  # Vertex radius of curvature
		self.K = float(K)  # Conic constant

		r = np.linspace(self.centerHoleRadius, self.radius, n_r)
		theta = np.linspace(0, 2 * np.pi, n_theta)
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
		"""Evaluates the standard optical conic sag equation."""
		if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
			if np.sqrt(x * x + y * y) > self.radius:
				return None

		r2 = x * x + y * y
		c = 1.0 / self.Rc
		inside = 1.0 - (1.0 + self.K) * (c * c) * r2

		if isinstance(inside, np.ndarray):
			inside = np.maximum(inside, 0.0)
		elif inside < 0:
			return None

		z = (c * r2) / (1.0 + np.sqrt(inside))
		return z

	def calculate_normalDirection(self, point):
		"""Returns the exact global normal vector at a given 3D point on the surface."""
		x0, y0, z0 = self.inverse_transform(point)

		c = 1.0 / self.Rc

		# Exact analytic normal derived from the implicit conic equation
		# F(x,y,z) = c*(x^2 + y^2) + c*(K+1)*z^2 - 2*z = 0
		local_normal = np.array([
			-c * x0,
			-c * y0,
			1.0 - c * (self.K + 1.0) * z0
		], dtype=float)

		# Normalize the local vector
		local_normal /= np.linalg.norm(local_normal)

		# Rotate to global coordinates
		global_normal = self.rotate_vector(local_normal)
		global_normal /= np.linalg.norm(global_normal)

		return global_normal


	def calculate_RayIntersection(self, ray, max_iter=50, tol=1e-6):
		"""
        Calculates exact analytic intersection of a ray with the conic surface.

        IMPORTANT:
        The quadric equation represents the full conic sheet(s), but the optical sag
        function self.function(x, y) defines the specific physical branch we want.
        So we solve the quadric analytically, then validate candidate roots against
        the sag equation and aperture limits.
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

		# Implicit conic:
		# F(x,y,z) = c*(x^2 + y^2) + c*(K + 1)*z^2 - 2*z = 0
		#
		# Substitute ray:
		# x = x0 + t*dx, y = y0 + t*dy, z = z0 + t*dz
		#
		# This yields:
		# A*t^2 + 2*B*t + C = 0
		A = c * (dx * dx + dy * dy) + c * (K + 1.0) * dz * dz
		B = c * (x0 * dx + y0 * dy) + c * (K + 1.0) * z0 * dz - dz
		C = c * (x0 * x0 + y0 * y0) + c * (K + 1.0) * z0 * z0 - 2.0 * z0

		eps_t = 1e-5
		eps_disc = 1e-12
		eps_z = 1e-5

		roots = []

		if abs(A) < eps_disc:
			# Degenerate linear case
			if abs(B) < eps_disc:
				return None
			t = -C / (2.0 * B)
			roots = [t]
		else:
			discriminant = B * B - A * C

			if discriminant < -eps_disc:
				return None

			discriminant = max(0.0, discriminant)
			sqrt_disc = np.sqrt(discriminant)

			t1 = (-B + sqrt_disc) / A
			t2 = (-B - sqrt_disc) / A
			roots = [t1, t2]

		# Only forward intersections
		valid_roots = sorted([t for t in roots if t > eps_t])
		if not valid_roots:
			return None

		# Check each candidate root against:
		# 1. aperture / center hole
		# 2. actual sag branch self.function(x, y)
		for t_local in valid_roots:
			local_intersection = local_start + t_local * local_dir
			x_hit, y_hit, z_hit = local_intersection

			r2_hit = x_hit * x_hit + y_hit * y_hit

			# Aperture and center-hole clipping
			if r2_hit > self.radius * self.radius:
				continue
			if r2_hit < self.centerHoleRadius * self.centerHoleRadius:
				continue

			expected_z = self.function(x_hit, y_hit)
			if expected_z is None:
				continue

			# For scalar function output
			expected_z = float(expected_z)

			# Keep only the root that lies on the same physical sag branch
			if abs(z_hit - expected_z) > eps_z:
				continue

			intersectionPoint = self.transform(local_intersection)
			return intersectionPoint, ray.get_Color()

		return None

	def create_dummy_hole(self, centerHoleRadius):
		X = np.where(self.x_grid ** 2 + self.y_grid ** 2 <= centerHoleRadius ** 2, np.nan, self.x_grid)
		Y = np.where(self.x_grid ** 2 + self.y_grid ** 2 <= centerHoleRadius ** 2, np.nan, self.y_grid)

		self.visual = SurfacePlot(X, Y, self.z_grid, color=(0.3, 0.3, 1, 0.3))
		self.visual.transform = scene.transforms.MatrixTransform()

	def is_point_inside_volume(self, point):
		local_point = self.inverse_transform(point)
		x, y, z = local_point
		r_squared = x ** 2 + y ** 2
		return r_squared <= (self.radius ** 2 + 1e-5)