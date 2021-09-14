# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import marshmallow as mm
import numpy as np
import toml
from marshmallow import Schema, fields, pre_load, post_load, validates, ValidationError
from numpy import pi as PI
from scipy.spatial.transform import Rotation as R
from vispy import scene
from vispy.scene.visuals import Arrow, LinePlot

from .component import BaseComponent
from .source import StateofPolarization


class _GenericWavePlateSchema(Schema):
	componentType = fields.Str(data_key="type",
	                           default="Retarder")  # This field will be ignored by the component during instantiation
	name = fields.Str(required=True, error_messages={'required': "Please give an appropriate name for the component"})
	description = fields.Str()
	theta = fields.Float(required=True)
	delta = fields.Float(required=True)
	radians = fields.Bool(default=False)
	lambda0 = fields.Float(default=6563.0)
	lambdaPresent = fields.Float(default=6563.6)
	mueller = fields.List(fields.List(fields.Float()))
	jones = fields.List(fields.List(fields.Float()))
	color = fields.Str(default='blue')
	enabled = fields.Bool(default=True)
	
	class Meta:
		# additional = ["help"]  # List of fields to include in addition to the explicitly defined fields,
		ordered = True  # preserve the order of the schema definition
		unknown = mm.RAISE  # the behavior to take on unknown fields (EXCLUDE, INCLUDE, RAISE)
	
	# Additional validations other than those given in the above Raw definition
	@pre_load
	def validate_angles(self, data, **kwargs):
		if data["radians"]:
			assert 0 < data["theta"] < 2 * np.pi, "Theta not in range: [0, 2π] for " + data["name"]
			assert 0 < data["delta"] < 2 * np.pi, "Delta not in range: [0, 2π] for " + data["name"]
		else:
			assert 0 < data["theta"] < 360, "Theta not in range: [0, 360] for " + data["name"]
			assert 0 < data["delta"] < 360, "Delta not in range: [0, 360] for " + data["name"]
		
		return data
	
	@validates('componentType')
	def validate_type(self, value):
		if value != 'Retarder':
			raise ValidationError("Component is not type: 'Retarder', instead it is: '" + value + "'")
	
	# Action to be taken after loading the schema. Create a component from the schema
	@post_load
	def create_Component(self, data, **kwargs):
		component = Generic_Waveplate(**data)
		return component

########################################################################################################################
class Generic_Waveplate(BaseComponent):
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
		
		if not self.radians:
			self.delta = np.deg2rad(self.delta)
		
		self.lambdaPresent = kwargs.get("lambdaPresent", 6563.0)
		
		self.lambda0 = kwargs.get("lambda0", 6563.0)
		
		self.__wavelength_ratio = self.lambda0 / self.lambdaPresent
		
		self.__calculate_MuellerMatrix()
		self.__calculate_JonesMatrix()
		
		self.parentCanvas = kwargs.get("parentCanvas", None)  # Visual will not be drawn in parent object is not passed
		
		# Set the help string for display in properties box
		self._helpString.update(
			{"delta": "Retardance in degrees. Check radians property to True if you want to enter in radians.",
			 "lambda0": "Reference wavelength in Å at which the retarder has retardance given by 'Delta'. Default is 6563Å",
			 "lambdaPresent": "Current operating wavelength"})
		
		self.retarder_Arrow = None
		self.labelText = None
		self.retarderDirection = np.array([1, 0, 0])
		
		self.position = np.array((1, 0, 0))
		
		self.__create_quaternion(self.delta, self.theta)
		
		if self.parentCanvas is not None:
			self.draw_visual(parentCanvas=self.parentCanvas)
		
		print("----Retarder '%s' created----" % self.name)
	
	def draw_visual(self, parentCanvas):
		
		if self.retarder_Arrow is not None:
			# Delete the existing visuals if they exist
			self.retarder_Arrow = None
			self.labelText = None
			self.retarderDirection = np.array([1, 0, 0])
		
		self.parentCanvas = parentCanvas
		arrowStart = (0, 0, 0)
		arrowDirection = self.position - arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.retarder_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                            arrows=arrowHead,
		                            arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True,
		                            parent=self.parentCanvas.view.scene)
		self.retarder_Arrow.transform = scene.transforms.MatrixTransform()
		self.retarder_Arrow.interactive = True
		
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parentCanvas.view.scene,
		                            pos=self.position + (0.15 * arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		self.labelText.interactive = True
		
		# Rotate the retarder visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * np.rad2deg(self.theta))
	
	def __create_quaternion(self, delta, theta):
		q = R.from_rotvec(2 * theta * np.array((0,0,1))) # theta is automatically converted to radians in the component super class
		self.retarderDirection = q.apply(np.array(self.retarderDirection)) # Update the retarder direction
		self.quaternion = R.from_rotvec(2 * delta * self.retarderDirection) # Create a quaternion from the retardance angle with retarder direction as the axis
	
	def __rotate(self, angle):
		self.retarder_Arrow.transform.rotate(angle, (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle, (0, 0, 1))
	
	def analyse(self, incoming_SoP):
		"""
		Rotates the incoming polarization to outgoing polarization using quaternions and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after retardation
		"""
		# Calculate the result SoP by rotating the vector using quaternion
		result = self.quaternion.apply(incoming_SoP.get_PolarizationVector())
		result_SoP = StateofPolarization(mueller=np.append(np.array([1, ]), result), parent=self.parentCanvas, color=incoming_SoP.get_Color(), name=incoming_SoP.get_Name() + 'x' + self.name)
		
		if self.parentCanvas is not None:
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
		print("SoP=", SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector))
		# print("[1],[2]=", np.dot(SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector)))
		dot = np.dot(SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector))
		if np.abs(dot) < 1.0001:  # Allow for numpy precision in calculations
			dot = np.round(dot, 4)
		arc_StartAngle = np.arccos(dot)
		if SoP_vector[2] < 0:  # If the SoP is in the lower hemisphere,
			arc_StartAngle = 2 * np.pi - arc_StartAngle  # determine the outer angle between the vectors
		
		# Debug Info
		# print("center=",self.retarderDirection, si, center)
		# scene.Text("◊", font_size=70, bold=True, color=self.color, parent=self.parentCanvas.view.scene, pos=center)  # To display the center point
		# Line(np.array([center, arcStart]), connect='strip', method='gl', width=2, color=self.color, parent=self.parentCanvas.view.scene)
		# print("line=", direction_of_intersection)
		# print("Angle=", arcStart, circle_StartVector, SoP_vector, np.rad2deg(arc_StartAngle))#, np.rad2deg(arcAngle))
		
		# Draw arc using quaternion
		# for angle in np.linspace(0, self.delta):
		# 	self.quaternion.apply(incoming_SoP)
		
		# Draw the arc using the above data
		t = np.linspace(arc_StartAngle, arc_StartAngle + (2 * self.delta), 100)
		y = r * np.cos(t)
		z = r * np.sin(t)
		x = np.zeros(y.size)
		arc = LinePlot((x, y, z), width=15, color=self.color, parent=self.parentCanvas.view.scene)
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
		              antialias=True, parent=self.parentCanvas.view.scene)
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
	
	# ---------------------------------------------------------------------------
	def __calculate_MuellerMatrix(self):
		"""
		Private method to calculate the Mueller matrix of the component
		"""
		# print("Waveplate: theta = ", self.theta, "delta = ", self.delta)
		c2 = np.cos(2 * self.theta)
		s2 = np.sin(2 * self.theta)
		
		self.delta_new = self.delta * self.__wavelength_ratio
		
		m22 = (c2 ** 2) + (s2 ** 2 * np.cos(self.delta_new))
		m23 = (c2 * s2) * (1 - np.cos(self.delta_new))
		m24 = -s2 * np.sin(self.delta_new)
		
		m33 = (s2 ** 2) + (c2 ** 2 * np.cos(self.delta_new))
		m34 = c2 * np.sin(self.delta_new)
		
		m44 = np.cos(self.delta_new)
		
		mueller = [[1, 0, 0, 0],
		           [0, m22, m23, m24],
		           [0, m23, m33, m34],
		           [0, -m24, -m34, m44]]
		
		self.mueller = np.array(mueller)
	
	# print("Retarder Mueller", mueller)
	
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
		return self.name + ": " + self.type + " [delta = " + str(self.get_Retardance()) + ", theta = " + str(
			self.get_OrientationAngle()) + ", lambda = " + str(self.lambda0) + "]:\n" + str(
			self.mueller) + "\n--------------\n"
	
	# ---------------------------------------------------------------------------
	def get_Retardance(self, radians=False):
		"""
		Returns the retardance angle δ of the component
		"""
		if radians:
			return self.delta
		return np.rad2deg(self.delta)
	
	# ---------------------------------------------------------------------------
	def set_Retardance(self, delta=0, radians=False):
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
		kwargs["name"] = kwargs.get("name", "HWP")
		if kwargs.get("radians", False):
			kwargs['delta'] = PI
			kwargs["radians"] = True
		else:
			kwargs["delta"] = 180
			kwargs["radians"] = False
		Generic_Waveplate.__init__(self, **kwargs)

########################################################################################################################
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
		kwargs["name"] = kwargs.get("name", "QWP")
		if kwargs.get("radians", False):
			kwargs["delta"] = PI / 2.0
			kwargs["radians"] = True
		else:
			kwargs["delta"] = 90.0
			kwargs["radians"] = False
		Generic_Waveplate.__init__(self, **kwargs)
