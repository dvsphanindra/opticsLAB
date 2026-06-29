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
## Class MyPanel_panel_components_tree
###########################################################################

class MyPanel_panel_components_tree ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 312,322 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.SetMinSize( wx.Size( 312,-1 ) )

        bSizer_components = wx.BoxSizer( wx.VERTICAL )

        self.treeCtrl_projectComponents = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        bSizer_components.Add( self.treeCtrl_projectComponents, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer_components )
        self.Layout()

        # Connect Events
        self.treeCtrl_projectComponents.Bind( wx.EVT_TREE_SEL_CHANGED, self.m_treeCtrl1OnTreeSelChanged )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_treeCtrl1OnTreeSelChanged( self, event ):
        event.Skip()


