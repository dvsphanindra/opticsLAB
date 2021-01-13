# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import marshmallow as mm
from marshmallow import Schema, fields, pre_load, post_load, validates, ValidationError
from marshmallow_oneofschema import OneOfSchema

import component_definitions as component_def

import numpy as np


########################################################################################################
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
	
	# Additional validations other than those given above Raw definition
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
		component = component_def.Generic_Waveplate(**data)
		return component


#######################################################################################################################
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
		component = component_def.Linear_Polariser(**data)
		return component


########################################################################################################################
class _SourceSchema(Schema):
	componentType = fields.Str(data_key="type",
	                           default="Source")  # This field will be ignored by the component during instantiation
	name = fields.Str(required=True, error_messages={'required': "Please give an appropriate name for the component"})
	description = fields.Str()
	theta = fields.Float(required=True)
	radians = fields.Bool(default=False)
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
		# Verify theta
		if data["radians"]:
			assert  0 < data["theta"] < 2*np.pi, "Theta not in range: [0, 2π] for " + data["name"]
		else:
			assert 0 < data["theta"] < 360, "Theta not in range: [0, 360] for " + data["name"]
		
		# Verify stokes vector
		stokes_vector = data["mueller"]
		intensity = stokes_vector[0]
		polarizationVector = stokes_vector[1:]  # / self.stokes_vector[0] # TODO: To be verified
		assert np.sqrt(np.sum(np.square(polarizationVector))) <= intensity, "Irregular Stokes Vector: S0, vector, square, sum of square: {0}, {1}, {2}, {3}".format(
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
		component = component_def.StateofPolarization(**data)
		return component

########################################################################################################################
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
		component = component_def.Detector(**data)
		return component


############################################################################################################
class _ProjectSchema(Schema):
	componentType = fields.Str()
	name = fields.Str()
	description = fields.Str()
	version = fields.Str()
	author = fields.Str()
	created = fields.DateTime()
	modified = fields.DateTime()
	componentsList = fields.List(fields.Str())
	components = fields.List(fields.Dict())
	
	class Meta:
		ordered = True
		unknown = mm.RAISE
	
	@post_load
	def create_Project(self, data, **kwargs):
		# print("CS: data")
		# mm.pprint(data)
		
		components = _ComponentSchema().load(data["components"], many=True)
		project_component = component_def.Project(**data)
		components.insert(0, project_component) # Add to the beginning of the list
		return components


###############################################################################################################
class _ComponentSchema(OneOfSchema):
	type_schemas = {"Retarder": _GenericWavePlateSchema, "Polariser": _LinearPolariserSchema, "Source": _SourceSchema,
	                "Detector": _DetectorSchema}
	
	def get_obj_type(self, obj):
		if isinstance(obj, _GenericWavePlateSchema):
			return "Retarder"
		elif isinstance(obj, _LinearPolariserSchema):
			return "Polariser"
		elif isinstance(obj, _SourceSchema):
			return "Source"
		elif isinstance(obj, _DetectorSchema):
			return "Detector"
		else:
			raise Exception("Unknown object type: {}".format(obj.__class__.__name__))
	
	class Meta:
		ordered = True
		unknown = mm.RAISE
