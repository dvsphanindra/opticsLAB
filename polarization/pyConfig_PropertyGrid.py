import wx

import wx.propgrid as wxpg

import toml

import os

class pyConfig_PropertyGrid(wxpg.PropertyGridManager):
	
	def __init__(self, parent, data=None, fileName=None):
		print(self, parent)
		wxpg.PropertyGridManager.__init__(self, parent, style=wxpg.PG_SPLITTER_AUTO_CENTER |
																	wxpg.PGMAN_DEFAULT_STYLE | wxpg.PG_DESCRIPTION |
																	wxpg.PG_TOOLBAR | wx.TAB_TRAVERSAL|
																	wxpg.PG_BOLD_MODIFIED)# | wxpg.PG_EX_MODE_BUTTONS |
																	# wxpg.PG_EX_TOOLBAR_SEPARATOR)
		# Show help as tooltips
		self.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)# | wxpg.PG_EX_MODE_BUTTONS | wxpg.PG_EX_TOOLBAR_SEPARATOR)
		
		self.Bind(wxpg.EVT_PG_CHANGED, self.propertyGrid_Config_OnPropertyChanged)
		self.Bind(wxpg.EVT_PG_SELECTED, self.propertyGrid_Config_OnPropGridSelect)
		self.Bind(wxpg.EVT_PG_RIGHT_CLICK, self.propertyGrid_Config_OnPropGridRightClick)
		
		self.dataChanged = False
		self.data = data
		self.fileName = fileName
		
		
		# self.propertyGrid_Config = None
		self.dataChanged = False
		
		print("Loading component templates...")
		templatesDir = "./templates"
		templateFiles = [f for f in os.listdir(templatesDir) if os.path.isfile(os.path.join(templatesDir, f)) and ".template.toml" in f]
		self.templateDict = {}
		self.helpStrings={}
		for templateFile in templateFiles:
			print("Parsing template: "+templateFile)
			d = toml.load(os.path.join(templatesDir, templateFile))
			self.templateDict.update(d)
			component_name = list(d.keys())[0]
			component=d[component_name]
			for key, value in component.items():
				if "help" in key:
					# print(key,value)
					self.helpStrings.update({component_name+'.'+key:value})
			# templateDict.update()
		# print(templateDict)
		print(self.helpStrings)
		
		print("Loading colors...")
		self.namedColors=toml.load(os.path.join(templatesDir,"namedColorsList.toml"))
		print(self.namedColors)
	
	def saveConfig(self, saveFileName):
		if self.propertyGrid_Config is not None:
			with open(self.saveFileName, "w+") as file_object:
				toml.dump(self.data, file_object)
			self.dataChanged = False
	
	def propertyGrid_Config_OnPropertyChanged(self, event):
		p = event.GetProperty()
		if p:
			if p.GetLabel() == 'color':
				newValue=p.GetValueAsString()
			else:
				newValue = p.GetValue()
			# print(p.GetName().split('.'), type(new))
			a = p.GetName().split('.')
			a=a[1:] # Remove top level name
			print('%s changed to "%s (%s)"\n' % (p.GetName(), p.GetValueAsString(), p.GetLabel()))
			print(self.data[a[0]][a[1]])
			dic = self.data
			for aa in a[:-1]:
				dic = dic[aa]
				print(aa, "==", dic)
			print("Updating")
			dic[a[-1]]=newValue
			print(dic)
			self.dataChanged = True
	
	def propertyGrid_Config_OnPropertyChanging(self, event):
		# p = event.GetProperty()
		# if p:
		# 	print('%s changing to "%s"\n' % (p.GetName(), p.GetValueAsString()))
		pass
	
	def parseConfig(self, fileName):
		self.data = toml.load(fileName)
		# print(self.data)
		self.Append(wxpg.PropertyCategory(list(self.data.keys())[0]))
		self.__updateTable__(self.data, "Top")
			
	def propertyGrid_Config_OnPropGridSelect(self, event):
		pass
	
	def propertyGrid_Config_OnPropGridRightClick(self, event):
		print("Property Right CLick: ", event.GetProperty())
	
	# Recursive method. Called on the encounter of every dict type object
	def __updateTable__(self, data, parentComponent):
		componentType = data.get("type")
		print("componentType: ", componentType)
		for key, value in data.items():
			# print(type(value))
			if not '@' in key:
				name = parentComponent + "." + key
				print(componentType, name)
				
				if type(value) is bool:
					self.Append(wxpg.BoolProperty(key, name, value=value))
					self.SetPropertyAttribute(name, "UseCheckbox", True)  # The attribute name and set to use checkbox
				
				if type(value) is float:
					self.Append(wxpg.FloatProperty(key, name, value=value))
				
				if type(value) is int:
					self.Append(wxpg.IntProperty(key, name, value=value))
				
				if type(value) is str or type(value) is type(None):
					if "color" in key:
						try:
							value = wx.Colour([int(x) for x in value.lstrip('(').rstrip(')').split(',')])
						except:
							pass
						self.Append(wxpg.ColourProperty(key, name, value=value))
					else:
						print(key, name)
						self.Append(wxpg.StringProperty(key, name, value=str(value)))
						print("Appending..")
						helpString = self.helpStrings.get(componentType + '.' + key + '@help', "Empty")
						print(self.GetPropertyValues(inc_attributes=True), helpString)
						if helpString is not "Empty":
							self.SetPropertyHelpString(name, helpString)
				if type(value) is list:
					if data.get("%s@choices" % key, "Empty") is not "Empty":
						value_str = [str(x) for x in value]
						t = [x for x in range(len(value))]
						self.Append(wxpg.EnumProperty(key, name, key, name, value_str, t, 0))
					else:
						value_str = [str(x) for x in value]
						self.Append(wxpg.ArrayStringProperty(key, name, value=value_str))
				
				# Add help strings
				if componentType is not None:
					helpString = self.helpStrings.get(componentType + '.' + key + '@help', "Empty")
					if helpString is not "Empty":
						print(name, helpString)
						self.SetPropertyHelpString(name, helpString)
				
				if type(value) is dict:
					self.Append(wxpg.PropertyCategory(key, name))
					print("-----" + key + "---------")
					self.__updateTable__(value, parentComponent + '.' + key)
	
