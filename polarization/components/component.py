# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import numpy as np

class BaseComponent:
	"""
	Base class for many of the components. The methods and attributes may be overridden by the child classes
	"""
	
	def __init__(self, **kwargs):
		# Define the parameters initially so that they are displayed in the same order of definition in the properties box
		self.type = "Component"  # Compulsory to be overridden by the child class to its own type
		self.name = kwargs.get("name", "ComponentName")
		self.description = kwargs.get("description")
		
		self.theta = 0.0
		self.radians = False
		# self.lambdaPresent = 6563.0
		
		self.mueller = []  # Mueller matrix
		self.jones = []  # Jones matrix
		self._readOnlyParameters = ['type']  # List of Parameters user cannot change but displayed in the properties
		self.color = kwargs.get("color", "blue")  # set to default color of Blue if not defined
		
		self.radians = kwargs.get("radians", False)  # Set to False if not defined
		
		self.__component_schema = None  # Create the corresponding child class schema for loading and validation
		
		# if kwargs.get("mueller") is not None:
		# 	self.set_MuellerMatrix(kwargs["mueller"])
		# 	self.__convert_Mueller2Jones()
		# 	self.add_ReadOnlyParameters(['theta', 'radians', 'jones'])
		# 	self.__calculate_thetaDelta_from_Mueller(self.mueller)
		# elif kwargs.get("jones") is not None:
		# 	self.set_JonesMatrix(kwargs["jones"])
		# 	self.__convert_Jones2Mueller()
		# 	self.add_ReadOnlyParameters(['mueller', 'theta', 'radians'])
		# 	self.__calculate_thetaDelta_from_Jones(self.jones)
		# else:
		if True:
			self.theta = float(kwargs.get("theta", 0.0))  # Set to default value of zero if not defined
			self.add_ReadOnlyParameters(['mueller', 'jones'])
			
			if not self.radians:
				self.theta = np.deg2rad(self.theta)
			self.__calculate_JonesMatrix()
			self.__calculate_MuellerMatrix()
		
		# Set the help string for display in properties box
		self._helpString = {"type": "Type of the component", "name": "Name of the component for reference (optional)",
		                    "description": "User notes for the component (optional)",
		                    "radians": "Select if 'delta' and 'theta' are in radians",
		                    "theta": "Orientation of the retarder in degrees. Check radians property to True if you want to enter in radians.",
		                    "mueller": "Mueller matrix of the component", "jones": "Jones matrix of the component",
		                    "color": "Color used for representation in the GUI",
		                    "enabled": "Whether the component should be included for calculations. Included if True."}
	
	# ---------------------------------------------------------------------------
	# NOTE: @staticmethod create_from_schema() will not be implemented by the baseclass
	
	# ---------------------------------------------------------------------------
	def __calculate_MuellerMatrix(self):
		"""
		Private method to calculate the Mueller matrix of the component. To be implemented by the child class
		"""
		# print("Mueller Matrix calculation in parent class")
		pass
	
	# ---------------------------------------------------------------------------
	def __calculate_JonesMatrix(self):
		"""
		Private Method to calculate Jones matrix of the retarder from the theta and delta values. To be implemented by the child class
		:return:
		"""
		# print("Jones Matrix calculation in parent class")
		pass
	
	# ---------------------------------------------------------------------------
	def __convert_Mueller2Jones(self):
		"""
		Private method to calculate Mueller matrix from Jones matrix. To be implemented by the child class
		:return:
		"""
		pass
	
	# ---------------------------------------------------------------------------
	def __convert_Jones2Mueller(self):
		"""
		Private method to calculate Jones matrix from Jones matrix. To be implemented by the child class
		:return:
		"""
		pass
	
	# ---------------------------------------------------------------------------
	def __calculate_thetaDelta_from_Mueller(self, mueller):
		pass
	
	# ---------------------------------------------------------------------------
	def __calculate_thetaDelta_from_Jones(self, jones):
		pass
	
	# ---------------------------------------------------------------------------
	def print_MuellerMatrix(self):
		"""
		Prints the Mueller matrix of the component
		"""
		np.set_printoptions(precision=4, suppress=True)
		print(self.mueller)
	
	# ---------------------------------------------------------------------------
	def __str__(self):
		pass
	
	# ---------------------------------------------------------------------------
	def __mul__(self, other):
		from .waveplates import Generic_Waveplate # import here to avoid circular import problems
		return Generic_Waveplate(name="Result Component", mueller=self.mueller * other.mueller)
	
	# ---------------------------------------------------------------------------
	def __rmul__(self, other):
		if other == 0:
			return self
		else:
			return self.__mul__(other)
	
	# ---------------------------------------------------------------------------
	def get_Type(self):
		"""
		Returns the type of the component
		"""
		return self.type
	
	# ---------------------------------------------------------------------------
	def get_OrientationAngle(self, radians=False):
		"""
		Returns the angle with respect to the optical axis θ of the component
		"""
		if radians:
			return self.theta
		return np.rad2deg(self.theta)
	
	# ---------------------------------------------------------------------------
	def get_Name(self):
		"""
		Returns the name of the optical component
		"""
		return self.name
	
	# ----------------------------------------------------------------------------
	def get_Color(self):
		"""
		To return the color
		:return: Returns the colour of the optical component
		"""
		return self.color
	
	# ---------------------------------------------------------------------------
	def get_Description(self):
		"""

		:return:
		"""
		return self.description
	
	# ---------------------------------------------------------------------------
	def set_Type(self, componentType):
		"""
		Private method to set the type of the component
		"""
		# TODO: Check whether this method is required or not
		self.type = componentType
	
	# ---------------------------------------------------------------------------
	def set_Name(self, name):
		"""

		:param name:
		:return:
		"""
		self.name = name
	
	# ----------------------------------------------------------------------------
	def set_Description(self, description):
		"""

		:param description:
		:return:
		"""
		self.description = description
	
	# ---------------------------------------------------------------------------
	def set_OrientationAngle(self, theta=0.0, radians=False):
		"""
		Sets the angle with respect to the optical axis θ of the component
		radians: Default is degrees. Set it True to indicate the angles are in radians
		"""
		if not radians:
			self.theta = np.deg2rad(theta)
		else:
			self.theta = float(theta)
		self.__calculate_MuellerMatrix()
		self.__calculate_JonesMatrix()
	
	# ---------------------------------------------------------------------------
	def set_MuellerMatrix(self, mueller):
		pass
	
	# ---------------------------------------------------------------------------
	def set_JonesMatrix(self, jones):
		pass
	
	# ---------------------------------------------------------------------------
	def get_MuellerMatrix(self):
		return self.mueller
	
	# ---------------------------------------------------------------------------
	def get_JonesMatrix(self):
		return self.jones
	
	# ----------------------------------------------------------------------------
	def get_HelpString(self, parameter):
		return self._helpString[parameter]
	
	# ----------------------------------------------------------------------------
	def get_isReadOnlyParameter(self, parameter):
		return parameter in self._readOnlyParameters
	
	# ----------------------------------------------------------------------------
	def add_ReadOnlyParameters(self, parameters):
		if type(parameters) == list:
			self._readOnlyParameters += parameters
		else:
			self._readOnlyParameters.append(parameters)
