# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"State of Polarization Visualizer", pos = wx.DefaultPosition, size = wx.Size( 1000,600 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		sizer_Top = wx.BoxSizer( wx.VERTICAL )

		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1000,600 ), wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel10 = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.panel_PoincareSphere = wx.Panel( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9.Add( self.panel_PoincareSphere, 1, wx.EXPAND |wx.ALL, 2 )

		self.panel_PolarizationEllipse = wx.Panel( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9.Add( self.panel_PolarizationEllipse, 1, wx.EXPAND |wx.ALL, 2 )

		self.m_panel61 = wx.Panel( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		checkList_oldValuesChoices = []
		self.checkList_oldValues = wx.CheckListBox( self.m_panel61, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, checkList_oldValuesChoices, wx.LB_ALWAYS_SB|wx.LB_MULTIPLE )
		bSizer6.Add( self.checkList_oldValues, 1, wx.ALL|wx.EXPAND, 2 )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_Remove = wx.Button( self.m_panel61, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.button_Remove, 0, wx.ALL, 5 )

		self.button_Reset = wx.Button( self.m_panel61, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.button_Reset, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer6.Add( bSizer81, 0, wx.EXPAND, 5 )


		self.m_panel61.SetSizer( bSizer6 )
		self.m_panel61.Layout()
		bSizer6.Fit( self.m_panel61 )
		bSizer9.Add( self.m_panel61, 0, wx.ALL|wx.EXPAND, 2 )


		self.m_panel10.SetSizer( bSizer9 )
		self.m_panel10.Layout()
		bSizer9.Fit( self.m_panel10 )
		bSizer8.Add( self.m_panel10, 3, wx.EXPAND |wx.ALL, 2 )

		self.panel_Controls = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText51 = wx.StaticText( self.panel_Controls, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		bSizer4.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_Name = wx.TextCtrl( self.panel_Controls, wx.ID_ANY, u"SoP1", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.textCtrl_Name, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText2 = wx.StaticText( self.panel_Controls, wx.ID_ANY, u"I:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer4.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_I = wx.TextCtrl( self.panel_Controls, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.textCtrl_I, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText3 = wx.StaticText( self.panel_Controls, wx.ID_ANY, u"Q:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_Q = wx.TextCtrl( self.panel_Controls, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.textCtrl_Q, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText4 = wx.StaticText( self.panel_Controls, wx.ID_ANY, u"U:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer4.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_U = wx.TextCtrl( self.panel_Controls, wx.ID_ANY, u"0.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.textCtrl_U, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText5 = wx.StaticText( self.panel_Controls, wx.ID_ANY, u"V:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer4.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_V = wx.TextCtrl( self.panel_Controls, wx.ID_ANY, u"0.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer4.Add( self.textCtrl_V, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.colourPicker_color = wx.ColourPickerCtrl( self.panel_Controls, wx.ID_ANY, wx.Colour( 255, 255, 255 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE|wx.CLRP_SHOW_LABEL )
		bSizer4.Add( self.colourPicker_color, 0, wx.ALL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer7.Add( bSizer4, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_Show = wx.Button( self.panel_Controls, wx.ID_ANY, u"Show", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.button_Show, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer7.Add( bSizer10, 1, wx.EXPAND, 5 )


		self.panel_Controls.SetSizer( bSizer7 )
		self.panel_Controls.Layout()
		bSizer7.Fit( self.panel_Controls )
		bSizer8.Add( self.panel_Controls, 0, wx.ALL|wx.EXPAND, 2 )


		self.m_panel6.SetSizer( bSizer8 )
		self.m_panel6.Layout()
		sizer_Top.Add( self.m_panel6, 0, wx.ALL, 2 )


		self.SetSizer( sizer_Top )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 4, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.mainFrame_OnClose )
		self.Bind( wx.EVT_SIZE, self.mainFrame_OnSize )
		self.checkList_oldValues.Bind( wx.EVT_LISTBOX_DCLICK, self.checkList_oldValues_OnCheckListBoxDClick )
		self.checkList_oldValues.Bind( wx.EVT_CHECKLISTBOX, self.checkList_oldValues_OnCheckListBoxToggled )
		self.button_Remove.Bind( wx.EVT_BUTTON, self.button_Remove_OnButtonClick )
		self.button_Reset.Bind( wx.EVT_BUTTON, self.button_Reset_OnClick )
		self.textCtrl_Name.Bind( wx.EVT_TEXT_ENTER, self.button_Show_OnClick )
		self.textCtrl_I.Bind( wx.EVT_TEXT_ENTER, self.button_Show_OnClick )
		self.textCtrl_Q.Bind( wx.EVT_TEXT_ENTER, self.button_Show_OnClick )
		self.textCtrl_U.Bind( wx.EVT_TEXT_ENTER, self.button_Show_OnClick )
		self.textCtrl_V.Bind( wx.EVT_TEXT_ENTER, self.button_Show_OnClick )
		self.colourPicker_color.Bind( wx.EVT_COLOURPICKER_CHANGED, self.colourPicker_color_OnColourChanged )
		self.button_Show.Bind( wx.EVT_BUTTON, self.button_Show_OnClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def mainFrame_OnClose( self, event ):
		event.Skip()

	def mainFrame_OnSize( self, event ):
		event.Skip()

	def checkList_oldValues_OnCheckListBoxDClick( self, event ):
		event.Skip()

	def checkList_oldValues_OnCheckListBoxToggled( self, event ):
		event.Skip()

	def button_Remove_OnButtonClick( self, event ):
		event.Skip()

	def button_Reset_OnClick( self, event ):
		event.Skip()

	def button_Show_OnClick( self, event ):
		event.Skip()





	def colourPicker_color_OnColourChanged( self, event ):
		event.Skip()



