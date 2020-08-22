import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot, Line
from scipy.spatial.transform import Rotation


class LineVector:
	def __init__(self, start, direction, length=1, color='Blue'):
		"""
		Creates a line or line segment object for rendering
		:param: start: Starting coordinate of the line
		:param: direction: Direction cosines of the line with respect to the openPyOpticalBench coordinates
		:param length: Length of the line segment (Optional). Default: Unit length
		:param color: Color to be shown when the line is being visualized (Optional). Default='Blue'
		"""
		self.lineStart = np.array(start)
		self.direction = np.array(direction)
		# TODO: assert
		# assert self.direction-1 < 1, "No: {0}, {1}, {2}".format(self.direction[0]-1, self.direction[1]-1, self.direction[2]-1)
		self.length = length
		self.color = color
		self.lineEnd = None
		self.vector = None
		self.lineVisual = None
		
		self.create_Vector()
	
	def create_Vector(self):
		self.lineEnd = self.lineStart + self.length * self.direction
		self.vector = self.lineEnd - self.lineStart
		
		# Create line Visual passing through two points
		self.lineVisual = Line(np.array([self.lineStart, self.lineEnd]), connect='strip', method='gl', width=2,
		                       color=self.color)
	
	def update_Vector(self, endPoint):
		endPoint = np.array(endPoint)
		if not np.array_equal(self.lineEnd, endPoint):  # Do not update if there is no change
			self.lineEnd = endPoint
			self.vector = self.lineEnd - self.lineStart
			self.length = np.linalg.norm(self.vector)
			
			# Create line Visual passing through two points
			self.lineVisual = Line(np.array([self.lineStart, self.lineEnd]), connect='strip', method='gl', width=2,
			                       color=self.color)
	
	def extend_Vector(self, length):
		if self.length != length:  # Do not update if there is no change
			self.length = length
			self.create_Vector()
	
	def get_Direction_Cosines(self):
		direction_ratios = self.lineEnd - self.lineStart
		direction_cosines = direction_ratios / np.linalg.norm(direction_ratios)
		return direction_cosines
	
	def get_Direction_Angles(self):
		direction_ratios = self.lineEnd - self.lineStart
		direction_angles = np.rad2deg(np.arccos(direction_ratios / np.linalg.norm(direction_ratios)))
		return direction_angles
	
	def get_visual(self):
		return self.lineVisual
	
	def translate(self, point):
		"""
		Translate the vector to a new origin without changing the length
		:param point: Starting Point to which the vector should be shifted
		"""
		point = np.array(point)
		if not np.array_equal(self.lineStart, point):  # Do not update if there is no change
			self.lineStart = point
			self.create_Vector()
	
	def rotate(self, axis, angle):
		"""
		Rotate the vector by an angle about an axis using Rodrigues formula
		:param axis: Axis about which the vector will be rotated
		:param angle: angle in degrees about which the vector will be rotated
		:return:
		"""
		# vector = np.array(vector)
		axis = np.array(axis)
		theta = np.deg2rad(angle)
		self.direction = self.vector * np.cos(theta) + (np.cross(axis, self.vector) * np.sin(theta)) + (
				np.dot(axis, self.vector) * axis * (1 - np.cos(theta)))  # Rodrigues formula
		self.create_Vector()
		"""
	def transform(self, transform):
		"" "
		Transform the vector under the transformation given by the transformation matrix
		:param transform: transformation matrix
		:return: transformed vector
		""
		pass"""


######################################################################################################################
class Surface:
	def __init__(self, center, x_grid, y_grid, z_grid, xTilt=0.0, yTilt=0.0, color="black"):
		"""
		Creates a plane surface with the given center and normal with the specified media
		:param center: Center of the plane with respect to the pyOpticalBench coordinates
		:param xTilt: tilt of the plane with respect to pyOpticalBench X axis
		:param yTilt: tilt of the plane with respect to pyOpticalBench Y axis
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "Green"
		"""
		self.center = np.array((0, 0, 0))
		final_center = np.array(center)
		normalDirection = np.array((0, 0, 1))  # Create a plane with normal parallel to z-axis direction (xy plane)
		self.xTilt = xTilt
		self.yTilt = yTilt
		self.color = color
		
		self.__translationMatrix = np.zeros(3)
		self.__rotationMatrix = Rotation.from_rotvec(np.zeros(3)) # Create a rotation matrix with zero degrees rotation
		# print("rot=\n", self.__rotationMatrix.as_matrix())
		
		self.normal = LineVector(start=self.center, direction=normalDirection, color='w')
		
		self.visual = SurfacePlot(x=x_grid, y=y_grid, z=z_grid, color=color)
		self.visual.transform = scene.transforms.MatrixTransform()
		self.rotate_aboutX(self.xTilt)
		self.rotate_aboutY(self.yTilt)
		self.translate(final_center)
	
	def get_Visual(self):
		return self.visual
	
	def get_normalVisual(self):
		return self.normal.get_visual()
	
	def function(self, x, y):
		"""To be implemented by the child surface"""
		pass
	
	def calculate_normalDirection(self, point):
		""" To be implemented by the child surface"""
		pass
	
	def calculate_RayIntersection(self, ray):
		""" To be implemented by the child surface"""
		pass
	
	def calculate_BeamIntersection(self, beam):
		""" To be implemented by the child surface"""
		pass
	
	def get_chiefNormalDirection(self):
		return self.normal.get_Direction_Cosines()
	
	def __rotate(self, angle, axis):
		if not all(self.center == 0):
			self.visual.transform.translate(-self.center)
		self.visual.transform.rotate(angle, axis)
		self.visual.transform.translate(self.center)
		self.normal.rotate(axis, angle)
		
		self.__rotationMatrix *= Rotation.from_rotvec(np.deg2rad(angle)*np.array(axis))
		
		# csTta, snTta= np.cos(angle), np.sin(angle)
		# ux,uy,uz=axis
		# rotation_matrix = np.array([[csTta + (ux * ux * (1 - csTta)), (ux * uy * (1 - csTta)) - (ux * snTta), (ux * uz * (1 - csTta)) + (uy * snTta)],
		#                             [(uy * ux * (1 - csTta)) + (ux * snTta), csTta + (uy * uy * (1 - csTta)), (uy * uz * (1 - csTta)) + (ux * snTta)],
		#                             [(uz * ux * (1 - csTta)) - (uy * snTta), (uz * uy * (1 - csTta)) + (ux * snTta), csTta + (uz * uz * (1 - csTta))]])
		# print("rotation_matrix:\n", rotation_matrix)
		# self.__rotationMatrix *= rotation_matrix
		# assert np.array_equal(self.__rotationMatrix.transpose(), self.__rotationMatrix), "Rotation matrix is not orthogonal:\n" + str(self.__rotationMatrix)
		# print(self.__rotationMatrix.as_matrix())
		# self.normal = LineVector(start=self.center, direction=self.normalDirection, color='w') # Update the normal
	
	
	
	def rotate_aboutX(self, angle):
		self.__rotate(angle, [1, 0, 0])
	
	def rotate_aboutY(self, angle):
		self.__rotate(angle, [0, 1, 0])
	
	def rotate_aboutZ(self, angle):
		self.__rotate(angle, [0, 0, 1])
	
	def translate(self, point):
		point = np.array(point)
		# Shift the surface back to origin of the pyOpticalBench as the point is defined wrt this origin
		if not all(self.center == 0):
			self.visual.transform.translate(-self.center)
		self.visual.transform.translate(pos=np.array(point))
		self.center = point
		self.normal.translate(self.center)
		self.__translationMatrix += self.center  # Update the translation matrix for transformation of coordinates
	
	def transform(self, point):
		# TODO First rotate, then translate
		# print("Point: ",point, self.translationMatrix)
		# transformedPoint = np.array(self.__rotationMatrix.apply(point) + self.__translationMatrix)
		transformedPoint = np.array(point+self.__translationMatrix)
		# print("translated Point: ",point)
		return transformedPoint
	
	def inverse_transform(self, point):
		# rotation = self.__rotationMatrix.inv()
		transformedPoint = np.array(self.__rotationMatrix.apply(point, inverse=True) - self.__translationMatrix)
		return transformedPoint


#######################################################################################################################
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


#######################################################################################################################
class Plane_Circular(Surface):
	def __init__(self, radius=1.0, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='black'):
		"""
		Creates the data for a circular plane whose center, radius are given as inputs
		"""
		# Generate the grid in cylindrical coordinates
		self.radius = radius
		
		r = np.linspace(0, self.radius, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		R, THETA = np.meshgrid(r, theta)
		
		# Convert to rectangular coordinates
		x_grid, y_grid = R * np.cos(THETA), R * np.sin(THETA)
		
		z_grid = np.zeros(np.shape(x_grid))
		
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt,
		                 color=color)


#######################################################################################################################
class Parabolic_Surface(Surface):
	def __init__(self, a, b, c, radius=1.0, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='black'):
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
		
		super().__init__(center=center, x_grid=self.x_grid, y_grid=self.y_grid, z_grid=self.z_grid, xTilt=xTilt,
		                 yTilt=yTilt, color=color)
	
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
		assert all(isinstance(n, float) for n in normal_Direction), print("No real solution for normal direction: ",
		                                                                  normal_Direction)
		# self.transform(normal_Direction)
		return normal_Direction
	
	def calculate_RayIntersection(self, ray):
		a, b, c = self.parameters
		x0, y0, z0 = self.inverse_transform(ray.get_StartPoint())
		dx, dy, dz = self.inverse_transform(ray.get_Direction())
		
		A = (dx / a) ** 2 + (dy / b) ** 2
		B = (((2 * dx * x0) / a ** 2) + ((2 * dy * y0) / b ** 2) - (dz / c))
		C = (x0 / a) ** 2 + (y0 / b) ** 2 - (z0 / c)
		r = np.roots((A, B, C))
		
		# TODO TO select one of the roots based on a proper criteria
		print("r= ", r)
		if len(r) > 1:
			r = r[1]
		intersectionPoint = ray.get_StartPoint() + (r * ray.get_Direction())
		assert all(isinstance(n, float) for n in intersectionPoint), print("No real solution for intersection point: ",
		                                                                   intersectionPoint, " r: ", r)
		
		intersectionPoint=self.transform(intersectionPoint)
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


########################################################################################################################
class Cylinder(Surface):
	def __init__(self, radius=1.0, length=1.0, center=(0, 0, 0), xTilt=0.0, yTilt=0.0, color='black'):
		""" Creates the data of a cylinder oriented along z axis whose center, radius and length are given as inputs
		Based on the example given at: https://stackoverflow.com/a/49311446/2602319
		"""
		z = np.linspace(-length / 2, length / 2, 100)
		theta = np.linspace(0, 2 * np.pi, 100)
		theta_grid, z_grid = np.meshgrid(theta, z)
		x_grid = radius * np.cos(theta_grid)
		y_grid = radius * np.sin(theta_grid)
		
		super().__init__(center=center, x_grid=x_grid, y_grid=y_grid, z_grid=z_grid, xTilt=xTilt, yTilt=yTilt,
		                 color=color)
