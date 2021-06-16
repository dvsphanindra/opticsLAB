# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import marshmallow as mm
import numpy as np
import toml
from marshmallow import Schema, fields, post_load, validates, ValidationError

from .component import BaseComponent


class _DetectorSchema(Schema):
	componentType = fields.Str(data_key="type",
	                           default="Detector")  # This field will be ignored by the component during instantiation
	name = fields.Str(required=True, error_messages={'required': "Please give an appropriate name for the component"})
	description = fields.Str()
	color = fields.Str(default='bluw')
	enabled = fields.Bool(default=True)
	
	class Meta:
		# additional = ["help"]  # List of fields to include in addition to the explicitly defined fields,
		ordered = True  # preserve the order of the schema definition
		unknown = mm.RAISE  # the behavior to take on unknown fields (EXCLUDE, INCLUDE, RAISE)
	
	# Additional validations other than those given above Raw definition
	@validates('componentType')
	def validate_type(self, value):
		if value != 'Detector':
			raise ValidationError("Component is not type: 'Detector', instead it is: '" + value + "'")
	
	# Action to be taken after loading the schema. Create a component from the schema
	@post_load
	def create_Component(self, data, **kwargs):
		component = Detector(**data)
		return component


class Detector(BaseComponent):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = "Detector"
		self.name = kwargs.get("name", "Detector_1")
		
		print("----Detector '%s' created----" % self.name)
	
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
