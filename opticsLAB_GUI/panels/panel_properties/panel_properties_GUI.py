# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid

import gettext
_ = gettext.gettext

###########################################################################
## Class panel_properties
###########################################################################

class panel_properties ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 262,459 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer_properties = wx.BoxSizer( wx.VERTICAL )

        self.scrolledWindow_properties = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.scrolledWindow_properties.SetScrollRate( 5, 5 )
        bSizer_prop_properties = wx.BoxSizer( wx.VERTICAL )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.scrolledWindow_properties, wx.ID_ANY, _(u"Property Operations") ), wx.HORIZONTAL )

        self.button_saveTOML = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Save TOML"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.button_saveTOML, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.button_loadTOML = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Load TOML"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.button_loadTOML, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer_prop_properties.Add( sbSizer2, 0, wx.EXPAND, 5 )

        self.m_propertyGrid2 = wx.propgrid.PropertyGrid(self.scrolledWindow_properties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
        bSizer_prop_properties.Add( self.m_propertyGrid2, 1, wx.ALL|wx.EXPAND, 5 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.scrolledWindow_properties, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )

        self.button_prop_apply = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Apply Changes"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer1.Add( self.button_prop_apply, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

        self.button_prop_reset = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, _(u"Reset"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer1.Add( self.button_prop_reset, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


        bSizer_prop_properties.Add( sbSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.scrolledWindow_properties.SetSizer( bSizer_prop_properties )
        self.scrolledWindow_properties.Layout()
        bSizer_prop_properties.Fit( self.scrolledWindow_properties )
        bSizer_properties.Add( self.scrolledWindow_properties, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer_properties )
        self.Layout()

        # Connect Events
        self.button_saveTOML.Bind( wx.EVT_BUTTON, self.button_saveTOMLOnButtonClick )
        self.button_prop_apply.Bind( wx.EVT_BUTTON, self.button_prop_applyOnButtonClick )
        self.button_prop_reset.Bind( wx.EVT_BUTTON, self.button_prop_resetOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def button_saveTOMLOnButtonClick( self, event ):
        event.Skip()

    def button_prop_applyOnButtonClick( self, event ):
        event.Skip()

    def button_prop_resetOnButtonClick( self, event ):
        event.Skip()


