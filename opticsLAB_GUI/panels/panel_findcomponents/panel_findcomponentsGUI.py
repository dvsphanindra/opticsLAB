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
## Class MyDialog_search_components_GUI
###########################################################################

class MyDialog_search_components_GUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Find / Search Components"), pos = wx.DefaultPosition, size = wx.Size( 405,361 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer_main = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText_label = wx.StaticText( self, wx.ID_ANY, _(u"Type to search component or preset in real-time:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_label.Wrap( -1 )

        bSizer_main.Add( self.m_staticText_label, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER|wx.ALIGN_TOP|wx.ALL|wx.TOP, 10 )

        self.m_searchCtrl1 = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_searchCtrl1.ShowSearchButton( True )
        self.m_searchCtrl1.ShowCancelButton( False )
        bSizer_main.Add( self.m_searchCtrl1, 0, wx.ALL|wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 10 )

        m_listBox1Choices = []
        self.m_listBox1 = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox1Choices, 0 )
        bSizer_main.Add( self.m_listBox1, 1, wx.ALL|wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.RIGHT, 5 )

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
        m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
        self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
        m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
        m_sdbSizer1.Realize()

        bSizer_main.Add( m_sdbSizer1, 0, wx.EXPAND, 10 )


        self.SetSizer( bSizer_main )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_searchCtrl1.Bind( wx.EVT_TEXT, self.m_searchCtrl1OnText )
        self.m_listBox1.Bind( wx.EVT_LISTBOX_DCLICK, self.m_listBox1OnListBoxDClick )
        self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer1OKOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_searchCtrl1OnText( self, event ):
        event.Skip()

    def m_listBox1OnListBoxDClick( self, event ):
        event.Skip()

    def m_sdbSizer1OKOnButtonClick( self, event ):
        event.Skip()


