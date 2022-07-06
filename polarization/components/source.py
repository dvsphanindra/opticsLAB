# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import marshmallow as mm
import numpy as np
import toml
from marshmallow import Schema, fields, pre_load, post_load, validates, ValidationError
from vispy import scene

from .component import BaseComponent


########################################################################################################################
class _SourceSchema(Schema):
	componentType = fields.Str(data_key="type",
	                           default="Source")  # This field will be ignored by the component during instantiation
	name = fields.Str(required=True, error_messages={'required': "Please give an appropriate name for the component"})
	description = fields.Str()
	# theta = fields.Float(required=True)
	# radians = fields.Bool(default=False)
	lambdaPresent = fields.Float(default=6563.0)
	mueller = fields.List(fields.List(fields.Float()))
	jones = fields.List(fields.List(fields.Float()))
	color = fields.Str(default='white')
	enabled = fields.Bool(default=True)
	
	class Meta:
		# additional = ["help"]  # List of fields to include in addition to the explicitly defined fields,
		ordered = True  # preserve the order of the schema definition
		unknown = mm.RAISE  # the behavior to take on unknown fields (EXCLUDE, INCLUDE, RAISE)
	
	# Additional validations other than those given above Raw definition
	@pre_load
	def validate_data(self, data, **kwargs):
		# # Verify theta
		# if data["radians"]:
		# 	assert  0 < data["theta"] < 2*np.pi, "Theta not in range: [0, 2π] for " + data["name"]
		# else:
		# 	assert 0 < data["theta"] < 360, "Theta not in range: [0, 360] for " + data["name"]
		#
		# Verify stokes vector
		stokes_vector = data["mueller"]
		intensity = stokes_vector[0]
		polarizationVector = stokes_vector[1:]  # / self.stokes_vector[0] # TODO: To be verified
		assert np.sqrt(np.sum(np.square(
			polarizationVector))) <= intensity, "Irregular Stokes Vector: S0, vector, square, sum of square: {0}, {1}, {2}, {3}".format(
			intensity, polarizationVector, np.square(polarizationVector),
			np.sum(np.square(polarizationVector)))
		# data["polarization_vector"]= polarizationVector
		# data["intensity"]= intensity
		return data
	
	@validates('componentType')
	def validate_type(self, value):
		if value != 'Source':
			raise ValidationError("Component is not type: 'Source', instead it is: '" + value + "'")
	
	# Action to be taken after loading the schema. Create a component from the schema
	@post_load
	def create_Component(self, data, **kwargs):
		component = StateofPolarization(**data)
		return component

########################################################################################################################
class StateofPolarization(BaseComponent):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = "Source"
		self.name = kwargs.get("name", "Source_1")
		self.lambdaPresent = kwargs.get("lambdaPresent", 6563.0)
		self.parentCanvas = kwargs.get('parentCanvas', None)
		
		# Set the help string for display in properties box
		self._helpString.update(
			{"lambdaPresent": "Current operating wavelength", "intensity": "Intensity component of the Stokes Vector",
			 "polarizationVector": "Polarization Vector"})
		
		self.stokes_vector = np.array(kwargs.get("mueller"))
		self.intensity = self.stokes_vector[0]
		self.polarizationVector = self.stokes_vector[1:].flatten()
		
		self.validate_StokesVector()
		
		self.color = kwargs.get("color")

		self.labelObjectVisual = None
		self.labelTextVisual = None
		
		if self.parentCanvas is not None:
			self.draw_visual()
		
		print("----Source '%s' created----" % self.name)
	
	def draw_visual(self):
		self.labelObjectVisual = scene.Text("•", font_size=100, bold=True, color=self.color, parent=self.parentCanvas.view.scene,
		                                    pos=self.polarizationVector.transpose())
		self.labelTextVisual = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parentCanvas.view.scene,
		                                  pos=self.polarizationVector.transpose() + (
					                            0.15 * self.polarizationVector.transpose()))
		self.labelObjectVisual.interactive = True
		self.labelTextVisual.interactive = True
		
	def display_Off(self):
		self.labelObjectVisual.visible = False
		self.labelTextVisual.visible = False
		
	def display_On(self):
		self.labelObjectVisual.visible = True
		self.labelTextVisual.visible = True
		
	def display(self, value):
		self.display_On() if value else self.display_Off()
	
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
		squareSum = np.sqrt(np.sum(np.square(self.polarizationVector)))
		if squareSum > self.stokes_vector[0]:
			if squareSum < 1.0001:  # Allow for numpy precision in calculations
				self.polarizationVector = np.round(self.polarizationVector, 13)
			else:
				raise AssertionError(f"Irregular Stokes Vector: S0={self.stokes_vector[0]}, (Q,U,V)={self.polarizationVector}, square(Q,U,V)={np.square(self.polarizationVector)}, sum of square(Q,U,V): {np.sum(np.square(self.polarizationVector))}")
	
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
