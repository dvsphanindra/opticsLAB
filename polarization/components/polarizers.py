# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import marshmallow as mm
import numpy as np
import toml
from marshmallow import Schema, fields, pre_load, post_load, validates, ValidationError
from scipy.spatial.transform import Rotation as R
from vispy import scene
from vispy.scene.visuals import Arrow

from .component import BaseComponent
from .source import StateofPolarization


class _LinearPolariserSchema(Schema):
	componentType = fields.Str(data_key="type",
	                           default="Polariser")  # This field will be ignored by the component during instantiation
	name = fields.Str(required=True, error_messages={'required': "Please give an appropriate name for the component"})
	description = fields.Str()
	theta = fields.Float(required=True)
	radians = fields.Bool(default=False)
	mueller = fields.List(fields.List(fields.Float()))
	jones = fields.List(fields.List(fields.Float()))
	color = fields.Str(default='blue')
	enabled = fields.Bool(default=True)
	
	class Meta:
		# additional = ["help"]  # List of fields to include in addition to the explicitly defined fields,
		ordered = True  # preserve the order of the schema definition
		unknown = mm.RAISE  # the behavior to take on unknown fields (EXCLUDE, INCLUDE, RAISE)
	
	# Additional validations other than those given above Raw definition
	@pre_load
	def validate_angles(self, data, **kwargs):
		if data["radians"]:
			assert 0 < data["theta"] < 2 * np.pi, "Theta not in range: [0, 2π] for " + data["name"]
		else:
			assert 0 < data["theta"] < 360, "Theta not in range: [0, 360] for " + data["name"]
		return data
	
	@validates('componentType')
	def validate_type(self, value):
		if value != 'Polariser':
			raise ValidationError("Component is not type: 'Polariser', instead it is: '" + value + "'")
	
	# Action to be taken after loading the schema. Create a component from the schema
	@post_load
	def create_Component(self, data, **kwargs):
		component = Linear_Polariser(**data)
		return component


###############################################################################
class Linear_Polariser(BaseComponent):
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
		
		self.__calculate_MuellerMatrix()
		self.__calculate_JonesMatrix()
		
		self.parentCanvas = kwargs.get("parentCanvas", None)  # Visual will not be drawn in parent object is not passed
		
		self.polariserDirection = np.array([1, 0, 0])
		
		self.position = np.array((1, 0, 0))
		
		print("----Polariser '%s' created----" % self.name)
		
		self.__create_quaternion(self.theta)
		
		if self.parentCanvas is not None:
			self.draw_visual(self.parentCanvas)
	
	def draw_visual(self, parentCanvas):
		self.parentCanvas = parentCanvas
		self.arrowStart = (0, 0, 0)
		self.arrowDirection = self.position - self.arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.polariser_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                             arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color,
		                             antialias=True, parent=self.parentCanvas.view.scene)
		self.polariser_Arrow.transform = scene.transforms.MatrixTransform()
		self.polariser_Arrow.interactive = True
		
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parentCanvas.view.scene,
		                            pos=self.position + (0.15 * self.arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		self.labelText.interactive = True
		
		# Rotate the polariser visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * self.theta)
	
	def __rotate(self, angle):
		self.polariser_Arrow.transform.rotate(np.rad2deg(angle), (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(np.rad2deg(angle), (0, 0, 1))
	
	def __create_quaternion(self, theta):
		q = R.from_rotvec(2 * theta * np.array((0, 0, 1)))
		self.polariserDirection = q.apply(np.array(self.polariserDirection))  # Update the rotation quaternion direction
	
	def analyse(self, incoming_SoP):
		"""
		Polarises the incoming polarization to outgoing polarization and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after polarisation
		"""
		
		incoming_SoP_direction=incoming_SoP.get_PolarizationVector()
		# Determine gamma -the angle between the orientation of the polariser and orientation of the incoming SoP
		if incoming_SoP_direction[0] == 0 and incoming_SoP_direction[1] == 0:  # Unpolarized incoming light
			gamma = np.pi / 2
		else:
			gamma = np.arccos(np.dot(incoming_SoP_direction, self.polariserDirection)) # Angle between the lines is the dot product of direction cosines of the lines
		print(f"polariser direction={self.polariserDirection}, polarization vector={incoming_SoP.get_PolarizationVector()}, gamma={gamma}")
		
		# From the basic relations for S0, S1, S2, S3 given in https://en.wikipedia.org/wiki/Stokes_parameters
		# The intensity value will be modified by cos^2(γ/2), the remaining intensity is distributed into Q and U
		# This distribution occurs so as to align the output radiation along the direction of orientation of the polariser
		I = incoming_SoP.get_intensity() * np.cos(gamma / 2) ** 2
		result_polarization_vector = I * self.polariserDirection
		result_SoP = StateofPolarization(mueller=np.append([I], result_polarization_vector), parentCanvas=self.parentCanvas, color=incoming_SoP.get_Color(), name=incoming_SoP.get_Name() + '+' + self.name)
		print(f"In Polariser: gamma={np.rad2deg(gamma)}, result(Q,U,V)={result_polarization_vector}, resultSoP={result_SoP.get_StokesVector()}, incoming={incoming_SoP.get_PolarizationVector()}")
		
		if self.parentCanvas is not None:
			self.__draw_polariserEffect(incoming_SoP, result_polarization_vector)
		
		return result_SoP
	
	def __draw_polariserEffect(self, incoming_SoP, result_polarization_vector):
		""" Draw the transformation visual """
		# Calculate mid point for drawing the arrow head
		mid_point = (incoming_SoP.get_PolarizationVector() + result_polarization_vector) / 2
		arrowHead = np.array([np.append(incoming_SoP.get_PolarizationVector(), mid_point)])  # Arrow direction, position
		
		Arrow(pos=np.array([incoming_SoP.get_PolarizationVector(), result_polarization_vector]), color=self.color,
		      method='gl', width=5., arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0,
		      arrow_color=self.color, antialias=True, parent=self.parentCanvas.view.scene)
	
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
		
		c2 = np.cos(2 * self.theta)
		s2 = np.sin(2 * self.theta)
		
		mueller = [[1, c2, s2, 0],
		           [c2, c2 ** 2, c2 * s2, 0],
		           [s2, c2 * s2, s2 ** 2, 0],
		           [0, 0, 0, 0]]
		
		self.mueller = 0.5 * np.array(mueller)
	
	# print("Polariser Mueller", mueller)
	
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
		return self.name + ": " + self.type + ", theta = " + str(self.get_OrientationAngle()) + "]:\n" + str(
			self.mueller) + "\n--------------\n"
