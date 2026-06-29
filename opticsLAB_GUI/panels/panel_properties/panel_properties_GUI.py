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

        self.m_propertyGrid2 = wx.propgrid.PropertyGrid(self.scrolledWindow_properties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
        bSizer_prop_properties.Add( self.m_propertyGrid2, 1, wx.ALL|wx.EXPAND, 5 )


        self.scrolledWindow_properties.SetSizer( bSizer_prop_properties )
        self.scrolledWindow_properties.Layout()
        bSizer_prop_properties.Fit( self.scrolledWindow_properties )
        bSizer_properties.Add( self.scrolledWindow_properties, 1, wx.EXPAND |wx.ALL, 5 )

        self.textCtrl_description = wx.StaticText( self, wx.ID_ANY, _(u"MyLabel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.textCtrl_description.Wrap( -1 )

        bSizer_properties.Add( self.textCtrl_description, 0, wx.ALL|wx.EXPAND, 10 )


        self.SetSizer( bSizer_properties )
        self.Layout()

        # Connect Events
        self.m_propertyGrid2.Bind( wx.propgrid.EVT_PG_CHANGED, self.m_propertyGrid2OnPropertyGridChanged )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_propertyGrid2OnPropertyGridChanged( self, event ):
        event.Skip()


