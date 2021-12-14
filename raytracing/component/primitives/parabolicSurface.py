import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot
from .surface import Surface
from ..miscellaneous_components import display_point


class Parabolic_Surface(Surface):
	def __init__(self, a, b, c, radius=1.0, center=(0, 0, 0), name=None, xTilt=0.0, yTilt=0.0, color='black', parentCanvas=None):
		"""
		Creates the data of a paraboloid whose center, radius and a, b, c parameters are given as inputs
		"""
		# Generate the grid in cylindrical coordinates
		self.radius = radius
		
		r = np.linspace(0, self.radius, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		R, THETA = np.meshgrid(r, theta)
		
		self.parameters = (a, b, c)
		
		# Convert to rectangular coordinates
		self.x_grid, self.y_grid = R * np.cos(THETA), R * np.sin(THETA)
		
		# self.z_grid  = c * ((self.x_grid / a) ** 2 + (self.y_grid / b) ** 2) # Elliptic paraboloid
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
	
	def calculate_normalDirection(self, point):
		# Calculate by using vector calculus formula: Normal=grad(F)@point
		x0, y0, z0 = point #self.inverse_transform(point)
		a, b, c = self.parameters
		A = 2 * x0 / a ** 2
		B = 2 * y0 / b ** 2
		C = -c
		dc = np.array((A, B, C))
		normal_Direction = c * (
					dc / np.linalg.norm(dc))  # Multiply with c to accommodate for the direction of the surface
		assert all(isinstance(n, float) for n in normal_Direction), print("No real solution for normal direction: ", normal_Direction)
		# self.transform(normal_Direction)
		return normal_Direction
	
	def calculate_RayIntersection(self, ray):
		a, b, c = self.parameters
		x0, y0, z0 = ray.get_StartPoint() # self.inverse_transform(ray.get_StartPoint())
		dx, dy, dz = ray.get_Direction() # self.inverse_transform(ray.get_Direction())
		
		A = (dx / a) ** 2 + (dy / b) ** 2
		B = (((2 * dx * x0) / a ** 2) + ((2 * dy * y0) / b ** 2) - (dz / c))
		C = (x0 / a) ** 2 + (y0 / b) ** 2 - (z0 / c)
		root = np.roots((A, B, C))
		
		# TODO To select one of the roots based on a proper criteria (substitute in the surface equation, checking if the point is within bounds)
		print("root= ", root)
		r = root[1] if len(root) > 1 else root
		intersectionPoint = ray.get_StartPoint() + (r * ray.get_Direction())
		if all(isinstance(n, complex) for n in intersectionPoint):
			print("No real solution for intersection point: " + str(intersectionPoint) + " r: " + str(r))
			r = root[0]
			intersectionPoint = ray.get_StartPoint() + (r * ray.get_Direction())
		
		display_point(intersectionPoint, marker='+', color='teal', parentCanvas=self.parentCanvas)
		# intersectionPoint=self.transform(intersectionPoint)
		# display_point(intersectionPoint, marker='x', color='white', parentCanvas=self.parentCanvas)
		# print("intersection= ", intersectionPoint)
		return intersectionPoint
	
	def calculate_BeamIntersection(self, beam):
		intersectionPoints = []
		for ray in beam.get_Rays():
			intersectionPoints.append(self.calculate_RayIntersection(ray))
		
		return intersectionPoints
	
	def create_hole(self, holeRadius):
		# Z = np.where(self.z_grid < holeRadius, np.NAN, self.z_grid)
		X = np.where(self.x_grid ** 2 + self.y_grid ** 2 <= holeRadius ** 2, np.NAN, self.x_grid)
		Y = np.where(self.x_grid ** 2 + self.y_grid ** 2 <= holeRadius ** 2, np.NAN, self.y_grid)
		
		self.visual = SurfacePlot(X, Y, self.z_grid, color=(0.3, 0.3, 1, 0.3))
		
		self.visual.transform = scene.transforms.MatrixTransform()
