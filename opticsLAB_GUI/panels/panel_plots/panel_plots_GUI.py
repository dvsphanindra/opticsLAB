# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer_Plots = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

        self.button_refresh_diagrams = wx.Button( self, wx.ID_ANY, _(u"Refresh"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.button_refresh_diagrams, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL, 5 )

        self.button_savePlot = wx.Button( self, wx.ID_ANY, _(u"Save Plot"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.button_savePlot, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer_Plots.Add( bSizer2, 0, wx.EXPAND, 5 )

        self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_BOTTOM )
        self.panel_SpotDiagram = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.notebook.AddPage( self.panel_SpotDiagram, _(u"Spot Diagram"), True )
        self.panel_RayFanDiagram = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.notebook.AddPage( self.panel_RayFanDiagram, _(u"Ray Fan Diagram"), False )

        bSizer_Plots.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer_Plots )
        self.Layout()

        # Connect Events
        self.button_refresh_diagrams.Bind( wx.EVT_BUTTON, self.button_refresh_diagramsOnButtonClick )
        self.button_savePlot.Bind( wx.EVT_BUTTON, self.button_savePlotOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def button_refresh_diagramsOnButtonClick( self, event ):
        event.Skip()

    def button_savePlotOnButtonClick( self, event ):
        event.Skip()


