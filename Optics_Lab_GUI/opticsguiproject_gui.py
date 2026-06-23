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

ID_OPEN_PROJECT = 6000
ID_SAVE_PROJECT = 6001
ID_QUIT = 6002
ID_CONCAVE_LENS = 6003
ID_CONVEX_LENS = 6004
ID_PARABOLIC_MIRROR = 6005
ID_SPHERICAL_MIRROR = 6006
ID_SPOT_DIAGRAM = 6007
ID_RAY_FAN_DIAGRAM = 6008
ID_ABOUT = 6009

###########################################################################
## Class MainFrameBase
###########################################################################

class MainFrameBase ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Optics Lab - wxPython Interactive GUI"), pos = wx.DefaultPosition, size = wx.Size( 1229,772 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        self.left_sidebar = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.left_sidebar.SetScrollRate( 5, 5 )
        self.left_sidebar.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self.left_sidebar, wx.ID_ANY, _(u"Components") ), wx.VERTICAL )

        self.m_staticText3 = wx.StaticText( sbSizer7.GetStaticBox(), wx.ID_ANY, _(u"Add New Component"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        self.m_staticText3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
        self.m_staticText3.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        sbSizer7.Add( self.m_staticText3, 1, wx.ALL, 5 )

        m_comboBox1Choices = [ _(u"Spherical Lens"), _(u"Parabolic Lens"), _(u"Concave Paraboloid"), _(u"Convex Paraboloid"), _(u"Parabolic Surface"), _(u"Spherical Surface") ]
        self.m_comboBox1 = wx.ComboBox( sbSizer7.GetStaticBox(), wx.ID_ANY, _(u"Parabolic Lens"), wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
        self.m_comboBox1.SetSelection( 1 )
        sbSizer7.Add( self.m_comboBox1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button_add_component = wx.Button( sbSizer7.GetStaticBox(), wx.ID_ANY, _(u"+ Add Component"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer7.Add( self.m_button_add_component, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_treeCtrl1 = wx.TreeCtrl( sbSizer7.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        sbSizer7.Add( self.m_treeCtrl1, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer2.Add( sbSizer7, 1, wx.EXPAND, 5 )

        sbSizer9 = wx.StaticBoxSizer( wx.StaticBox( self.left_sidebar, wx.ID_ANY, _(u"Active List") ), wx.VERTICAL )

        self.m_staticText4 = wx.StaticText( sbSizer9.GetStaticBox(), wx.ID_ANY, _(u"Active List"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        sbSizer9.Add( self.m_staticText4, 0, wx.ALL, 5 )

        m_listBox_lst_componentsChoices = []
        self.m_listBox_lst_components = wx.ListBox( sbSizer9.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_lst_componentsChoices, 0 )
        sbSizer9.Add( self.m_listBox_lst_components, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button_up = wx.Button( sbSizer9.GetStaticBox(), wx.ID_ANY, _(u"▲ Up"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button_up, 0, wx.ALL, 5 )

        self.m_button_down = wx.Button( sbSizer9.GetStaticBox(), wx.ID_ANY, _(u"▼ Down"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button_down, 0, wx.ALL, 5 )

        self.m_button_remove = wx.Button( sbSizer9.GetStaticBox(), wx.ID_ANY, _(u"✖ Remove"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button_remove.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

        bSizer3.Add( self.m_button_remove, 0, wx.ALL, 5 )


        sbSizer9.Add( bSizer3, 1, wx.EXPAND, 5 )

        self.m_gauge_graph_loading = wx.Gauge( sbSizer9.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge_graph_loading.SetValue( 0 )
        sbSizer9.Add( self.m_gauge_graph_loading, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer2.Add( sbSizer9, 1, wx.EXPAND, 5 )

        sbSizer10 = wx.StaticBoxSizer( wx.StaticBox( self.left_sidebar, wx.ID_ANY, _(u"Lens Design Examples") ), wx.VERTICAL )

        m_listBox2Choices = []
        self.m_listBox2 = wx.ListBox( sbSizer10.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox2Choices, wx.LB_MULTIPLE )
        sbSizer10.Add( self.m_listBox2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button_add_py_eg = wx.Button( sbSizer10.GetStaticBox(), wx.ID_ANY, _(u"📂 Add Python Example File"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer10.Add( self.m_button_add_py_eg, 0, wx.ALL, 5 )


        bSizer2.Add( sbSizer10, 1, wx.EXPAND, 5 )


        self.left_sidebar.SetSizer( bSizer2 )
        self.left_sidebar.Layout()
        bSizer2.Fit( self.left_sidebar )
        bSizer1.Add( self.left_sidebar, 1, wx.EXPAND |wx.ALL, 10 )

        self.m_panel_middle_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer_Middle_panel = wx.BoxSizer( wx.VERTICAL )

        sbSizer_graph1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_middle_panel, wx.ID_ANY, _(u"Optical Simulation") ), wx.VERTICAL )

        self.m_panel_canvas_placeholder = wx.Panel( sbSizer_graph1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sbSizer_graph1.Add( self.m_panel_canvas_placeholder, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer_Middle_panel.Add( sbSizer_graph1, 1, wx.EXPAND, 5 )

        sbSizerGraph2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_middle_panel, wx.ID_ANY, _(u"2nd Graph") ), wx.VERTICAL )

        self.notebook = wx.Notebook( sbSizerGraph2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_BOTTOM )
        self.panel_SpotDiagram = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.notebook.AddPage( self.panel_SpotDiagram, _(u"Spot Diagram"), True )
        self.panel_RayFanDiagram = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.notebook.AddPage( self.panel_RayFanDiagram, _(u"Ray Fan Diagram"), False )

        sbSizerGraph2.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )


        bSizer_Middle_panel.Add( sbSizerGraph2, 1, wx.EXPAND, 5 )


        self.m_panel_middle_panel.SetSizer( bSizer_Middle_panel )
        self.m_panel_middle_panel.Layout()
        bSizer_Middle_panel.Fit( self.m_panel_middle_panel )
        bSizer1.Add( self.m_panel_middle_panel, 1, wx.ALL|wx.BOTTOM|wx.EXPAND|wx.TOP, 5 )

        self.m_scrolledWindow_right_editor = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow_right_editor.SetScrollRate( 5, 5 )
        sbSizer14 = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledWindow_right_editor, wx.ID_ANY, _(u"Parameters of Selected Lens") ), wx.VERTICAL )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button_btn_load_toml = wx.Button( sbSizer14.GetStaticBox(), wx.ID_ANY, _(u" 📂 Load TOML"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button_btn_load_toml, 0, wx.ALL, 5 )

        self.m_button_btn_save_toml = wx.Button( sbSizer14.GetStaticBox(), wx.ID_ANY, _(u"💾 Save TOML"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button_btn_save_toml, 0, wx.ALL, 5 )


        bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )


        sbSizer14.Add( bSizer5, 0, wx.EXPAND, 5 )

        self.propertyGrid_Properties = wx.propgrid.PropertyGrid(sbSizer14.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
        sbSizer14.Add( self.propertyGrid_Properties, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_scrolledWindow_right_editor.SetSizer( sbSizer14 )
        self.m_scrolledWindow_right_editor.Layout()
        sbSizer14.Fit( self.m_scrolledWindow_right_editor )
        bSizer1.Add( self.m_scrolledWindow_right_editor, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        self.menubar = wx.MenuBar( 0 )
        self.file = wx.Menu()
        self.openProject = wx.MenuItem( self.file, ID_OPEN_PROJECT, _(u"Open Project"), wx.EmptyString, wx.ITEM_NORMAL )
        self.file.Append( self.openProject )

        self.saveProject = wx.MenuItem( self.file, ID_SAVE_PROJECT, _(u"Save Project"), wx.EmptyString, wx.ITEM_NORMAL )
        self.file.Append( self.saveProject )

        self.file.AppendSeparator()

        self.quit = wx.MenuItem( self.file, ID_QUIT, _(u"Quit"), wx.EmptyString, wx.ITEM_NORMAL )
        self.file.Append( self.quit )

        self.menubar.Append( self.file, _(u"File") )

        self.lens = wx.Menu()
        self.concaveLens = wx.MenuItem( self.lens, ID_CONCAVE_LENS, _(u"Concave Lens"), wx.EmptyString, wx.ITEM_NORMAL )
        self.lens.Append( self.concaveLens )

        self.convexLens = wx.MenuItem( self.lens, ID_CONVEX_LENS, _(u"Convex Lens"), wx.EmptyString, wx.ITEM_NORMAL )
        self.lens.Append( self.convexLens )

        self.menubar.Append( self.lens, _(u"Lens") )

        self.mirror = wx.Menu()
        self.parabolicMirror = wx.MenuItem( self.mirror, ID_PARABOLIC_MIRROR, _(u"Parabolic Mirror"), wx.EmptyString, wx.ITEM_NORMAL )
        self.mirror.Append( self.parabolicMirror )

        self.sphericalMirror = wx.MenuItem( self.mirror, ID_SPHERICAL_MIRROR, _(u"Spherical Mirror"), wx.EmptyString, wx.ITEM_NORMAL )
        self.mirror.Append( self.sphericalMirror )

        self.menubar.Append( self.mirror, _(u"Mirror") )

        self.plots = wx.Menu()
        self.spotDiagram = wx.MenuItem( self.plots, ID_SPOT_DIAGRAM, _(u"Spot Diagram"), wx.EmptyString, wx.ITEM_NORMAL )
        self.plots.Append( self.spotDiagram )

        self.rayFanDiagram = wx.MenuItem( self.plots, ID_RAY_FAN_DIAGRAM, _(u"Ray Fan Diagram"), wx.EmptyString, wx.ITEM_NORMAL )
        self.plots.Append( self.rayFanDiagram )

        self.menubar.Append( self.plots, _(u"Plots") )

        self.help = wx.Menu()
        self.about = wx.MenuItem( self.help, ID_ABOUT, _(u"About"), wx.EmptyString, wx.ITEM_NORMAL )
        self.help.Append( self.about )

        self.menubar.Append( self.help, _(u"Help") )

        self.SetMenuBar( self.menubar )

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
        self.m_toolBar1.Realize()


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button_add_component.Bind( wx.EVT_BUTTON, self.m_button_add_componentOnButtonClick )
        self.m_treeCtrl1.Bind( wx.EVT_TREE_SEL_CHANGED, self.m_treeCtrl1OnTreeSelChanged )
        self.m_button_up.Bind( wx.EVT_BUTTON, self.m_button_upOnButtonClick )
        self.m_button_down.Bind( wx.EVT_BUTTON, self.m_button_downOnButtonClick )
        self.m_button_remove.Bind( wx.EVT_BUTTON, self.m_button_removeOnButtonClick )
        self.m_button_add_py_eg.Bind( wx.EVT_BUTTON, self.m_button_add_py_egOnButtonClick )
        self.m_button_btn_load_toml.Bind( wx.EVT_BUTTON, self.m_button_btn_load_tomlOnButtonClick )
        self.m_button_btn_save_toml.Bind( wx.EVT_BUTTON, self.m_button_btn_save_tomlOnButtonClick )
        self.Bind( wx.EVT_MENU, self.openProjectOnMenuSelection, id = self.openProject.GetId() )
        self.Bind( wx.EVT_MENU, self.saveProjectOnMenuSelection, id = self.saveProject.GetId() )
        self.Bind( wx.EVT_MENU, self.quitOnMenuSelection, id = self.quit.GetId() )
        self.Bind( wx.EVT_MENU, self.concaveLensOnMenuSelection, id = self.concaveLens.GetId() )
        self.Bind( wx.EVT_MENU, self.convexLensOnMenuSelection, id = self.convexLens.GetId() )
        self.Bind( wx.EVT_MENU, self.parabolicMirrorOnMenuSelection, id = self.parabolicMirror.GetId() )
        self.Bind( wx.EVT_MENU, self.sphericalMirrorOnMenuSelection, id = self.sphericalMirror.GetId() )
        self.Bind( wx.EVT_MENU, self.spotDiagramOnMenuSelection, id = self.spotDiagram.GetId() )
        self.Bind( wx.EVT_MENU, self.rayFanDiagramOnMenuSelection, id = self.rayFanDiagram.GetId() )
        self.Bind( wx.EVT_MENU, self.aboutOnMenuSelection, id = self.about.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_button_add_componentOnButtonClick( self, event ):
        event.Skip()

    def m_treeCtrl1OnTreeSelChanged( self, event ):
        event.Skip()

    def m_button_upOnButtonClick( self, event ):
        event.Skip()

    def m_button_downOnButtonClick( self, event ):
        event.Skip()

    def m_button_removeOnButtonClick( self, event ):
        event.Skip()

    def m_button_add_py_egOnButtonClick( self, event ):
        event.Skip()

    def m_button_btn_load_tomlOnButtonClick( self, event ):
        event.Skip()

    def m_button_btn_save_tomlOnButtonClick( self, event ):
        event.Skip()

    def openProjectOnMenuSelection( self, event ):
        event.Skip()

    def saveProjectOnMenuSelection( self, event ):
        event.Skip()

    def quitOnMenuSelection( self, event ):
        event.Skip()

    def concaveLensOnMenuSelection( self, event ):
        event.Skip()

    def convexLensOnMenuSelection( self, event ):
        event.Skip()

    def parabolicMirrorOnMenuSelection( self, event ):
        event.Skip()

    def sphericalMirrorOnMenuSelection( self, event ):
        event.Skip()

    def spotDiagramOnMenuSelection( self, event ):
        event.Skip()

    def rayFanDiagramOnMenuSelection( self, event ):
        event.Skip()

    def aboutOnMenuSelection( self, event ):
        event.Skip()


