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

        self.staticText_projectDirectory = wx.StaticText( self, wx.ID_ANY, _(u"Project Directory"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.staticText_projectDirectory.Wrap( -1 )

        bSizer_components.Add( self.staticText_projectDirectory, 0, wx.ALL, 5 )

        self.treeCtrl_projectDirectory = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        bSizer_components.Add( self.treeCtrl_projectDirectory, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer_components )
        self.Layout()

        # Connect Events
        self.treeCtrl_projectDirectory.Bind( wx.EVT_TREE_SEL_CHANGED, self.treeCtrl_projectDirectoryOnTreeSelChanged )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def treeCtrl_projectDirectoryOnTreeSelChanged( self, event ):
        event.Skip()


