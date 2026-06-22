import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot
from .surface import Surface
# from ..miscellaneous_components import display_point
# from opticsLab.raytracing.component import Point

class Parabolic_Surface(Surface):
	def __init__(self, a, b, c, radius=1.0, centerHoleRadius=0.0, center=(0, 0, 0),
				 mediumAfter="Air", mediumBefore="Air", name=None, xTilt=0.0, yTilt=0.0,
				 color='black', parentCanvas=None, n_r=100, n_theta=100):
		"""
		Creates the data of a paraboloid whose center, radius and a, b, c parameters are given as inputs
		"""
		# Generate the grid in cylindrical coordinates
		self.mediumBefore = mediumBefore
		self.mediumAfter = mediumAfter
		self.radius = radius
		self.centerHoleRadius = centerHoleRadius
		
		#r = np.linspace(0, self.radius, 100)
		r = np.linspace(self.centerHoleRadius, self.radius, n_r)
		theta = np.linspace(0, 2 * np.pi, n_theta)
		R, THETA = np.meshgrid(r, theta)
		
		self.parameters = (a, b, c)
		
		# Convert to rectangular coordinates
		self.x_grid, self.y_grid = R * np.cos(THETA), R * np.sin(THETA)
		
		#self.z_grid  = c * ((self.x_grid / a) ** 2 + (self.y_grid / b) ** 2) # Elliptic paraboloid
		self.z_grid = self.function(self.x_grid, self.y_grid)
		
		super().__init__(center=center, x_grid=self.x_grid, y_grid=self.y_grid, z_grid=self.z_grid, name=name, xTilt=xTilt,
		                 yTilt=yTilt, color=color, parentCanvas=parentCanvas)
	
	def function(self, x, y):
		if type(x) != np.ndarray or type(y) != np.ndarray:
			if np.sqrt(x * x + y * y) > self.radius:
				return None
		a, b, c = self.parameters
		z = c * ((x / a) ** 2 + (y / b) ** 2)  # Elliptic paraboloid
		# TODO to verify intersection point is outside the surface

		return z
	
	# def calculate_normalDirection(self, point):
	# 	# Calculate by using vector calculus formula: Normal=grad(F)@point
	# 	x0, y0, z0 = self.inverse_transform(point) #point #jay edit
	# 	a, b, c = self.parameters
	# 	A = 2 * x0 / (a ** 2)
	# 	B = 2 * y0 / (b ** 2)
	# 	C = -c
	# 	dc = np.array((A, B, C))
	# 	normal_Direction = c * (
	# 				dc / np.linalg.norm(dc))  # Multiply with c to accommodate for the direction of the surface
	# 	assert all(isinstance(n, float) for n in normal_Direction), print("No real solution for normal direction: ", normal_Direction)
	#
	# 	origin_transformed = self.transform(np.array([0.0,0.0,0.0])) #jay edit
	# 	normal_Direction   = self.transform(normal_Direction) - origin_transformed #jay edit
	#
	# 	#self.transform(normal_Direction)   #dvs original
	# 	return normal_Direction

	def calculate_normalDirection(self, point):
		x0, y0, z0 = self.inverse_transform(point)
		a, b, c = self.parameters

		local_normal = np.array([
			2.0 * c * x0 / (a ** 2),
			2.0 * c * y0 / (b ** 2),
			-1.0
		], dtype=float)

		local_normal = local_normal / np.linalg.norm(local_normal)

		global_normal = self.rotate_vector(local_normal)
		global_normal = global_normal / np.linalg.norm(global_normal)

		return global_normal
	
	# def calculate_RayIntersection(self, ray):
	# 	a, b, c = self.parameters
	# 	# x0, y0, z0 = ray.get_StartPoint()
	# 	# x0, y0, z0 = self.transform(ray.get_StartPoint())
	# 	x0, y0, z0 = self.inverse_transform(ray.get_StartPoint()) #jay edit
	#
	# 	dx, dy, dz = ray.get_Direction() # self.inverse_transform(ray.get_Direction())
	#
	# 	A = (dx / a) ** 2 + (dy / b) ** 2
	# 	B = (((2 * dx * x0) / a ** 2) + ((2 * dy * y0) / b ** 2) - (dz / c))
	# 	C = (x0 / a) ** 2 + (y0 / b) ** 2 - (z0 / c)
	# 	root = np.roots((A, B, C))
	#
	# 	# TODO To select one of the roots based on a proper criteria (substitute in the surface equation, checking if the point is within bounds)
	# 	print("root= ", root)
	# 	r = root[1] if len(root) > 1 else root
	# 	intersectionPoint = ray.get_StartPoint() + (r * ray.get_Direction())
	# 	if all(isinstance(n, complex) for n in intersectionPoint):
	# 		print("No real solution for intersection point: " + str(intersectionPoint) + " r: " + str(r))
	# 		r = root[0]
	# 		intersectionPoint = ray.get_StartPoint() + (r * ray.get_Direction())
	#
	# 	# display_point(intersectionPoint, marker='+', color='teal', parentCanvas=self.parentCanvas)
	# 	intersectionPoint=self.inverse_transform(intersectionPoint)
	# 	# intersectionPoint = Point(intersectionPoint[0], intersectionPoint[1], intersectionPoint[2], parentCanvas=self.parentCanvas)
	# 	# display_point(intersectionPoint, marker='x', color='white', parentCanvas=self.parentCanvas)
	# 	print("intersection= ", intersectionPoint)
	# 	return intersectionPoint, ray.get_Color()

	def calculate_RayIntersection(self, ray):
		a, b, c = self.parameters

		# 1. Start Point (Translate AND Rotate)
		global_start = ray.get_StartPoint()
		local_start = self.inverse_transform(global_start)
		x0, y0, z0 = local_start

		# 2. Direction (ONLY Rotate, DO NOT Translate!)
		global_dir = ray.get_Direction()
		# The safest way to do this without writing a new function:
		# Transform a point exactly 1 unit along the direction, then subtract the local start
		local_dir = self.inverse_transform(global_start + global_dir) - local_start

		# Normalize the local direction just to be safe
		local_dir = local_dir / np.linalg.norm(local_dir)
		dx, dy, dz = local_dir

		# 3. Math
		A = (dx / a) ** 2 + (dy / b) ** 2
		B = (((2 * dx * x0) / a ** 2) + ((2 * dy * y0) / b ** 2) - (dz / c))
		C = (x0 / a) ** 2 + (y0 / b) ** 2 - (z0 / c)

		roots = np.roots((A, B, C))

		# 4. Find closest intersection in FRONT of the ray (t > epsilon)
		valid_roots = [r.real for r in roots if np.isreal(r) and r.real > 1e-5]
		if not valid_roots:
			return None

		t_local = min(valid_roots)

		# 5. Calculate intersection in LOCAL space first
		local_intersection = local_start + (t_local * local_dir)

		# 6. Transform the local intersection back to GLOBAL space
		intersectionPoint = self.transform(local_intersection)

		return intersectionPoint, ray.get_Color()
	
	def calculate_BeamIntersection(self, beam):
		intersectionPoints = []
		for ray in beam.get_Rays():
			intersectionPoints.append(self.calculate_RayIntersection(ray))
		
		return intersectionPoints
	
	def create_dummy_hole(self, centerHoleRadius):
		# Z = np.where(self.z_grid < centerHoleRadius, np.NAN, self.z_grid)
		X = np.where(self.x_grid ** 2 + self.y_grid ** 2 <= centerHoleRadius ** 2, np.NAN, self.x_grid)
		Y = np.where(self.x_grid ** 2 + self.y_grid ** 2 <= centerHoleRadius ** 2, np.NAN, self.y_grid)
		
		self.visual = SurfacePlot(X, Y, self.z_grid, color=(0.3, 0.3, 1, 0.3))
		
		self.visual.transform = scene.transforms.MatrixTransform()
		
	def create_hole(self):
		thickness = self.radius - self.centerHoleRadius
		theta = np.linspace(0, 2 * np.pi, 100)
		z = np.linspace(0, self.height, 100)
		theta_grid, z_grid = np.meshgrid(theta, z)
		x_grid = (self.radius - thickness) * np.cos(theta_grid) + self.center[0]
		y_grid = (self.radius - thickness) * np.sin(theta_grid) + self.center[1]
		self.inner_cylinder_visual = SurfacePlot(x_grid, y_grid, z_grid, color=self.color, parent=self.parentCanvas)
		# self.inner_cylinder_visual.transform = vispy.scene.transforms.MatrixTransform()

	def is_point_inside_volume(self, point):
		# Translate point to the cylinder's local coordinate system
		local_point = self.inverse_transform(point)
		x, y, z = local_point

		# Inside cylinder if x^2 + y^2 <= radius^2 and z is within length
		r_squared = x ** 2 + y ** 2

		# Optionally, you don't even need to check Z here because the
		# parabolic surfaces act as the top and bottom Z bounds!
		return r_squared <= (self.radius ** 2 + 1e-5)