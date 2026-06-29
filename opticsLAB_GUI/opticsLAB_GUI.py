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

wx.ID_CLOSEFILE = 6000
wx.ID_VIEWCOMP = 6001
wx.ID_SHOWCOMP = 6002
wx.ID_SHOWPROP = 6003
wx.ID_SHOWPLOTPANEL = 6004
wx.ID_SHOWSIMULATIONPANEL = 6005
wx.ID_FULLSCREEN = 6006
wx.ID_MODE = 6007
wx.ID_SAVELAYOUT = 6008
wx.ID_RESETLAYOUT = 6009
wx.ID_LOADLAYOUT = 6010
wx.ID_UNDOMENU = 6011
wx.ID_REDOMENU = 6012
wx.ID_DESELECTALL = 6013
wx.ID_DOCUMENTATION = 6014
wx.ID_EXAMPLE = 6015
wx.ID_FINDCOMP = 6016

###########################################################################
## Class MyFrame_opticsLAB_GUI
###########################################################################

class MyFrame_opticsLAB_GUI ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 925,628 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar2 = wx.MenuBar( 0 )
        self.menu_File = wx.Menu()
        self.menuItem_new = wx.MenuItem( self.menu_File, wx.ID_NEW, _(u"New"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_new.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NEW_DIR, wx.ART_MENU ) )
        self.menu_File.Append( self.menuItem_new )

        self.menuItem_openFile = wx.MenuItem( self.menu_File, wx.ID_OPEN, _(u"Open File"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_openFile.SetBitmap( wx.Bitmap( u"data/icons/openfile/openfile.ico", wx.BITMAP_TYPE_ANY ) )
        self.menu_File.Append( self.menuItem_openFile )

        self.menuItem_closeFile = wx.MenuItem( self.menu_File, wx.ID_CLOSEFILE, _(u"Close File"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_closeFile.SetBitmap( wx.Bitmap( u"data/icons/closefile/closefile.ico", wx.BITMAP_TYPE_ANY ) )
        self.menu_File.Append( self.menuItem_closeFile )

        self.menuItem_openFolder = wx.MenuItem( self.menu_File, wx.ID_ANY, _(u"Open Folder"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_openFolder.SetBitmap( wx.Bitmap( u"data/icons/openfolder/openfolder.ico", wx.BITMAP_TYPE_ANY ) )
        self.menu_File.Append( self.menuItem_openFolder )

        self.menuItem_closefolder = wx.MenuItem( self.menu_File, wx.ID_ANY, _(u"Close Folder"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_closefolder.SetBitmap( wx.Bitmap( u"data/icons/closefolder/closefolder.ico", wx.BITMAP_TYPE_ANY ) )
        self.menu_File.Append( self.menuItem_closefolder )

        self.menu_recent = wx.Menu()
        self.menu_File.AppendSubMenu( self.menu_recent, _(u"Recent") )

        self.menu_File.AppendSeparator()

        self.menuItem_save = wx.MenuItem( self.menu_File, wx.ID_SAVE, _(u"Save"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_save.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE, wx.ART_MENU ) )
        self.menu_File.Append( self.menuItem_save )

        self.menuItem_saveAs = wx.MenuItem( self.menu_File, wx.ID_SAVE, _(u"Save As"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_saveAs.SetBitmap( wx.Bitmap( u"data/icons/save/saveas.ico", wx.BITMAP_TYPE_ANY ) )
        self.menu_File.Append( self.menuItem_saveAs )

        self.menu_File.AppendSeparator()

        self.menuItem_exit = wx.MenuItem( self.menu_File, wx.ID_EXIT, _(u"Exit"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_exit.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MENU ) )
        self.menu_File.Append( self.menuItem_exit )

        self.m_menubar2.Append( self.menu_File, _(u"File") )

        self.menu_View = wx.Menu()
        self.menuItem_view_components = wx.MenuItem( self.menu_View, wx.ID_VIEWCOMP, _(u"Show Components Panel\tCtrl+1"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_view_components )
        self.menuItem_view_components.Check( True )

        self.menuItem_view_tree = wx.MenuItem( self.menu_View, wx.ID_SHOWCOMP, _(u"Show Components Tree\tCtrl+4"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_view_tree )
        self.menuItem_view_tree.Check( True )

        self.menuItem_view_properties = wx.MenuItem( self.menu_View, wx.ID_SHOWPROP, _(u"Show Properties Panel\tCtrl+2"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_view_properties )
        self.menuItem_view_properties.Check( True )

        self.menuItem_view_plots = wx.MenuItem( self.menu_View, wx.ID_SHOWPLOTPANEL, _(u"Show Plots Panel\tCtrl+3"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_view_plots )
        self.menuItem_view_plots.Check( True )

        self.menuItem_view_simulation = wx.MenuItem( self.menu_View, wx.ID_SHOWSIMULATIONPANEL, _(u"Show Simulation Panel\tCtrl+5"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_view_simulation )
        self.menuItem_view_simulation.Check( True )

        self.menuItem_view_project_tree = wx.MenuItem( self.menu_View, wx.ID_ANY, _(u"Show Project Folder Tree")+ u"\t" + u"Ctrl+6", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_View.Append( self.menuItem_view_project_tree )

        self.menuItem_view_beam_launcher = wx.MenuItem( self.menu_View, wx.ID_ANY, _(u"Show Beam Launcher Panel")+ u"\t" + u"Ctrl+7", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_View.Append( self.menuItem_view_beam_launcher )

        self.menu_View.AppendSeparator()

        self.menuItem_view_fullScreen = wx.MenuItem( self.menu_View, wx.ID_FULLSCREEN, _(u"View Full Screen"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_view_fullScreen )
        self.menuItem_view_fullScreen.Check( True )

        self.menuItem_Mode = wx.MenuItem( self.menu_View, wx.ID_MODE, _(u"Dark Mode / Light Mode"), wx.EmptyString, wx.ITEM_CHECK )
        self.menu_View.Append( self.menuItem_Mode )
        self.menuItem_Mode.Check( True )

        self.menu_View.AppendSeparator()

        self.menuItem_save_Layout = wx.MenuItem( self.menu_View, wx.ID_SAVELAYOUT, _(u"Save Layout"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_View.Append( self.menuItem_save_Layout )

        self.menuItem_reset_Layout1 = wx.MenuItem( self.menu_View, wx.ID_RESETLAYOUT, _(u"Reset Layout"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_View.Append( self.menuItem_reset_Layout1 )

        self.menuItem_Load_Layout = wx.MenuItem( self.menu_View, wx.ID_LOADLAYOUT, _(u"Load Layout"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_View.Append( self.menuItem_Load_Layout )

        self.m_menubar2.Append( self.menu_View, _(u"&View") )

        self.menu_components = wx.Menu()
        self.menu_mirror = wx.Menu()
        self.menuItem_parabolicMirror = wx.MenuItem( self.menu_mirror, wx.ID_ANY, _(u"Parabolic Mirror"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_mirror.Append( self.menuItem_parabolicMirror )

        self.menuItem_sphericalMirror = wx.MenuItem( self.menu_mirror, wx.ID_ANY, _(u"Spherical Mirror"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_mirror.Append( self.menuItem_sphericalMirror )

        self.menu_mirror.AppendSeparator()

        self.menuItem_concaveParaboloid = wx.MenuItem( self.menu_mirror, wx.ID_ANY, _(u"Concave Paraboloid"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_mirror.Append( self.menuItem_concaveParaboloid )

        self.menuItem_convexParaboloid = wx.MenuItem( self.menu_mirror, wx.ID_ANY, _(u"Convex Paraboloid"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_mirror.Append( self.menuItem_convexParaboloid )

        self.menu_mirror.AppendSeparator()

        self.menuItem_parabolicSurface = wx.MenuItem( self.menu_mirror, wx.ID_ANY, _(u"Parabolic Surface"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_mirror.Append( self.menuItem_parabolicSurface )

        self.menuItem_sphericalSurface = wx.MenuItem( self.menu_mirror, wx.ID_ANY, _(u"Spherical Surface"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_mirror.Append( self.menuItem_sphericalSurface )

        self.menu_components.AppendSubMenu( self.menu_mirror, _(u"Mirrors") )

        self.menu_lens = wx.Menu()
        self.menuItem_concaveLens = wx.MenuItem( self.menu_lens, wx.ID_ANY, _(u"Concave Lens"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_lens.Append( self.menuItem_concaveLens )

        self.menuItem_convexLens = wx.MenuItem( self.menu_lens, wx.ID_ANY, _(u"Convex Lens"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_lens.Append( self.menuItem_convexLens )

        self.menu_lens.AppendSeparator()

        self.menuItem_parabolicLens = wx.MenuItem( self.menu_lens, wx.ID_ANY, _(u"Parabolic Lens"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_lens.Append( self.menuItem_parabolicLens )

        self.menuItem_sphericalLens = wx.MenuItem( self.menu_lens, wx.ID_ANY, _(u"Spherical Lens"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_lens.Append( self.menuItem_sphericalLens )

        self.menu_components.AppendSubMenu( self.menu_lens, _(u"Lens") )

        self.menu_detectors = wx.Menu()
        self.menuItem_rectangularScreen = wx.MenuItem( self.menu_detectors, wx.ID_ANY, _(u"Rectangular Screen"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_detectors.Append( self.menuItem_rectangularScreen )

        self.menu_components.AppendSubMenu( self.menu_detectors, _(u"Detectors") )

        self.m_menubar2.Append( self.menu_components, _(u"Components") )

        self.menu_sources = wx.Menu()
        self.menuItem_sourceRay = wx.MenuItem( self.menu_sources, wx.ID_ANY, _(u"Ray"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_sources.Append( self.menuItem_sourceRay )

        self.subMenu_Beams = wx.Menu()
        self.menuItem_CircularBeam = wx.MenuItem( self.subMenu_Beams, wx.ID_ANY, _(u"Circular Beam"), wx.EmptyString, wx.ITEM_NORMAL )
        self.subMenu_Beams.Append( self.menuItem_CircularBeam )

        self.menuItem_rect = wx.MenuItem( self.subMenu_Beams, wx.ID_ANY, _(u"Rectangular Beam"), wx.EmptyString, wx.ITEM_NORMAL )
        self.subMenu_Beams.Append( self.menuItem_rect )

        self.menuItem_randomBeam = wx.MenuItem( self.subMenu_Beams, wx.ID_ANY, _(u"Random Beam"), wx.EmptyString, wx.ITEM_NORMAL )
        self.subMenu_Beams.Append( self.menuItem_randomBeam )

        self.menu_sources.AppendSubMenu( self.subMenu_Beams, _(u"Beams") )

        self.m_menubar2.Append( self.menu_sources, _(u"Sources") )

        self.menu_edit = wx.Menu()
        self.menuItem_undo = wx.MenuItem( self.menu_edit, wx.ID_UNDOMENU, _(u"Undo"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_undo.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_BACK, wx.ART_MENU ) )
        self.menu_edit.Append( self.menuItem_undo )

        self.menuItem_redo = wx.MenuItem( self.menu_edit, wx.ID_REDOMENU, _(u"Redo"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_redo.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_MENU ) )
        self.menu_edit.Append( self.menuItem_redo )

        self.menu_edit.AppendSeparator()

        self.menuItem_selectAll = wx.MenuItem( self.menu_edit, wx.ID_SELECTALL, _(u"Select All"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_edit.Append( self.menuItem_selectAll )

        self.menuItem_deselectAll = wx.MenuItem( self.menu_edit, wx.ID_DESELECTALL, _(u"Deselect All"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_edit.Append( self.menuItem_deselectAll )

        self.menu_edit.AppendSeparator()

        self.m_menubar2.Append( self.menu_edit, _(u"Edit") )

        self.menu_Help = wx.Menu()
        self.menuItem_Documentation = wx.MenuItem( self.menu_Help, wx.ID_DOCUMENTATION, _(u"Documentations"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_Documentation.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP_BOOK, wx.ART_MENU ) )
        self.menu_Help.Append( self.menuItem_Documentation )

        self.menu_Examples = wx.Menu()
        self.menuItem_telescopeexmp = wx.MenuItem( self.menu_Examples, wx.ID_EXAMPLE, _(u"Telescope Example"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_Examples.Append( self.menuItem_telescopeexmp )

        self.menuItem_cooketriplet = wx.MenuItem( self.menu_Examples, wx.ID_ANY, _(u"CookeTriplet"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menu_Examples.Append( self.menuItem_cooketriplet )

        self.menu_Help.AppendSubMenu( self.menu_Examples, _(u"Examples") )

        self.menu_Help.AppendSeparator()

        self.menuItem_find_components = wx.MenuItem( self.menu_Help, wx.ID_FINDCOMP, _(u"Find Components"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_find_components.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_MENU ) )
        self.menu_Help.Append( self.menuItem_find_components )

        self.menuItem_about = wx.MenuItem( self.menu_Help, wx.ID_ABOUT, _(u"&About OpticsLAB"), wx.EmptyString, wx.ITEM_NORMAL )
        self.menuItem_about.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_INFORMATION, wx.ART_MENU ) )
        self.menu_Help.Append( self.menuItem_about )

        self.m_menubar2.Append( self.menu_Help, _(u"&Help") )

        self.SetMenuBar( self.m_menubar2 )

        self.m_toolBar1 = self.CreateToolBar( wx.TB_FLAT|wx.TB_TEXT, wx.ID_ANY )
        self.tool_New = self.m_toolBar1.AddTool( wx.ID_NEW, _(u"New"), wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_save = self.m_toolBar1.AddTool( wx.ID_SAVE, _(u"Save"), wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_Open = self.m_toolBar1.AddTool( wx.ID_OPEN, _(u"Open"), wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.tool_Redo = self.m_toolBar1.AddTool( wx.ID_REDO, _(u"Redo"), wx.ArtProvider.GetBitmap( wx.ART_REDO, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_undo = self.m_toolBar1.AddTool( wx.ID_UNDO, _(u"Undo"), wx.ArtProvider.GetBitmap( wx.ART_UNDO, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_run = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"Run"), wx.ArtProvider.GetBitmap( wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_zoom = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"Zoom"), wx.ArtProvider.GetBitmap( wx.ART_FULL_SCREEN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_clear = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"Clear All"), wx.ArtProvider.GetBitmap( wx.ART_CLOSE, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_find = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"Find"), wx.ArtProvider.GetBitmap( wx.ART_FIND, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_export = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"Export"), wx.ArtProvider.GetBitmap( wx.ART_FIND_AND_REPLACE, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_Screenshot = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"ScreenShot"), wx.ArtProvider.GetBitmap( wx.ART_COPY, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.tool_help = self.m_toolBar1.AddTool( wx.ID_ANY, _(u"Help"), wx.ArtProvider.GetBitmap( wx.ART_QUESTION, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

        self.m_toolBar1.Realize()

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.OnCloseWindow )
        self.Bind( wx.EVT_MENU, self.menuItem_newOnMenuSelection, id = self.menuItem_new.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_openFileOnMenuSelection, id = self.menuItem_openFile.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_closeFileOnMenuSelection, id = self.menuItem_closeFile.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_openFolderOnMenuSelection, id = self.menuItem_openFolder.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_closefolderOnMenuSelection, id = self.menuItem_closefolder.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_saveOnMenuSelection, id = self.menuItem_save.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_saveAsOnMenuSelection, id = self.menuItem_saveAs.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_exitOnMenuSelection, id = self.menuItem_exit.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_componentsOnMenuSelection, id = self.menuItem_view_components.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_treeOnMenuSelection, id = self.menuItem_view_tree.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_propertiesOnMenuSelection, id = self.menuItem_view_properties.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_plotsOnMenuSelection, id = self.menuItem_view_plots.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_simulationOnMenuSelection, id = self.menuItem_view_simulation.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_project_treeOnMenuSelection, id = self.menuItem_view_project_tree.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_beam_launcherOnMenuSelection, id = self.menuItem_view_beam_launcher.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_view_fullScreenOnMenuSelection, id = self.menuItem_view_fullScreen.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_ModeOnMenuSelection, id = self.menuItem_Mode.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_save_LayoutOnMenuSelection, id = self.menuItem_save_Layout.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_reset_Layout1OnMenuSelection, id = self.menuItem_reset_Layout1.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_Load_LayoutOnMenuSelection, id = self.menuItem_Load_Layout.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_parabolicMirrorOnMenuSelection, id = self.menuItem_parabolicMirror.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_sphericalMirrorOnMenuSelection, id = self.menuItem_sphericalMirror.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_concaveParaboloidOnMenuSelection, id = self.menuItem_concaveParaboloid.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_convexParaboloidOnMenuSelection, id = self.menuItem_convexParaboloid.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_parabolicSurfaceOnMenuSelection, id = self.menuItem_parabolicSurface.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_sphericalSurfaceOnMenuSelection, id = self.menuItem_sphericalSurface.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_concaveLensOnMenuSelection, id = self.menuItem_concaveLens.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_convexLensOnMenuSelection, id = self.menuItem_convexLens.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_parabolicLensOnMenuSelection, id = self.menuItem_parabolicLens.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_sphericalLensOnMenuSelection, id = self.menuItem_sphericalLens.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_rectangularScreenOnMenuSelection, id = self.menuItem_rectangularScreen.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_sourceRayOnMenuSelection, id = self.menuItem_sourceRay.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_CircularBeamOnMenuSelection, id = self.menuItem_CircularBeam.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_rectOnMenuSelection, id = self.menuItem_rect.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_randomBeamOnMenuSelection, id = self.menuItem_randomBeam.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_undoOnMenuSelection, id = self.menuItem_undo.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_redoOnMenuSelection, id = self.menuItem_redo.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_selectAllOnMenuSelection, id = self.menuItem_selectAll.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_deselectAllOnMenuSelection, id = self.menuItem_deselectAll.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_DocumentationOnMenuSelection, id = self.menuItem_Documentation.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_telescopeexmpOnMenuSelection, id = self.menuItem_telescopeexmp.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_cooketripletOnMenuSelection, id = self.menuItem_cooketriplet.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_find_componentsOnMenuSelection, id = self.menuItem_find_components.GetId() )
        self.Bind( wx.EVT_MENU, self.menuItem_aboutOnMenuSelection, id = self.menuItem_about.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_NewOnToolClicked, id = self.tool_New.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_saveOnToolClicked, id = self.tool_save.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_OpenOnToolClicked, id = self.tool_Open.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_RedoOnToolClicked, id = self.tool_Redo.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_undoOnToolClicked, id = self.tool_undo.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_runOnToolClicked, id = self.tool_run.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_zoomOnToolClicked, id = self.tool_zoom.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_clearOnToolClicked, id = self.tool_clear.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_findOnToolClicked, id = self.tool_find.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_exportOnToolClicked, id = self.tool_export.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_ScreenshotOnToolClicked, id = self.tool_Screenshot.GetId() )
        self.Bind( wx.EVT_TOOL, self.tool_helpOnToolClicked, id = self.tool_help.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnCloseWindow( self, event ):
        event.Skip()

    def menuItem_newOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_openFileOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_closeFileOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_openFolderOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_closefolderOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_saveOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_saveAsOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_exitOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_componentsOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_treeOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_propertiesOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_plotsOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_simulationOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_project_treeOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_beam_launcherOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_view_fullScreenOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_ModeOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_save_LayoutOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_reset_Layout1OnMenuSelection( self, event ):
        event.Skip()

    def menuItem_Load_LayoutOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_parabolicMirrorOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_sphericalMirrorOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_concaveParaboloidOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_convexParaboloidOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_parabolicSurfaceOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_sphericalSurfaceOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_concaveLensOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_convexLensOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_parabolicLensOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_sphericalLensOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_rectangularScreenOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_sourceRayOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_CircularBeamOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_rectOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_randomBeamOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_undoOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_redoOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_selectAllOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_deselectAllOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_DocumentationOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_telescopeexmpOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_cooketripletOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_find_componentsOnMenuSelection( self, event ):
        event.Skip()

    def menuItem_aboutOnMenuSelection( self, event ):
        event.Skip()

    def tool_NewOnToolClicked( self, event ):
        event.Skip()

    def tool_saveOnToolClicked( self, event ):
        event.Skip()

    def tool_OpenOnToolClicked( self, event ):
        event.Skip()

    def tool_RedoOnToolClicked( self, event ):
        event.Skip()

    def tool_undoOnToolClicked( self, event ):
        event.Skip()

    def tool_runOnToolClicked( self, event ):
        event.Skip()

    def tool_zoomOnToolClicked( self, event ):
        event.Skip()

    def tool_clearOnToolClicked( self, event ):
        event.Skip()

    def tool_findOnToolClicked( self, event ):
        event.Skip()

    def tool_exportOnToolClicked( self, event ):
        event.Skip()

    def tool_ScreenshotOnToolClicked( self, event ):
        event.Skip()

    def tool_helpOnToolClicked( self, event ):
        event.Skip()


