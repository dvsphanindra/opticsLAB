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
## Class MyPanel_tree
###########################################################################

class MyPanel_tree ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 436,262 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        bSizer_components = wx.BoxSizer( wx.HORIZONTAL )

        self.scrollWindow_components = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.scrollWindow_components.SetScrollRate( 5, 5 )
        self.scrollWindow_components.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        bSizer_activeList = wx.StaticBoxSizer( wx.StaticBox( self.scrollWindow_components, wx.ID_ANY, _(u"Active List") ), wx.VERTICAL )

        listBox_lst_componentsChoices = []
        self.listBox_lst_components = wx.ListBox( bSizer_activeList.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, listBox_lst_componentsChoices, 0 )
        bSizer_activeList.Add( self.listBox_lst_components, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button_up = wx.Button( bSizer_activeList.GetStaticBox(), wx.ID_ANY, _(u"▲ Up"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button_up, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

        self.m_button_down = wx.Button( bSizer_activeList.GetStaticBox(), wx.ID_ANY, _(u"▼ Down"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button_down, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


        bSizer_activeList.Add( bSizer3, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( bSizer_activeList.GetStaticBox(), wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )

        self.m_button_remove_component = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Remove Compont"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer3.Add( self.m_button_remove_component, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

        self.m_button_Duplicate_component = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Duplicate Compont"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer3.Add( self.m_button_Duplicate_component, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


        bSizer_activeList.Add( sbSizer3, 0, wx.EXPAND, 5 )


        self.scrollWindow_components.SetSizer( bSizer_activeList )
        self.scrollWindow_components.Layout()
        bSizer_activeList.Fit( self.scrollWindow_components )
        bSizer_components.Add( self.scrollWindow_components, 1, wx.ALL|wx.EXPAND, 10 )


        self.SetSizer( bSizer_components )
        self.Layout()

        # Connect Events
        self.m_button_up.Bind( wx.EVT_BUTTON, self.m_button_upOnButtonClick )
        self.m_button_down.Bind( wx.EVT_BUTTON, self.m_button_downOnButtonClick )
        self.m_button_remove_component.Bind( wx.EVT_BUTTON, self.m_button_remove_componentOnButtonClick )
        self.m_button_Duplicate_component.Bind( wx.EVT_BUTTON, self.m_button_Duplicate_componentOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_button_upOnButtonClick( self, event ):
        event.Skip()

    def m_button_downOnButtonClick( self, event ):
        event.Skip()

    def m_button_remove_componentOnButtonClick( self, event ):
        event.Skip()

    def m_button_Duplicate_componentOnButtonClick( self, event ):
        event.Skip()


