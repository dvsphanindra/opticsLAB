import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot
from scipy.spatial.transform import Rotation

from component.primitives.lineVector import LineVector


class Surface:
	def __init__(self, center, x_grid, y_grid, z_grid, xTilt=0.0, yTilt=0.0, color="black"):
		"""
		Creates a plane surface with the given center and normal with the specified media
		:param center: Center of the plane with respect to the pyOptiCAD coordinates
		:param xTilt: tilt of the plane with respect to pyOptiCAD X axis
		:param yTilt: tilt of the plane with respect to pyOptiCAD Y axis
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
		# transformedPoint = np.array(self.__rotationMatrix.apply(point) + self.__translationMatrix)
		transformedPoint = np.array(point+self.__translationMatrix)
		# print("translated Point: ",point)
		return transformedPoint
	
	def inverse_transform(self, point):
		# rotation = self.__rotationMatrix.inv()
		transformedPoint = np.array(self.__rotationMatrix.apply(point, inverse=True) - self.__translationMatrix)
		return transformedPoint
