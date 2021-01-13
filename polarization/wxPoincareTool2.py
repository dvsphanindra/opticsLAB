import wx

import wx.propgrid as wxpg

import wxPoincareTool_GUI

from objectListView import objectList

import time

import toml

import os

import numpy as np

from poincareSphere import wxPoincareSphereAxes

from component_definitions import Generic_Waveplate, Quarter_Waveplate, Half_Waveplate, Linear_Polariser, Project, StateofPolarization, Detector

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from mpl_toolkits.mplot3d import Axes3D

import datetime

import component_definitions as cd

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

class wxPoincareTool(wxPoincareTool_GUI.mainFrame):
	""" Sub Class the GUI created with wxFormBuilder and extend the functionality """
	
	def __init__(self, parent):
		wxPoincareTool_GUI.mainFrame.__init__(self, parent)
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
		
		figHeight,figWidth = 3, 3
		# Create a matplotlib Figure
		self.figure_MainImage = Figure(figsize=(figWidth, figHeight), tight_layout=True)
		self.canvas_MainImage = FigCanvas(self.panel_Poincare, wx.ID_ANY, self.figure_MainImage) # Create canvas before plot to enable mouse interaction
		self.axes_MainImage = self.figure_MainImage.add_subplot(111, projection='3d', facecolor='Gainsboro', frame_on=True)
		self.axes_MainImage.view_init(20,60)
		self.canvas_MainImage.draw()
		self.poincareSphereAxes = wxPoincareSphereAxes(axes=self.axes_MainImage)
		
		# And add it to the appropriate panel
		sizer111 = wx.BoxSizer(wx.VERTICAL)
		sizer111.Add(self.canvas_MainImage, 1, wx.ALL|wx.EXPAND, 1)
		self.panel_Poincare.SetSizer(sizer111)
		# To adjust to fit the panel
		self.panel_Poincare.Fit()
		
		# Display the camera coordinates
		self.SetStatusText("E: 20, A: 60", 2)
		
		# Interactions with the figure
		self.figure_MainImage.canvas.mpl_connect("button_press_event", self.axes_ImageOnClick)
		self.figure_MainImage.canvas.mpl_connect("motion_notify_event", self.axes_ImageMouseMotion)
		self.figure_MainImage.canvas.mpl_connect('button_release_event', self.axes_ImageOnClickRelease)
		self.figure_LeftButtonPress = False
		
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
		self.displayComponent(self.selectedComponent)
		
	def displayComponent(self, component):
		# print(vars(component))
		for key, value in vars(component).items():
			if '_' not in key:
				name = key.capitalize()
				# print(key, name, value, type(value))
				
				if type(value) is bool:
					self.propertyGrid_Config.Append(wxpg.BoolProperty(name, key, value=value))
					self.propertyGrid_Config.SetPropertyAttribute(key, "UseCheckbox", True)  # The attribute name and value
				
				if type(value) is float or isinstance(value, np.float):
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
				helpString = component.get_HelpString(key)
				self.propertyGrid_Config.SetPropertyHelpString(key, helpString)
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
		self.project_componentsList = self.__parseConfig(f_name)
		print(self.project_componentsList)
		self.propertyGrid_Config.Append(wxpg.PropertyCategory(list(self.project_componentsList.keys())[0]))
		self.__updateTable(self.project_componentsList, "project")
		self.selectedComponent = self.project_componentsList
		
		self.selectedComponent_dataChanged = False
		self.project_dataChanged = False

	def button_NewProject_OnClick( self, event ):
		page = self.propertyGrid_Config.GetPageByName("Page 1")
		if page is not None:
			self.propertyGrid_Config.ClearPage(page)
		self.staticText_ProjectFile.SetLabelText("Project File: File not saved")
		self.selectedComponent = self.templateDict['project']
		self.project_componentsList = self.selectedComponent
		self.project_componentsList['Created'] = time.strftime("%d-%b-%Y %I.%M%p")
		self.__updateTable(self.selectedComponent, "project")
		
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
			self.project_componentsList['Modified']=time.strftime("%d-%b-%Y %I.%M%p")
			with open(self.saveFileName, "w+") as file_object:
				toml.dump(self.project_componentsList, file_object)
			self.project_dataChanged = False
			self.staticText_ProjectFile.SetLabelText("Project File: "+self.saveFileName)
	
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
		self.displayComponent(self.selectedComponent)
	
	def axes_ImageOnClick(self, event):
		if event.button == 1:
			# self.SetStatusText("({0:3.3f},{1:3.3f})".format(event.xdata, event.ydata), 2)
			self.figure_LeftButtonPress = True
		
	def axes_ImageMouseMotion(self, event):
		if self.figure_LeftButtonPress:
			# self.SetStatusText("({0:3.3f},{1:3.3f})".format(event.xdata, event.ydata), 2)
			self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.axes_MainImage.elev, self.axes_MainImage.azim, event.ydata), 2)
	
	def axes_ImageOnClickRelease(self, event):
		if event.button == 1:
			# self.SetStatusText("({0:3.3f},{1:3.3f})".format(event.xdata, event.ydata), 2)
			self.figure_LeftButtonPress = False
			
	def button_ResetView_OnClick( self, event ):
		self.axes_MainImage.view_init(20, 60)
		self.canvas_MainImage.draw()
		self.SetStatusText("E: 20, A: 60", 2)
		
###############################################################################

if __name__ == "__main__":
	app = wx.App(False)
	
	GUI = wxPoincareTool(None)
	
	GUI.Raise()
	
	GUI.Show(True)
	
	app.MainLoop()
