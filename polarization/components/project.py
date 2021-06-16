# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 14:18:15 2015

@author: D.V.S. Phanindra
"""

import marshmallow as mm
import toml
from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from .detector import _DetectorSchema
from .polarizers import _LinearPolariserSchema
from .source import _SourceSchema
from .waveplates import _GenericWavePlateSchema


class _ComponentSchema(OneOfSchema):
	"""
		Helps in (de)serializing object schema from name string and vice versa
	"""
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

########################################################################################################################
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
		
		components = _ComponentSchema().load(data["components"], many=True) # Load multiple components with the help of marshmallow OneOfSchema
		project_component = Project(**data)
		components.insert(0, project_component)  # Add to the beginning of the list
		return components


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

