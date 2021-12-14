import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot
from scipy.spatial.transform import Rotation

from .lineVector import LineVector
from .constants import Z_AXIS_DIRECTION
from .primitive_point import Primitive_point

class Surface:
	def __init__(self, center, x_grid, y_grid, z_grid, name=None, xTilt=0.0, yTilt=0.0, color="black", parentCanvas=None):
		"""
		Creates a surface with the given center and normal with the specified media
		:param center: Center of the plane with respect to the pyOptiCAD coordinates. Can be a Point object or numpy array.
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
		:param: name: Name of the surface for debugging purposes (optional)
		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "Green"
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		"""
		self.center = np.array((0, 0, 0))
		self.name = name
		final_center = center.get_coordinates() if isinstance(center, Primitive_point) else np.array(center)
		normalDirection = Z_AXIS_DIRECTION  # Create a surface with normal parallel to z-axis direction (xy plane)
		self.xTilt = xTilt
		self.yTilt = yTilt
		self.color = color
		self.parentCanvas = parentCanvas
		
		self.Q = None
		
		self.__translationMatrix = np.zeros(3)
		self.__rotationMatrix = Rotation.from_rotvec(np.zeros(3)) # Create a rotation matrix with zero degrees rotation
		# print("rot=\n", self.__rotationMatrix.as_matrix())
		
		self.normal = LineVector(start=self.center, direction=normalDirection, color='w')
		
		parent = None if self.parentCanvas is None else self.parentCanvas.view.scene
		self.visual = SurfacePlot(x=x_grid, y=y_grid, z=z_grid, color=color, parent=parent)
		self.visual.transform = scene.transforms.MatrixTransform()
		self.rotate_aboutX(self.xTilt)
		self.rotate_aboutY(self.yTilt)
		self.translate(final_center)
	
	def get_Visual(self):
		return self.visual
	
	def get_normalVisual(self):
		return self.normal.get_visual()
	
	def showNormal(self):
		self.parentCanvas.view.add(self.normal.get_visual())
	
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
			self.visual.transform.translate(-self.center) # Bring to origin
		self.visual.transform.rotate(angle, axis)
		self.visual.transform.translate(self.center)
		self.normal.rotate(axis, angle)
		
		self.__rotationMatrix *= Rotation.from_rotvec(np.deg2rad(angle)*np.array(axis)) # Multiply quaternions
		print(self.name, " rot matrix: ", np.rad2deg(self.__rotationMatrix.as_rotvec()))
	
	
	def rotate_aboutX(self, angle):
		self.__rotate(angle, (1, 0, 0))
	
	def rotate_aboutY(self, angle):
		self.__rotate(angle, (0, 1, 0))
	
	def rotate_aboutZ(self, angle):
		self.__rotate(angle, (0, 0, 1))
	
	def translate(self, point):
		point = np.array(point)
		# Shift the surface back to origin of the pyOptiCAD as the point is defined wrt this origin
		if not all(self.center == 0):
			self.visual.transform.translate(-self.center)
		self.visual.transform.translate(pos=np.array(point))
		self.center = point
		self.normal.translate(self.center)
		self.__translationMatrix += self.center  # Update the translation matrix for transformation of coordinates
	
	def transform(self, point):
		# TODO First rotate, then translate
		# print("Point: ",point, self.translationMatrix)
		transformedPoint = np.array(self.__rotationMatrix.apply(point))# + self.__translationMatrix)
		# transformedPoint = np.array(point+self.__translationMatrix)
		# print("translated Point: ",point)
		return transformedPoint
	
	def inverse_transform(self, point):
		# rotation = self.__rotationMatrix.inv()
		transformedPoint = np.array(self.__rotationMatrix.apply(point, inverse=True))# - self.__translationMatrix)
		return transformedPoint
	
	def create_quadric(self, A,B,C,D,E,F,G,H,I,J):
		self.Q = np.matrix([[A,B,C,D],[B,E,F,G],[C,F,H,I],[D,G,I,J]])
		
	def calculate_quadric_intersection(self, ray):
		p = np.array([np.append(ray.get_StartPoint(),[1])]).T # To convert to quadric equation compatible form
		d = np.array([np.append(ray.get_Direction(),[1])]).T # To convert to quadric equation compatible form
		
		# squeeze is used to remove the axes of length 1. Since the output is a scalar, but the numpy product results in a 2D array
		dTQ = d.T * self.Q
		A = np.squeeze(np.array((dTQ * d)))
		B = 2 * np.squeeze(np.array(dTQ * p))
		C = np.squeeze(np.array(p.T * self.Q * p))
		#
		# A = np.dot(np.dot(d.T,self.Q),d) ** 2
		# B = 2 * np.dot(np.dot(d.T, self.Q), p)
		# C = np.dot(np.dot(p.T, self.Q), p)
		
		if A == 0:
			print("A=0, returning -C/B")
			return -C/B
		# else:
		discriminant = B ** 2 - (4*A*C)
		
		print("d,p,dTQ, A,B,C, discriminant, {d, dTQ shape} = ", d,p, dTQ, A, B, C, discriminant, "{",np.shape(d), np.shape(dTQ), "}")
		if discriminant < 0:
			print("No intersection")
			return None
		elif discriminant == 0:
			print("Ray is tangent to the quadric surface ", self.name)
			return  -B/(2*A)
		else: # if discriminant > 0
			x1 = (-B + np.sqrt(discriminant))/(2*A)
			x2 = (-B - np.sqrt(discriminant))/(2*A)
			print("x1,x2 = ",x1,x2)
			if x1 >= 0:
				print("Selecting first root")
				return x1
			elif x2 >= 0:
				print("Selecting second root")
				return x2
			else:
				print("Unknown case")
				return x1
				
	def calculate_quadric_normal(self, point):
		n = np.squeeze(np.array(self.Q[:-1,:] * np.array([np.append(point,[1])]).T))
		return n/np.linalg.norm(n)
		
	
