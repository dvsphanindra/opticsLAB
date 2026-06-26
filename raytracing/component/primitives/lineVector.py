import numpy as np
from vispy.scene.visuals import Line
from .miscellaneous import deg2DC
from .primitive_point import Primitive_point

class LineVector:
	def __init__(self, start, direction, name=None, dc=False, length=1, color='Blue', parentCanvas=None):
		"""
		Creates a line or line segment object for rendering
		:param: start: Starting point of the line. Can be a Point object or numpy array.
		:param: direction: Direction of the line with respect to the openPyOpticalBench coordinates. Can be specified as angles in degrees or as direction cosines
		:param: name: Name of the line for debugging purposes (optional)
		:param: dc: If the direction is specified as dc (True) or angles (False). Default: False
		:param length: Length of the line segment (Optional). Default: Unit length
		:param color: Color to be shown when the line is being visualized (Optional). Default='Blue'
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		"""
		# self.lineStart_point = start.get_coordinates() if isinstance(start, Primitive_point) else np.array(start)
		
		self.length = length
		self.color = color
		self.lineEnd = None
		self.vector = None
		self.lineVisual = None
		self.parentCanvas = parentCanvas
		
		# print(isinstance(start, Point))
		# if isinstance(start, Point):
		# 	self.lineStart_point = start
		# 	self.lineStart_coordinates = start.get_coordinates()
		# else:
		self.lineStart_coordinates = np.array(start)
		self.lineStart_point = start# Point(start, parentCanvas=self.parentCanvas)

		self.name=name
		
		if not dc:
			self.direction = deg2DC(direction)
		else:
			self.direction = np.array(direction)
		# TODO: assert
		# assert self.direction-1 < 1, "No: {0}, {1}, {2}".format(self.direction[0]-1, self.direction[1]-1, self.direction[2]-1)
		
		self.create_Vector()
	
	def create_Vector(self):
		#print(self.lineStart_point, self.length * self.direction)
		# Check for is instance Point
		# if not "Point" in self.lineStart_point.__str__():
		# self.lineEnd = Point(self.lineStart_point.get_coordinates() + self.length * self.direction)
		# self.vector = self.lineEnd.get_coordinates() - self.lineStart_point.get_coordinates()
		
		self.lineEnd = self.lineStart_point + self.length * self.direction
		self.vector = self.lineEnd - self.lineStart_point
		
		# Create line Visual passing through two points
		parent=None if self.parentCanvas is None else self.parentCanvas.view.scene
		self.lineVisual = Line(np.array([self.lineStart_point, self.lineEnd]), connect='strip', method='gl', width=2,
							   color=self.color, parent=parent)
	
	def update_Vector(self, endPoint):
		if not np.array_equal(self.lineEnd, endPoint):  # Do not update if there is no change
			self.lineEnd = endPoint
			self.vector = self.lineEnd - self.lineStart_point
			self.length = np.linalg.norm(self.vector)
			
			self.lineVisual.parent=None # Remove the old visual
			# Create line Visual passing through two points
			parent = None if self.parentCanvas is None else self.parentCanvas.view.scene
			self.lineVisual = Line(np.array([self.lineStart_point, self.lineEnd]), connect='strip', method='gl', width=2,
								   color=self.color, parent=parent)
	
	def extend_Vector(self, length):
		if self.length != length:  # Do not update if there is no change
			self.length = length
			self.create_Vector()
	
	def get_Direction_Cosines(self):
		direction_ratios = self.lineEnd - self.lineStart_point
		direction_cosines = direction_ratios / np.linalg.norm(direction_ratios)
		return direction_cosines
	
	def get_Direction_Angles(self):
		direction_ratios = self.lineEnd - self.lineStart_point
		direction_angles = np.rad2deg(np.arccos(direction_ratios / np.linalg.norm(direction_ratios)))
		return direction_angles
	
	def get_visual(self):
		return self.lineVisual
	
	def translate(self, point):
		"""
		Translate the vector to a new origin without changing the length
		:param point: Starting Point to which the vector should be shifted
		"""
		if not np.array_equal(self.lineStart_point, point):  # Do not update if there is no change
			self.lineStart_point = point
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
