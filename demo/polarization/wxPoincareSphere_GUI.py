# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg

ID_NEW_PROJECT = 1000
ID_OPEN_PROJECT = 1001
ID_SAVE_PROJECT = 1002
ID_SAVE_PROJECT_AS = 1003
ID_QUIT = 1004
ID_CREDITS = 1005

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Poincare Sphere Demo", pos = wx.DefaultPosition, size = wx.Size( 1159,901 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.menuBar = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.newProject = wx.MenuItem( self.file, ID_NEW_PROJECT, u"&New Project..."+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.newProject )

		self.file.AppendSeparator()

		self.openProject = wx.MenuItem( self.file, ID_OPEN_PROJECT, u"&Open Project..."+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.openProject )

		self.saveProject = wx.MenuItem( self.file, ID_SAVE_PROJECT, u"&Save Project"+ u"\t" + u"Ctrl+Shift+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.saveProject )

		self.saveProjectAs = wx.MenuItem( self.file, ID_SAVE_PROJECT_AS, u"Save Project &As..."+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.saveProjectAs )

		self.file.AppendSeparator()

		self.quit = wx.MenuItem( self.file, ID_QUIT, u"&Quit"+ u"\t" + u"Ctrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.quit )

		self.menuBar.Append( self.file, u"&File" )

		self.about = wx.Menu()
		self.credits = wx.MenuItem( self.about, ID_CREDITS, u"Credits", wx.EmptyString, wx.ITEM_NORMAL )
		self.about.Append( self.credits )

		self.menuBar.Append( self.about, u"&About" )

		self.SetMenuBar( self.menuBar )

		sizer_Top = wx.BoxSizer( wx.VERTICAL )

		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_NewProject = wx.Button( self.m_panel6, wx.ID_ANY, u"New Project", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_NewProject, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_OpenProject = wx.Button( self.m_panel6, wx.ID_ANY, u"Open Project", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_OpenProject, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_SaveProjectAs = wx.Button( self.m_panel6, wx.ID_ANY, u"Save As...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_SaveProjectAs, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_SaveProject = wx.Button( self.m_panel6, wx.ID_ANY, u"Save Project", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_SaveProject, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer8.Add( bSizer2, 0, wx.EXPAND, 5 )

		self.staticText_ProjectFile = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Project File:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.staticText_ProjectFile.Wrap( -1 )

		self.staticText_ProjectFile.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer8.Add( self.staticText_ProjectFile, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_panel10 = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.panel_Poincare = wx.Panel( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer81 = wx.BoxSizer( wx.VERTICAL )


		self.panel_Poincare.SetSizer( bSizer81 )
		self.panel_Poincare.Layout()
		bSizer81.Fit( self.panel_Poincare )
		bSizer9.Add( self.panel_Poincare, 3, wx.EXPAND |wx.ALL, 5 )

		self.panel_Properties = wx.Panel( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE|wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.propertyGrid_Config = pg.PropertyGridManager(self.panel_Properties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PGMAN_DEFAULT_STYLE|wx.propgrid.PG_BOLD_MODIFIED|wx.propgrid.PG_DESCRIPTION|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.TAB_TRAVERSAL)
		self.propertyGrid_Config.SetExtraStyle( wx.propgrid.PG_EX_MODE_BUTTONS|wx.propgrid.PG_EX_TOOLBAR_SEPARATOR )
		bSizer3.Add( self.propertyGrid_Config, 1, wx.ALL|wx.EXPAND, 5 )


		self.panel_Properties.SetSizer( bSizer3 )
		self.panel_Properties.Layout()
		bSizer3.Fit( self.panel_Properties )
		bSizer9.Add( self.panel_Properties, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel10.SetSizer( bSizer9 )
		self.m_panel10.Layout()
		bSizer9.Fit( self.m_panel10 )
		bSizer8.Add( self.m_panel10, 3, wx.EXPAND |wx.ALL, 2 )

		self.panel_Display = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.panel_OpticalBench = wx.Panel( self.panel_Display, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN|wx.TAB_TRAVERSAL )
		bSizer5.Add( self.panel_OpticalBench, 3, wx.EXPAND |wx.ALL, 2 )

		self.panel_PolarizationEllipse = wx.Panel( self.panel_Display, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5.Add( self.panel_PolarizationEllipse, 1, wx.EXPAND |wx.ALL, 2 )


		self.panel_Display.SetSizer( bSizer5 )
		self.panel_Display.Layout()
		bSizer5.Fit( self.panel_Display )
		bSizer8.Add( self.panel_Display, 2, wx.EXPAND |wx.ALL, 2 )

		self.panel_Controls = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		choice_ComponentsChoices = []
		self.choice_Components = wx.Choice( self.panel_Controls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_ComponentsChoices, 0 )
		self.choice_Components.SetSelection( 0 )
		bSizer4.Add( self.choice_Components, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.button_AddComponent = wx.Button( self.panel_Controls, wx.ID_ANY, u"Add Component", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.button_AddComponent, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.spinButton_Position = wx.SpinButton( self.panel_Controls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.SP_VERTICAL )
		bSizer4.Add( self.spinButton_Position, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_RemoveComponent = wx.Button( self.panel_Controls, wx.ID_ANY, u"Remove Component", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.button_RemoveComponent, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_Analyse = wx.Button( self.panel_Controls, wx.ID_ANY, u"Analyse", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.button_Analyse, 0, wx.ALL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_ResetView = wx.Button( self.panel_Controls, wx.ID_ANY, u"Reset View", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.button_ResetView, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		self.panel_Controls.SetSizer( bSizer4 )
		self.panel_Controls.Layout()
		bSizer4.Fit( self.panel_Controls )
		bSizer8.Add( self.panel_Controls, 0, wx.ALL|wx.EXPAND, 2 )


		self.m_panel6.SetSizer( bSizer8 )
		self.m_panel6.Layout()
		bSizer8.Fit( self.m_panel6 )
		sizer_Top.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( sizer_Top )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 4, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.mainFrame_OnClose )
		self.Bind( wx.EVT_SIZE, self.mainFrame_OnSize )
		self.Bind( wx.EVT_MENU, self.button_NewProject_OnClick, id = self.newProject.GetId() )
		self.Bind( wx.EVT_MENU, self.button_OpenProject_OnClick, id = self.openProject.GetId() )
		self.Bind( wx.EVT_MENU, self.button_SaveProject_OnClick, id = self.saveProject.GetId() )
		self.Bind( wx.EVT_MENU, self.button_SaveProjectAs_OnClick, id = self.saveProjectAs.GetId() )
		self.Bind( wx.EVT_MENU, self.mainFrame_OnClose, id = self.quit.GetId() )
		self.button_NewProject.Bind( wx.EVT_BUTTON, self.button_NewProject_OnClick )
		self.button_OpenProject.Bind( wx.EVT_BUTTON, self.button_OpenProject_OnClick )
		self.button_SaveProjectAs.Bind( wx.EVT_BUTTON, self.button_SaveProjectAs_OnClick )
		self.button_SaveProject.Bind( wx.EVT_BUTTON, self.button_SaveProject_OnClick )
		self.propertyGrid_Config.Bind( pg.EVT_PG_CHANGED, self.propertyGrid_Config_OnPropertyChanged )
		self.choice_Components.Bind( wx.EVT_CHOICE, self.choice_Components_OnChoice )
		self.button_AddComponent.Bind( wx.EVT_BUTTON, self.button_AddComponent_OnClick )
		self.spinButton_Position.Bind( wx.EVT_SPIN_DOWN, self.spinButton_Position_OnSpinDown )
		self.spinButton_Position.Bind( wx.EVT_SPIN_UP, self.spinButton_Position_OnSpinUp )
		self.button_Analyse.Bind( wx.EVT_BUTTON, self.button_Analyse_OnClick )
		self.button_ResetView.Bind( wx.EVT_BUTTON, self.button_ResetView_OnClick )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def mainFrame_OnClose( self, event ):
		event.Skip()

	def mainFrame_OnSize( self, event ):
		event.Skip()

	def button_NewProject_OnClick( self, event ):
		event.Skip()

	def button_OpenProject_OnClick( self, event ):
		event.Skip()

	def button_SaveProject_OnClick( self, event ):
		event.Skip()

	def button_SaveProjectAs_OnClick( self, event ):
		event.Skip()






	def propertyGrid_Config_OnPropertyChanged( self, event ):
		event.Skip()

	def choice_Components_OnChoice( self, event ):
		event.Skip()

	def button_AddComponent_OnClick( self, event ):
		event.Skip()

	def spinButton_Position_OnSpinDown( self, event ):
		event.Skip()

	def spinButton_Position_OnSpinUp( self, event ):
		event.Skip()

	def button_Analyse_OnClick( self, event ):
		event.Skip()

	def button_ResetView_OnClick( self, event ):
		event.Skip()


