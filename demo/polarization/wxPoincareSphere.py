import wx

import wx.propgrid as wxpg

import wxPoincareSphere_GUI

from objectListView import objectList

import time

import toml

import os

import numpy as np

from pyOptiCAD.polarization.vispy_canvas import PoincareSphere_VispyCanvas, PoincareSphere

from pyOptiCAD.polarization.vispy_canvas import PolarizationEllipse_VispyCanvas

from pyOptiCAD.polarization.components import Project

import datetime

import pyOptiCAD.polarization.components as cd

import inspect

class FileDrop(wx.FileDropTarget):
	def __init__(self, dropTargetWindow):
		wx.FileDropTarget.__init__(self)
		self.dropTargetWindow = dropTargetWindow
	
	# ---------------------------------------------------------------------------
	def OnDropFiles(self, x, y, droppedFile):
		# Send the dropped file path to the appropriate method in the class
		self.dropTargetWindow.openProjectFile(fileName=droppedFile[0])


###############################################################################

class wxPoincareTool(wxPoincareSphere_GUI.mainFrame):
	""" Sub Class the GUI created with wxFormBuilder and extend the functionality """
	
	def __init__(self, parent):
		wxPoincareSphere_GUI.mainFrame.__init__(self, parent)
		self.fileName = None
		self.selectedComponent = None
		self.saveFileName = None
		
		# Add Object List View
		sizer1 = wx.BoxSizer(wx.VERTICAL)
		self.componentsListViewer = objectList(self.panel_OpticalBench)
		sizer1.Add(self.componentsListViewer, 1, wx.ALL | wx.EXPAND, 5)
		self.panel_OpticalBench.SetSizer(sizer1)
		self.panel_OpticalBench.Layout()
		sizer1.Fit(self.panel_OpticalBench)
		self.componentsListViewer.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.componentsListViewer_onDClick)
		
		self.fileName = None
		self.selectedComponent = None # Temporary variable for component under selection
		self.project_componentsList = [] # List of components used in the currently open project
		self.saveFileName = None
		self.selectedComponent_dataChanged = False
		self.project_dataChanged = False
		# Get the dictionary of available public classes in a module (classes not starting with '_')
		self.available_Components = {name[0]: eval("cd." + name[0]) for name in inspect.getmembers(cd, inspect.isclass) if name[0][0] != '_'}
		print("Available Components: ", self.available_Components)
		self.choice_Components.Clear()
		self.choice_Components.Append("None")
		for key in self.available_Components.keys():
			self.choice_Components.Append(key)
		self.choice_Components.SetSelection(0)
		
		# Add a (default) page to the Property Grid. Otherwise the widget will not work properly
		self.propertyGrid_Config.AddPage("Page 1")
		
		self.panel_Poincare.canvas = PoincareSphere_VispyCanvas(app="wx", parent=self.panel_Poincare, sizes=self.panel_Poincare.GetSize(), azimuth=90, elevation=10, resizable=True, labels=("Q", "U", "V"))
		
		# Interactions with the figure
		self.panel_Poincare.canvas.canvas.events.mouse_press.connect(self.canvas_ImageOnClick)
		self.panel_Poincare.canvas.canvas.events.mouse_release.connect(self.canvas_ImageOnClickRelease)
		self.panel_Poincare.canvas.canvas.events.mouse_move.connect(self.canvas_ImageMouseMotion)
		self.figure_LeftButtonPress = False
		self.selected_object=None
		self.intermediate_SoP = []
		
		self.panel_PolarizationEllipse.canvas = PolarizationEllipse_VispyCanvas(app="wx", parent=self.panel_PolarizationEllipse,
		                                                                        sizes=self.panel_PolarizationEllipse.GetSize(), resizable=True)
		
		# Display the camera coordinates
		self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.panel_Poincare.canvas.view.camera.elevation, self.panel_Poincare.canvas.view.camera.azimuth), 2)
		
		# TODO to add these later
		dt = FileDrop(self)
		self.SetDropTarget(dt)
		
		
		# Set Accelerator keys
		entries = [wx.AcceleratorEntry() for i in range(4)]
		
		ID_NEW = wx.NewIdRef()
		ID_OPEN = wx.NewIdRef()
		ID_SAVE = wx.NewIdRef()
		ID_QUIT = wx.NewIdRef()
		self.Bind(wx.EVT_MENU, self.button_NewProject_OnClick, ID_NEW)
		self.Bind(wx.EVT_MENU, self.button_OpenProject_OnClick, ID_OPEN)
		self.Bind(wx.EVT_MENU, self.saveProjectData, ID_SAVE)
		self.Bind(wx.EVT_MENU, self.mainFrame_OnClose, ID_QUIT)
		
		entries[0].Set(wx.ACCEL_CTRL, ord('N'), ID_NEW)
		entries[1].Set(wx.ACCEL_CTRL, ord('O'), ID_OPEN)
		entries[2].Set(wx.ACCEL_CTRL|wx.WXK_SHIFT, ord('S'), ID_SAVE)
		entries[3].Set(wx.ACCEL_CTRL, ord('Q'), ID_QUIT)
		
		accelerator = wx.AcceleratorTable(entries)
		self.SetAcceleratorTable(accelerator)
		
		self.staticText_ProjectFile.SetLabelText("Project File: None")
		
		self.project_componentsList = Project.create_from_schema(schema="./polarimeter.toml")
		print("Project:", self.project_componentsList)

		self.componentsListViewer.updateList(self.project_componentsList[1:])

		self.selectedComponent = self.project_componentsList[0]
		self.displayComponentProperties(self.selectedComponent)
		print(self.selectedComponent)
		for selected_object in self.project_componentsList:
			if selected_object.get_Type() not in ["Project", "Detector"]:
				selected_object.draw_visual(self.panel_Poincare.canvas)
		self.poincareSphere=PoincareSphere(radius=1.0, center=(0.0, 0.0, 0.0), parentCanvas=self.panel_Poincare.canvas.canvas, labels=("Q", "U", "V"))
		
	def displayComponentProperties(self, component):
		# print(vars(component))
		page = self.propertyGrid_Config.GetPageByName("Page 1")
		if page is not None:
			self.propertyGrid_Config.ClearPage(page)    
		for key, value in vars(component).items():
			if '_' not in key:
				name = key.capitalize()
				# print(key, name, value, type(value))
				
				if type(value) is bool:
					self.propertyGrid_Config.Append(wxpg.BoolProperty(name, key, value=value))
					self.propertyGrid_Config.SetPropertyAttribute(key, "UseCheckbox", True)  # The attribute name and value
				
				if type(value) is float:
					self.propertyGrid_Config.Append(wxpg.FloatProperty(name, key, value=value))
				
				if type(value) is int:
					self.propertyGrid_Config.Append(wxpg.IntProperty(name, key, value=value))
				
				if type(value) is str or type(value) is type(None) or isinstance(value, datetime.datetime):
					if "color" in key:
						try:
							value = wx.Colour([int(x) for x in value.lstrip('(').rstrip(')').split(',')])
						except:
							pass
						self.propertyGrid_Config.Append(wxpg.ColourProperty(name, key, value=value))
					else:
						self.propertyGrid_Config.Append(wxpg.StringProperty(name, key, value=str(value)))
				if type(value) is list or type(value) is tuple or isinstance(value, np.ndarray):
					value_str = [str(x) for x in value]
					self.propertyGrid_Config.Append(wxpg.ArrayStringProperty(name, key, value=value_str))
				
				# Add help strings and read only attributes
				
				try:
					helpString = component.get_HelpString(key)
					# print(key, helpString)
					self.propertyGrid_Config.SetPropertyHelpString(key, helpString)
				except:
					pass
				if component.get_isReadOnlyParameter(key):
					self.propertyGrid_Config.SetPropertyReadOnly(key, True)
					if key=='type' or key=='created' or key=='modified':
						self.propertyGrid_Config.DisableProperty(key)
				
				if type(value) is dict:
					self.propertyGrid_Config.Append(wxpg.PropertyCategory(key.split('.')[1], name))
					print("-----" + key + "---------")
					raise Exception("Dict found")
					# self.displayComponent(value, component + '.' + key)
	
	def button_OpenProject_OnClick( self, event ):
		wildcard = "Config source (*.toml)|*.toml|All files (*.*)|*.*"
		dialog = wx.FileDialog(parent=None, message="Choose a file", defaultDir=os.getcwd(), wildcard=wildcard,
		                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

		if dialog.ShowModal() == wx.ID_OK:
			fileName = dialog.GetPath()
		dialog.Destroy()
		# fileName = "./polarimeter.toml"
		self.openProjectFile(fileName=fileName)
	
	def openProjectFile(self, fileName):
		
		self.saveFileName = fileName
		
		self.staticText_ProjectFile.SetLabelText("Project File: "+fileName)
		
		_, f_name = os.path.split(fileName)
		
		page = self.propertyGrid_Config.GetPageByName("Page 1")
		if page is not None:
			self.propertyGrid_Config.ClearPage(page)
		
		self.selectedComponent = self.project_componentsList
		self.intermediate_SoP = []
		
		self.project_componentsList = Project.create_from_schema(schema=fileName)
		print("Project:", self.project_componentsList)
		

		self.selectedComponent = self.project_componentsList[0]
		print(self.selectedComponent)
		# self.propertyGrid_Config.Append(wxpg.PropertyCategory(self.selectedComponent))
		self.componentsListViewer.updateList(self.project_componentsList[1:])
		self.displayComponentProperties(self.selectedComponent)
		
		# TODO: Delete the old poincare sphere
		for selected_object in self.project_componentsList:
			if selected_object.get_Type() not in ["Project", "Detector"]:
				selected_object.draw_visual(self.panel_Poincare.canvas.view.scene)
		
		self.selectedComponent_dataChanged = False
		self.project_dataChanged = False

	def button_NewProject_OnClick( self, event ):
		page = self.propertyGrid_Config.GetPageByName("Page 1")
		if page is not None:
			self.propertyGrid_Config.ClearPage(page)
		self.staticText_ProjectFile.SetLabelText("Project File: File not saved")
		
		self.project_componentsList = self.selectedComponent
		self.project_componentsList['Created'] = time.strftime("%d-%b-%Y %I.%M%p")
		
	def button_SaveProjectAs_OnClick( self, event ):
		self.saveProjectDataAs() # Get the filename from the user
		
	def saveProjectDataAs(self):
		wildcard = "Config source (*.toml)|*.toml|All files (*.*)|*.*"
		dialog = wx.FileDialog(parent=None, message="Choose a file", defaultDir=os.getcwd(), wildcard=wildcard,
		                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		
		if dialog.ShowModal() == wx.ID_OK:
			self.saveFileName = dialog.GetPath()
			self.SetStatusText(self.saveFileName, 1)
		
		dialog.Destroy()
		self.saveProjectData()
	
	def button_SaveProject_OnClick( self, event ):
		if self.saveFileName is None: # If the user has not selected any file,
			self.saveProjectDataAs() # Get the file
		else:
			self.saveProjectData()
	
	def saveProjectData(self):
		if self.project_componentsList is not None:
			self.project_componentsList['modified']=time.strftime("%d-%b-%Y %I.%M%p")
			with open(self.saveFileName, "w+") as file_object:
				toml.dump(self.project_componentsList, file_object)
			self.project_dataChanged = False
			self.staticText_ProjectFile.SetLabelText("Project File: "+self.saveFileName)
	
	def mainFrame_OnSize( self, event ):
		# print(self.panel_Poincare.GetSize())
		self.panel_Poincare.canvas.size=self.panel_Poincare.GetSize()
		self.panel_Poincare.Refresh()
	
	def componentsListViewer_onDClick(self, event):
		selected_object=self.componentsListViewer.GetSelectedObject()
		self.displayComponentProperties(selected_object)
		
	def propertyGrid_Config_OnPropertyChanged(self, event):
		p = event.GetProperty()
		if p:
			# TODO: validation
			print(self.selectedComponent.validate({p.GetName().lower():p.GetValue()}))
			self.selectedComponent.__dict__[p.GetName().lower()] = p.GetValue()
			print(vars(self.selectedComponent))
		
	# Use for preventing properties from changing
	def propertyGrid_Config_OnPropertyChanging(self, event):
		# p = event.GetProperty()
		# if p:
		# 	print('%s changing to "%s"\n' % (p.GetName(), p.GetValueAsString()))
		# TODO Use Veto()
		pass
	
	@staticmethod
	def __parseConfig(fileName):
		data = toml.load(fileName)
		return data
	
	def mainFrame_OnClose(self, event):
		response = wx.ID_OK
		# if self.project_dataChanged:
		# 	dialog = wx.MessageDialog(None, 'Data is changed. Are you sure to quit without saving?', 'Quit without saving', wx.OK |wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_QUESTION)
		# 	response = dialog.ShowModal()
		if response == wx.ID_OK:
			self.Destroy()
	
	def button_AddComponent_OnClick(self, event):
		if not self.project_componentsList:
			wx.MessageBox(parent=self, message='Project not created. Please create a New Project', caption="No Project Created", style=wx.ICON_ERROR)
		else:
			self.project_componentsList.append(self.selectedComponent)
			print(self.project_componentsList)
			self.componentsListViewer.append2List(self.selectedComponent)
			self.project_dataChanged = True
	
	def choice_Components_OnChoice(self, event):
		page = self.propertyGrid_Config.GetPageByName("Page 1")
		if page is not None:
			self.propertyGrid_Config.ClearPage(page)
		# TODO to load the choices based on the components in the template dictionary (using dictionary keys)
		component = self.choice_Components.GetStringSelection()
		self.selectedComponent = self.available_Components[component]()
		self.displayComponentProperties(self.selectedComponent)
	
	def canvas_ImageOnClick(self, event):
		if event.button == 1:
			self.figure_LeftButtonPress = True
		
	def canvas_ImageMouseMotion(self, event):
		if self.figure_LeftButtonPress:
			self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.panel_Poincare.canvas.view.camera.elevation, self.panel_Poincare.canvas.view.camera.azimuth), 2)
	
	def canvas_ImageOnClickRelease(self, event):
		if event.button == 1:
			self.figure_LeftButtonPress = False
			# print("Here: ",self.panel_Poincare.canvas.selected_object_name)
			# print(self.project_componentsList)
			for component in self.project_componentsList:
				# print(component.get_Type(), component.get_Name())
				if component.get_Name() == self.panel_Poincare.canvas.selected_object_name:
					self.displayComponentProperties(component)
					if component.get_Type() in "Source":
						self.panel_PolarizationEllipse.canvas.set_StokesVector(component.get_StokesVector())
			for component in self.intermediate_SoP:
				if component.get_Name() == self.panel_Poincare.canvas.selected_object_name:
					self.panel_PolarizationEllipse.canvas.set_StokesVector(component.get_StokesVector())
			
	def button_ResetView_OnClick( self, event ):
		self.panel_Poincare.canvas.view.camera.azimuth = 90
		self.panel_Poincare.canvas.view.camera.elevation = 10
		self.panel_PolarizationEllipse.canvas.view.camera.rect = (-1, -1, 2, 2)
		self.panel_PolarizationEllipse.canvas.view.camera.zoom(0.75)
		self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.panel_Poincare.canvas.view.camera.elevation, self.panel_Poincare.canvas.view.camera.azimuth), 2)
		
	def button_Analyse_OnClick( self, event ):
		# self.poincareSphere.parent=None # Remove the old poincare sphere
		incoming_SoP = self.project_componentsList[1]
		for component in self.project_componentsList:
			if component.get_Type() not in ["Source", "Detector", "Project"]:
				SoP=component.analyse(incoming_SoP)
				SoP.draw_visual(self.panel_Poincare.canvas)
				incoming_SoP=SoP
				self.intermediate_SoP.append(SoP)
		
		# Add the new poincare sphere for viewing it
		self.poincareSphere.update_sphere()
		
###############################################################################

if __name__ == "__main__":
	app = wx.App(False)
	
	GUI = wxPoincareTool(None)
	
	GUI.Raise()
	
	GUI.Show(True)
	
	app.MainLoop()
