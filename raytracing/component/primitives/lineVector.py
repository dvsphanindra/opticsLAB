import numpy as np
from vispy.scene.visuals import Line


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
