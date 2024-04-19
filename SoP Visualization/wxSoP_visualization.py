import wx

import wxSoP_visualization_GUI

import numpy as np

from pyOptiCAD.polarization.vispy_canvas import PolarizationEllipse_VispyCanvas
from pyOptiCAD.polarization.components import StateofPolarization

from poincareSphere_VispyCanvas import PoincareSphere_VispyCanvas


class wxPoincareTool(wxSoP_visualization_GUI.mainFrame):
	""" Sub Class the GUI created with wxFormBuilder and extend the functionality """
	
	def __init__(self, parent):
		wxSoP_visualization_GUI.mainFrame.__init__(self, parent)
		
		self.checkList_selectedItems = []
		self.panel_PoincareSphere.canvas = PoincareSphere_VispyCanvas(app="wx", parent=self.panel_PoincareSphere,
		                                                              size=self.panel_PoincareSphere.GetSize(), azimuth=90,
		                                                              elevation=10, resizable=True, labels=("Q", "U", "V"))
		
		# Interactions with the figure
		self.panel_PoincareSphere.canvas.canvas.events.mouse_press.connect(self.canvas_ImageOnClick)
		self.panel_PoincareSphere.canvas.canvas.events.mouse_release.connect(self.canvas_ImageOnClickRelease)
		self.panel_PoincareSphere.canvas.canvas.events.mouse_move.connect(self.canvas_ImageMouseMotion)
		self.figure_LeftButtonPress = False
		
		# Display the camera coordinates
		self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.panel_PoincareSphere.canvas.view.camera.elevation,
		                                                     self.panel_PoincareSphere.canvas.view.camera.azimuth), 2)
		
		self.panel_PolarizationEllipse.canvas = PolarizationEllipse_VispyCanvas(app="wx",
		                                                                        parent=self.panel_PolarizationEllipse,
		                                                                        sizes=self.panel_PolarizationEllipse.GetSize(),
		                                                                        resizable=True)
		self.sop_list = dict()  # To Maintain a list of state of polarizations entered
		
	def canvas_ImageOnClick(self, event):
		if event.button == 1:
			self.figure_LeftButtonPress = True
	
	def canvas_ImageMouseMotion(self, event):
		if self.figure_LeftButtonPress:
			self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.panel_PoincareSphere.canvas.view.camera.elevation,
			                                                     self.panel_PoincareSphere.canvas.view.camera.azimuth), 2)

	def canvas_ImageOnClickRelease(self, event):
		if event.button == 1:
			self.figure_LeftButtonPress = False
			print("Here: ", self.panel_PoincareSphere.canvas.selected_object_name)
			
	def button_Reset_OnClick(self, event):
		self.panel_PoincareSphere.canvas.view.camera.azimuth = 30
		self.panel_PoincareSphere.canvas.view.camera.elevation = 30
		self.panel_PolarizationEllipse.canvas.view.camera.rect = (-1, -1, 2, 2)
		self.panel_PolarizationEllipse.canvas.view.camera.zoom(0.75)
		self.SetStatusText("E: {0:3.2f}, A: {1:3.2f}".format(self.panel_PoincareSphere.canvas.view.camera.elevation,
		                                                     self.panel_PoincareSphere.canvas.view.camera.azimuth), 2)
		
		self.panel_PolarizationEllipse.canvas.stokesVector_visual.parent = None
		self.panel_PolarizationEllipse.canvas.stokesVectorArrow_visual.parent = None
		
		sop_list = list(self.sop_list.keys())
		for sop_string in sop_list:
			self.remove_sop(sop_string)
		self.checkList_oldValues.Clear()
		self.sop_list.clear()
		self.textCtrl_Name.SetValue('SoP1')
		self.textCtrl_I.SetValue('1.0')
		self.textCtrl_Q.SetValue('1.0')
		self.textCtrl_U.SetValue('0.0')
		self.textCtrl_V.SetValue('0.0')
		
	def button_Show_OnClick(self, event):
		i , q, u , v = self.textCtrl_I.GetValue(), self.textCtrl_Q.GetValue(), self.textCtrl_U.GetValue(), self.textCtrl_V.GetValue()
		I = float(i)
		Q = float(q)
		U = float(u)
		V = float(v)
		name = self.textCtrl_Name.GetValue()
		color = self.colourPicker_color.GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
		
		if Q * Q + U * U + V * V > I * I:
			wx.MessageBox("Invalid Stokes Parameters", "Invalid Stokes Parameters", style=wx.OK|wx.ICON_ERROR)
		else:
			if name in self.sop_list.keys():  # Ensure unique names
				name = list(self.sop_list.keys())[-1]+'1'
				self.textCtrl_Name.SetValue(name)
			sop = StateofPolarization(mueller=np.array((I, Q, U, V)), color=color, name=name, parentCanvas=self.panel_PoincareSphere.canvas)
			
			self.checkList_oldValues.Append(f"{name}:{i},{q},{u},{v}:{color}")
			self.checkList_oldValues.Check(self.checkList_oldValues.GetCount()-1)
			self.sop_list.update({name: sop})
			self.panel_PolarizationEllipse.canvas.set_StokesVector(sop.get_StokesVector())
		
	def button_Remove_OnButtonClick(self, event):
		for item in self.checkList_oldValues.GetSelections():
			sop_string = self.checkList_oldValues.GetString(item).split(':')[0]
			self.remove_sop(sop_string)
			self.checkList_oldValues.Delete(item)
			
	def remove_sop(self, sop_string):
		sop = self.sop_list.pop(sop_string)
		sop.labelObjectVisual.parent = None
		sop.labelTextVisual.parent = None
		del sop
		
	def checkList_oldValues_OnCheckListBoxToggled(self, event):
		checkedStrings = []
		for sop in self.checkList_oldValues.GetCheckedStrings():
			nameString = sop.split(':')[0]
			self.sop_list[nameString].display_On()
			checkedStrings.append(nameString)
		notCheckedStrings = set(self.sop_list.keys()) - set(checkedStrings)  # Get the difference of the lists
		# print("99: Checked = ", checkedStrings, "Not Checked:", notCheckedStrings)
		for sop in notCheckedStrings:
			nameString = sop.split(':')[0]
			self.sop_list[nameString].display_Off()
		
	def checkList_oldValues_OnCheckListBoxDClick(self, event):
		index = event.GetSelection()
		name = self.checkList_oldValues.GetString(index).split(':')[0]
		sop = self.sop_list[name]
		stokesVector = sop.get_StokesVector()
		self.textCtrl_I.SetValue(str(stokesVector[0]))
		self.textCtrl_Q.SetValue(str(stokesVector[1]))
		self.textCtrl_U.SetValue(str(stokesVector[2]))
		self.textCtrl_V.SetValue(str(stokesVector[3]))
		self.panel_PolarizationEllipse.canvas.set_StokesVector(stokesVector)
		

###############################################################################

if __name__ == "__main__":
	app = wx.App(False)
	
	GUI = wxPoincareTool(None)
	
	GUI.Raise()
	
	GUI.Show(True)
	
	app.MainLoop()
