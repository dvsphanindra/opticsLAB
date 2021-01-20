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

from vispy import scene

from vispy.scene.visuals import Arrow, LinePlot, GridMesh, Line

from pyquaternion import Quaternion

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
	def get_Name(self):
		return self.name
	
	# ----------------------------------------------------------------------------
	def get_Type(self):
		return self.type
	
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
class StateofPolarization(_Component):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = "Source"
		self.name = kwargs.get("name", "Source_1")
		self.lambdaPresent = kwargs.get("lambdaPresent", 6563.0)
		self.parentVisual = kwargs.get('parent', None)
		
		# Set the help string for display in properties box
		self._helpString.update({"lambdaPresent": "Current operating wavelength", "intensity":"Intensity component of the Stokes Vector", "polarizationVector":"Polarization Vector"})
		
		self.stokes_vector = np.array(kwargs.get("mueller"))
		self.intensity = self.stokes_vector[0]
		self.polarizationVector = self.stokes_vector[1:].flatten()
		
		self.validate_StokesVector()
		
		self.color = kwargs.get("color")
		
		if self.parentVisual is not None:
			self.draw_visual(self.parentVisual)
			
		self.labelObject=None
		self.labelText=None
		
		print("----Source created----")
		
	def draw_visual(self, parentVisual):
		self.parentVisual = parentVisual
		self.labelObject = scene.Text("•", font_size=100, bold=True, color=self.color, parent=self.parentVisual,
		                              pos=self.polarizationVector.transpose())
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parentVisual,
		                            pos=self.polarizationVector.transpose() + (0.15 * self.polarizationVector.transpose()))
		self.labelObject.interactive = True
		self.labelText.interactive = True
		
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
	
	def validate_StokesVector(self):
		squareSum=np.sqrt(np.sum(np.square(self.polarizationVector)))
		if squareSum > self.stokes_vector[0]:
			if squareSum < 1.0001: # Allow for numpy precision in calculations
				self.polarizationVector = np.round(self.polarizationVector,13)
			else:
				raise AssertionError("Irregular Stokes Vector: S0, vector, square, sum of square: {0}, {1}, {2}, {3}".format(self.stokes_vector[0], self.polarizationVector, np.square(self.polarizationVector), np.sum(np.square(self.polarizationVector))))
		
	# ---------------------------------------------------------------------------
	def set_MuellerMatrix(self, mueller):
		# TODO: to verify the conditions for M given in del Toro and only then accept.
		assert np.shape(mueller) == (4, 1), "Invalid Mueller matrix: {}".format(mueller)
		self.mueller = np.array(mueller)
	
	# ---------------------------------------------------------------------------
	def set_JonesMatrix(self, jones):
		assert np.shape(jones) == (2, 1), "Invalid Jones matrix: {}".format(jones)
		self.jones = np.array(jones)
		
	def get_StokesVector(self):
		return self.stokes_vector
		
	def get_PolarizationVector(self):
		return self.polarizationVector
	
	def get_intensity(self):
		return self.intensity
	
	def get_DegreeOfPolarization(self):
		return np.sqrt(np.sum(np.square(self.polarizationVector))) / self.stokes_vector[0]
	
	# def get_ellipticity(self):
	# 	return np.tan(np.pi/4-self.Xi)
	# def get_orientation(self):
	# 	return self.theta
		
########################################################################################################################
class Detector(_Component):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = "Detector"
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
		
		self.parentVisual = kwargs.get("parent", None) # Visual will not be drawn in parent object is not passed
		
		# Set the help string for display in properties box
		self._helpString.update({"delta": "Retardance in degrees. Check radians property to True if you want to enter in radians.",
		                         "lambda0":"Reference wavelength in Å at which the retarder has retardance given by 'Delta'. Default is 6563Å",
		                         "lambdaPresent": "Current operating wavelength"})
		
		self.retarder_Arrow = None
		self.labelText = None
		self.retarderDirection = np.array([1, 0, 0])
		
		self.position = np.array((1, 0, 0))
		
		self.__create_quaternion(self.delta, self.theta)
		
		if self.parentVisual is not None:
			self.draw_visual(parentVisual=self.parentVisual)
		
		print("----Retarder created----")
		
	def draw_visual(self, parentVisual):
		
		if self.retarder_Arrow is not None:
			# Delete the existing visuals if they exist
			self.retarder_Arrow = None
			self.labelText = None
			self.retarderDirection = np.array([1, 0, 0])
			
		self.parentVisual=parentVisual
		arrowStart = (0, 0, 0)
		arrowDirection = self.position - arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.retarder_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                            arrows=arrowHead,
		                            arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True,
		                            parent=self.parentVisual)
		self.retarder_Arrow.transform = scene.transforms.MatrixTransform()
		self.retarder_Arrow.interactive = True
		
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parentVisual,
		                            pos=self.position + (0.15 * arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		self.labelText.interactive = True
		
		
		# Rotate the retarder visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * np.rad2deg(self.theta))
		
	
	def __create_quaternion(self, delta, theta):
		q = Quaternion(axis=(0, 0, 1), radians=2*theta) # Theta is automatically converted to radians in the component super class
		self.retarderDirection = q.rotate(np.array(self.retarderDirection))  # Update the rotation quaternion direction
		
		self.quaternion = Quaternion(axis=self.retarderDirection, degrees=2 * delta)
		
	def __rotate(self, angle):
		self.retarder_Arrow.transform.rotate(angle, (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle, (0, 0, 1))
		
	
	def analyse(self, incoming_SoP):
		"""
		Rotates the incoming polarization to outgoing polarization using quaternions and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after retardation
		"""
		result = self.quaternion.rotate(incoming_SoP.get_PolarizationVector())  # Calculate the result SoP by rotating the vector using quaternion
		result_SoP = StateofPolarization(mueller=np.append(np.array([1, ]), result), parent=self.parentVisual, color=incoming_SoP.get_Color(),
		                 name=incoming_SoP.get_Name() + 'x' + self.name)
		
		if self.parentVisual is not None:
			self.__draw_retarderEffect(incoming_SoP)
		
		return result_SoP
	
	def __draw_retarderEffect(self, incoming_SoP):
		# Find the plane which is normal to the retardance vector and also in which the input SoP lies. Result SoP also lies in the same plane
		# https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
		dotProduct = np.dot(self.retarderDirection, self.retarderDirection)
		
		w = np.array((0, 0, 0))  # Line start point
		si = np.dot(self.retarderDirection, incoming_SoP.get_PolarizationVector()) / dotProduct
		center = w + si * self.retarderDirection  # Find the center of rotation which is located on this plane
		
		# To draw the arc of rotation of the retarder
		r = np.sqrt(np.sum((center - incoming_SoP.get_PolarizationVector()) ** 2))  # Radius is the distance from center to the incoming SoP
		
		# Find the line of intersection of the plane (Normal: retarder direction vector) and the XY plane (Normal: z-axis)
		# https://en.wikipedia.org/wiki/Intersection_curve#Intersection_line_of_two_planes
		direction_of_intersection = np.cross(self.retarderDirection, np.array((0, 0, 1)))
		arcStart = center + (-r) * direction_of_intersection  # Find the point towards the right side of the center (-r)
		circle_StartVector = arcStart - center
		
		# Find the SoP Vector to determine the starting angle of the arc
		SoP_vector = incoming_SoP.get_PolarizationVector() - center
		print("SoP=",SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector))
		# print("[1],[2]=", np.dot(SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector)))
		dot = np.dot(SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector))
		if np.abs(dot) < 1.0001: # Allow for numpy precision in calculations
			dot=np.round(dot,4)
		arc_StartAngle = np.arccos(dot)
		if SoP_vector[2] < 0:  # If the SoP is in the lower hemisphere,
			arc_StartAngle = 2 * np.pi - arc_StartAngle  # determine the outer angle between the vectors
		
		# Debug Info
		# print("center=",self.retarderDirection, si, center)
		# scene.Text("◊", font_size=70, bold=True, color=self.color, parent=self.parentVisual, pos=center)  # To display the center point
		# Line(np.array([center, arcStart]), connect='strip', method='gl', width=2, color=self.color, parent=self.parentVisual)
		# print("line=", direction_of_intersection)
		# print("Angle=", arcStart, circle_StartVector, SoP_vector, np.rad2deg(arc_StartAngle))#, np.rad2deg(arcAngle))
		
		# Draw arc using quaternion
		# for angle in np.linspace(0, self.delta):
		# 	self.quaternion.rotate(incoming_SoP)
		
		# Draw the arc using the above data
		t = np.linspace(arc_StartAngle, arc_StartAngle + np.deg2rad(2 * self.delta), 100)
		y = r * np.cos(t)
		z = r * np.sin(t)
		x = np.zeros(y.size)
		arc = LinePlot((x, y, z), width=15, color=self.color, parent=self.parentVisual)
		arc.transform = scene.transforms.MatrixTransform()
		arc.transform.rotate(2 * np.rad2deg(self.theta), (0, 0, 1))
		arc.transform.translate(center)
		
		# Draw arrow head at the center (51st point) of the above arc to indicate the direction of rotation
		arrowHead = np.array([(x[50], y[50], z[50], x[51], y[51],
		                       z[51])])  # Arrow direction, position -Direction determined by the 50th point
		
		arrowSize = 5. if r > 0.2 else 3.
		# The pos parameter is simply a line of short length same as that of the arrowhead
		arrow = Arrow(pos=np.array([(x[50], y[50], z[50]), (x[51], y[51], z[51])]), color=self.color, method='gl',
		              width=arrowSize, arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color,
		              antialias=True, parent=self.parentVisual)
		arrow.transform = scene.transforms.MatrixTransform()
		arrow.transform.rotate(2 * np.rad2deg(self.theta), (0, 0, 1))
		arrow.transform.translate(center)
	
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
		
	# ---------------------------------------------------------------------------
	def set_OperatingWavelength(self, lambdaPresent):
		self.lambdaPresent = lambdaPresent
		self.__wavelength_ratio = self.lambda0 / self.lambdaPresent
		self.__calculate_MuellerMatrix()
		# self.__calculate_JonesMatrix()
		
		self.draw_visual()
		
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
		self.parentVisual = kwargs.get("parent", None)
		
		self.polariserDirection = np.array([1, 0, 0])
		
		self.position = np.array((1, 0, 0))
		
		print("----Polariser created----")
		
		if self.parentVisual is not None:
			self.draw_visual(self.parentVisual)

		
		
	def draw_visual(self, parentVisual):
		self.parentVisual = parentVisual
		self.arrowStart = (0, 0, 0)
		self.arrowDirection = self.position - self.arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.polariser_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                             arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color,
		                             antialias=True, parent=self.parentVisual)
		self.polariser_Arrow.transform = scene.transforms.MatrixTransform()
		self.polariser_Arrow.interactive = True
		
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parentVisual,
		                            pos=self.position + (0.15 * self.arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		self.labelText.interactive = True
		
		
		# Rotate the polariser visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * np.rad2deg(self.theta))
	
	def __rotate(self, angle):
		self.polariser_Arrow.transform.rotate(angle, (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle, (0, 0, 1))
		q = Quaternion(axis=(0, 0, 1), degrees=angle)
		self.polariserDirection = q.rotate(np.array(self.polariserDirection))  # Update the rotation quaternion direction
	
	def analyse(self, incoming_SoP):
		"""
		Polarises the incoming polarization to outgoing polarization and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after polarisation
		"""
		# gamma is the angle between the orientation of the polariser and orientation of the incoming SoP
		gamma = np.arccos(np.dot(self.polariserDirection, incoming_SoP.get_PolarizationVector()))
		two_psi = np.arctan(self.polariserDirection[1] / self.polariserDirection[0])
		if np.abs(self.theta) > 45:
			two_psi += np.pi
		I = np.cos(gamma / 2) ** 2
		# From the basic relations for S0, S1, S2, S3 given in https://en.wikipedia.org/wiki/Stokes_parameters
		# DoP=1, two_Xi=0, the relations simplify
		result_polarization_vector = np.array((I * np.cos(two_psi), I * np.sin(two_psi), 0))
		result_SoP = StateofPolarization(mueller=np.append([I], result_polarization_vector), parent=self.parentVisual, color=incoming_SoP.get_Color(),
		                 name=incoming_SoP.get_Name() + '+' + self.name)
		# print("In Polariser: gamma, 2Psi, result=",np.rad2deg([gamma, two_psi]), result_polarization_vector)
		
		if self.parentVisual is not None:
			self.__draw_polariserEffect(incoming_SoP, result_polarization_vector)
		
		return result_SoP
	
	def __draw_polariserEffect(self, incoming_SoP, result_polarization_vector):
		""" Draw the transformation visual """
		# Calculate mid point for drawing the arrow head
		mid_point = (incoming_SoP.get_PolarizationVector() + result_polarization_vector) / 2
		arrowHead = np.array([np.append(incoming_SoP.get_PolarizationVector(), mid_point)])  # Arrow direction, position
		
		Arrow(pos=np.array([incoming_SoP.get_PolarizationVector(), result_polarization_vector]), color=self.color,
		      method='gl', width=5., arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0,
		      arrow_color=self.color, antialias=True, parent=self.parentVisual)
	
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

