# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import numpy as np
from numpy import cos, sin
from numpy import pi as PI

import toml

from component_schema import _ProjectSchema, _GenericWavePlateSchema, _LinearPolariserSchema, _DetectorSchema, _SourceSchema, _ComponentSchema

import marshmallow as mm

####################################################################################################
class Project:
	"""
	Project class
	"""
	
	def __init__(self, **kwargs):
		self.type = "Project"
		self.name = kwargs.get("name", "Project_1")
		self.description = kwargs.get("description")
		self.created = kwargs.get("created")
		self.modified = kwargs.get("modified")
		self._componentsList = kwargs.get("componentsList")
		
		self._readOnlyParameters = ['type', 'created', 'modified']
		# Set the help string for display in properties box
		self._helpString = {"type": "Type of the component", "name": "Name of the Project for reference",
		                    "description": "Description of the Project",
		                    "created": "Date on which the project was created",
		                    "modified": "Date on which the project was modified last"}
	
	@staticmethod
	def create_from_schema(schema):
		project_data = toml.load(schema)
		project_schema = _ProjectSchema(many=False, unknown=mm.EXCLUDE)
		project = project_schema.load(project_data)
		return project
	
	@staticmethod
	def validate(instance):
		component_schema = _ProjectSchema(many=False, unknown=mm.EXCLUDE)
		print(component_schema.validate(instance))
	
	# ----------------------------------------------------------------------------
	def get_HelpString(self, parameter):
		return self._helpString[parameter]
		
	# ----------------------------------------------------------------------------
	def get_isReadOnlyParameter(self, parameter):
		return parameter in self._readOnlyParameters


###########################################################################################################3
class _Component:
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
		self.color = kwargs.get("color", "Blue")  # set to default color of Blue if not defined
		
		self.radians = kwargs.get("radians", False)  # Set to False if not defined
		
		self.__component_schema = None  # Create the corresponding child class schema for loading and validation
		
		if kwargs.get("mueller") is not None:
			self.set_MuellerMatrix(kwargs["mueller"])
			self.__convert_Mueller2Jones()
			self.add_ReadOnlyParameters(['theta', 'radians', 'jones'])
			self.__calculatethetaDelta_from_Mueller(self.mueller)
		elif kwargs.get("jones") is not None:
			self.set_JonesMatrix(kwargs["jones"])
			self.__convert_Jones2Mueller()
			self.add_ReadOnlyParameters(['mueller', 'theta', 'radians'])
			self.__calculatethetaDelta_from_Jones(self.jones)
		else:
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
		pass
	
	# ---------------------------------------------------------------------------
	def __calculate_JonesMatrix(self):
		"""
		Private Method to calculate Jones matrix of the retarder from the theta and delta values. To be implemented by the child class
		:return:
		"""
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
	def __calculatethetaDelta_from_Mueller(self, mueller):
		pass
	
	# ---------------------------------------------------------------------------
	def __calculatethetaDelta_from_Jones(self, jones):
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
	def get_OrientationAngle(self):
		"""
		Returns the angle with respect to the optical axis θ of the component
		"""
		return np.rad2deg(self.theta)
	
	# ---------------------------------------------------------------------------
	def get_Name(self):
		"""
		Returns the name of the optical component
		"""
		return self.name
	
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
	def set_OperatingWavelength(self, lambdaPresent):
		self.lambdaPresent = lambdaPresent
	
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

########################################################################################################################
class Source(_Component):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = "Source"
		self.name = kwargs.get("name", "Source_1")
		self.lambdaPresent = kwargs.get("lambdaPresent", 6563.0)
		
		# Set the help string for display in properties box
		self._helpString.update({"lambdaPresent": "Current operating wavelength"})
		
		print("----Source created----")
	
	@staticmethod
	def create_from_schema(schema):
		component_template = toml.load(schema)
		component_data = component_template["component"]
		component_schema = _SourceSchema(many=False, unknown=mm.EXCLUDE)
		component = component_schema.load(component_data)
		return component
	
	@staticmethod
	def validate(instance):
		component_schema = _SourceSchema(many=False, unknown=mm.EXCLUDE)
		print(component_schema.validate(instance))
		
	# ---------------------------------------------------------------------------
	def set_MuellerMatrix(self, mueller):
		# TODO: to verify the conditions for M given in del Toro and only then accept.
		assert np.shape(mueller) == (4, 1), "Invalid Mueller matrix: {}".format(mueller)
		self.mueller = np.array(mueller)
	
	# ---------------------------------------------------------------------------
	def set_JonesMatrix(self, jones):
		assert np.shape(jones) == (2, 1), "Invalid Jones matrix: {}".format(jones)
		self.jones = np.array(jones)
		
########################################################################################################################
class Detector(_Component):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = "Source"
		self.name = kwargs.get("name", "Detector_1")
		
		print("----Detector created----")
	
	@staticmethod
	def create_from_schema(schema):
		component_template = toml.load(schema)
		component_data = component_template["component"]
		component_schema = _DetectorSchema(many=False, unknown=mm.EXCLUDE)
		component = component_schema.load(component_data)
		return component
	
	@staticmethod
	def validate(instance):
		component_schema = _DetectorSchema(many=False, unknown=mm.EXCLUDE)
		print(component_schema.validate(instance))
	
	# ---------------------------------------------------------------------------
	def set_MuellerMatrix(self, mueller):
		# TODO: to verify the conditions for M given in del Toro and only then accept.
		assert np.shape(mueller) == (4, 1), "Invalid Mueller matrix: {}".format(mueller)
		self.mueller = np.array(mueller)
	
	# ---------------------------------------------------------------------------
	def set_JonesMatrix(self, jones):
		assert np.shape(jones) == (2, 1), "Invalid Jones matrix: {}".format(jones)
		self.jones = np.array(jones)

########################################################################################################################
class Generic_Waveplate(_Component):
	"""
	Creates a retarder depending on the value of retardance whose retardance also varies with the wavelength.
	
	Arguments:
	
	:name : Specify the name of the component (String)
	
	:delta : The retardance angle 'δ'. (Default degrees)
	For Quarter wave plate, enter δ = 90˚
	Half wave plate, enter δ = 180˚
	
	:theta : Angle between fast axis to optical axis 'θ' (Default degrees)
	
	:lambda0 : operating wavelength in Angstroms. Default is 6563.0 Angstroms
	
	:radians: Default is degrees. Set it True to indicate the angles are in radians
	
	Refer delToro Iniesta Eq 4.47, 4.49, Chapter 4, Page 52, 53
	"""
	def __init__(self, **kwargs):
		# Define the parameters initially so that they are displayed in the same order of definition in the properties box
		super().__init__(**kwargs)
		self.type = "Retarder"
		
		self.delta = kwargs.get("delta", 0.0)
		
		self.lambdaPresent = kwargs.get("lambdaPresent", 6563.0)
		
		self.lambda0 = kwargs.get("lambda0", 6563.0)
		
		self.__wavelength_ratio = self.lambda0 / self.lambdaPresent
		
		# Set the help string for display in properties box
		self._helpString.update({"delta": "Retardance in degrees. Check radians property to True if you want to enter in radians.",
		                         "lambda0":"Reference wavelength in Å at which the retarder has retardance given by 'Delta'. Default is 6563Å",
		                         "lambdaPresent": "Current operating wavelength"})
		
		print("----Retarder created----")
	
	@staticmethod
	def create_from_schema(schema):
		component_template = toml.load(schema)
		component_data = component_template["component"]
		component_schema = _GenericWavePlateSchema(many=False, unknown=mm.EXCLUDE)
		component = component_schema.load(component_data)
		return component
	
	@staticmethod
	def validate(instance):
		component_schema = _GenericWavePlateSchema(many=False, unknown=mm.EXCLUDE)
		print(component_schema.validate(instance))
		
	#---------------------------------------------------------------------------
	def __calculate_MuellerMatrix(self):
		"""
		Private method to calculate the Mueller matrix of the component
		"""
		
		c2 = cos(2*self.theta)
		s2 = sin(2*self.theta)
		
		self.delta_new = self.delta * self.__wavelength_ratio
		
		m22 = (c2**2) + (s2**2 * cos(self.delta_new))
		m23 = (c2 * s2) * (1 - cos(self.delta_new))
		m24 = -s2 * sin(self.delta_new)
		
		m33 = (s2**2) + (c2**2 * cos(self.delta_new))
		m34 = c2 * sin(self.delta_new)
		
		m44 = cos(self.delta_new)
		
		mueller = [	[	1,		0,		0,		0	],
				[	0,		m22,	m23,	m24],
				[	0,		m23,	m33,	m34],
				[	0,		-m24,	-m34,	m44]]
		
		self.mueller = np.array(mueller)
	
	#---------------------------------------------------------------------------
	def __calculate_JonesMatrix(self):
		"""
		Private Method to calculate Jones matrix of the retarder from the theta and delta values
		:return:
		"""
		pass
	
	#---------------------------------------------------------------------------
	def __str__(self):
		np.set_printoptions(precision=4, suppress=True)
		return  self.name + ": " + self.type + " [delta = " + str(self.get_Retardance()) + ", theta = "+ str(self.get_OrientationAngle()) + ", lambda = " + str(self.lambda0) + "]:\n"+ str(self.mueller) + "\n--------------\n"

	#---------------------------------------------------------------------------
	def set_Retardance(self):
		"""
		Returns the retardance angle δ of the component
		"""
		return np.rad2deg(self.delta)
	
	#---------------------------------------------------------------------------
	def get_Retardance(self, delta = 0, radians = False):
		"""
		Sets the retardance angle δ of the component.
		radians: Default is degrees. Set it True to indicate the angles are in radians
		"""
		if not radians:
			self.delta = np.deg2rad(delta)
		else:
			self.delta = float(delta)
		self.__calculate_MuellerMatrix()
		
	# ---------------------------------------------------------------------------
	def set_MuellerMatrix(self, mueller):
		# TODO: to verify the conditions for M given in del Toro and only then accept.
		assert np.shape(mueller) == (4, 4), "Invalid Mueller matrix: {}".format(mueller)
		self.mueller = np.array(mueller)
	
	# ---------------------------------------------------------------------------
	def set_JonesMatrix(self, jones):
		assert np.shape(jones) == (2, 2), "Invalid Jones matrix: {}".format(jones)
		self.jones = np.array(jones)
		
###############################################################################
class Linear_Polariser(_Component):
	"""
	Creates a linear polariser with the specified orientation angle

	Arguments:

	:name : Specify the name of the component (String)

	:theta : Orientation angle of the polariser 'θ' (Default degrees)

	:radians: Default is degrees. Set it True to indicate the angles are in radians

	Refer delToro Iniesta Eq 4.47, 4.49, Chapter 4, Page 52, 53
	"""
	def __init__(self, **kwargs):
		# Define the parameters initially so that they are displayed in the same order of definition in the properties box
		super().__init__(**kwargs)
		self.type = "Polariser"
		self.name = kwargs.get("name", "PolariserName")
		self.description = kwargs.get("description")
		
		print("----Polariser created----")
	
	@staticmethod
	def create_from_schema(schema):
		component_template = toml.load(schema)
		component_data = component_template["component"]
		component_schema = _LinearPolariserSchema(many=False, unknown=mm.EXCLUDE)
		component = component_schema.load(component_data)
		return component
	
	@staticmethod
	def validate(instance):
		component_schema = _LinearPolariserSchema(many=False, unknown=mm.EXCLUDE)
		print(component_schema.validate(instance))
		
	# ---------------------------------------------------------------------------
	def set_MuellerMatrix(self, mueller):
		# TODO: to verify the conditions for M given in del Toro and only then accept.
		assert np.shape(mueller) == (4, 4), "Invalid Mueller matrix: {}".format(mueller)
		self.mueller = np.array(mueller)
	
	# ---------------------------------------------------------------------------
	def set_JonesMatrix(self, jones):
		assert np.shape(jones) == (2, 2), "Invalid Jones matrix: {}".format(jones)
		self.jones = np.array(jones)
	
	# ---------------------------------------------------------------------------
	def __calculate_MuellerMatrix(self):
		"""
		Private method to calculate the Mueller matrix of the component
		"""
		self.__set_Type()
		
		c2 = cos(2 * self.theta)
		s2 = sin(2 * self.theta)
		
		mueller = [[1, c2, s2, 0],
		     [c2, c2 ** 2, c2 * s2, 0],
		     [s2, c2 * s2, s2 ** 2, 0],
		     [0, 0, 0, 0]]
		
		self.mueller = 0.5 * np.array(mueller)
		
	# ---------------------------------------------------------------------------
	def __calculate_JonesMatrix(self):
		"""
		Private Method to calculate Jones matrix of the retarder from the theta and delta values
		:return:
		"""
		pass
	
	# ---------------------------------------------------------------------------
	def __str__(self):
		np.set_printoptions(precision=4, suppress=True)
		return self.name + ": " + self.type + ", theta = " + str(self.get_OrientationAngle())  + "]:\n" + str(self.mueller) + "\n--------------\n"
			
###############################################################################
class Quarter_Waveplate(Generic_Waveplate):
	"""
	Creates a Quarter Wave Plate and initializes its Mueller matrix
	
	Arguments:
	
	name : Specify the name of the component (String)
	
	theta : Angle between fast axis to optical axis 'θ' (Default degrees)
	
	radians: Default is degrees. Set it True to indicate the angles are in radians
	
	Refer delToro Iniesta Eq 4.47, 4.49, Chapter 4, Page 52, 53
	"""
	def __init__(self, **kwargs):
		kwargs["name"] = "Default QWP"
		if kwargs.get("radians") is True:
			kwargs["delta"] = PI/2
		else:
			kwargs["delta"]= 90.0
		Generic_Waveplate.__init__(self, **kwargs)

###############################################################################
class Half_Waveplate(Generic_Waveplate):
	"""
	Creates a Half Wave Plate and initializes its Mueller matrix 
	
	Arguments:
	
	name : Specify the name of the component (String)
	
	theta : Angle between fast axis to optical axis 'θ' (Default degrees)
	
	radians: Default is degrees. Set it True to indicate the angles are in radians
	
	Refer delToro Iniesta Eq 4.47, 4.49, Chapter 4, Page 52, 53
	"""
	
	def __init__(self, **kwargs):
		kwargs["name"] = "Default HWP"
		if kwargs.get("radians") is True:
			kwargs['delta'] = PI
		else:
			kwargs["delta"] = 180
		Generic_Waveplate.__init__(self, **kwargs)

###############################################################################
if __name__ == "__main__":
	C1 = Generic_Waveplate(name="Component_1", delta=180, theta=0)
	C2 = Generic_Waveplate.create_from_schema(schema="./templates/retarder.template.toml")
	C3 = Quarter_Waveplate(theta=np.deg2rad(30), radians=True)
	C4 = Half_Waveplate(theta=30)
	P1 = Linear_Polariser(name="Polariser_1", theta=30)
	P2 = Linear_Polariser.create_from_schema("./templates/polariser.template.toml")
	
	print(C1)
	print(C2)
	print(vars(C2))
	print(C3)
	print(C4)
	C5 = C2 * C1
	print(C5)
	print(P1)
	print(P2)

