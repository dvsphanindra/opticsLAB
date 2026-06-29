# -*- coding: utf-8 -*-
"""
Generated GUI class for BeamLauncher panel.
"""

import wx
import wx.xrc
import wx.dataview
import gettext
_ = gettext.gettext


class panel_BeamLauncher_GUI(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(702, 583), style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        self.m_splitter1 = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)
        self.m_splitter1.Bind(wx.EVT_IDLE, self.m_splitter1OnIdle)

        self.panel_BeamLauncherControls = wx.Panel(self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_STATIC | wx.TAB_TRAVERSAL)
        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText1 = wx.StaticText(self.panel_BeamLauncherControls, wx.ID_ANY, _("Select Beam Type:"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.choice_BeamLauncherType = wx.Choice(self.panel_BeamLauncherControls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [_("Single Ray"), _("Circular"), _("Rectangle"), _("Random")], 0)
        self.choice_BeamLauncherType.SetSelection(0)
        bSizer7.Add(self.choice_BeamLauncherType, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        bSizer4.Add(bSizer7, 0, wx.EXPAND, 5)

        self.panel_RayCount = wx.Panel(self.panel_BeamLauncherControls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL)
        self.panel_RayCount.Enable(False)
        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText11 = wx.StaticText(self.panel_RayCount, wx.ID_ANY, _("No of Rays:"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_staticText11, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.textCtrl_Ray_Count = wx.TextCtrl(self.panel_RayCount, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), wx.TE_PROCESS_ENTER)
        self.textCtrl_Ray_Count.SetMaxSize(wx.Size(50, -1))
        bSizer8.Add(self.textCtrl_Ray_Count, 0, wx.ALL, 5)
        self.m_staticText12 = wx.StaticText(self.panel_RayCount, wx.ID_ANY, _("Separation:"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_textCtrl8 = wx.TextCtrl(self.panel_RayCount, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), 0)
        self.m_textCtrl8.SetMaxSize(wx.Size(50, -1))
        bSizer8.Add(self.m_textCtrl8, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.panel_RayCount.SetSizer(bSizer8)
        self.panel_RayCount.Layout()
        bSizer4.Add(self.panel_RayCount, 0, wx.EXPAND | wx.ALL, 5)

        bSizer15 = wx.BoxSizer(wx.HORIZONTAL)
        self.staticText_wavelength_beam = wx.StaticText(self.panel_BeamLauncherControls, wx.ID_ANY, _("Wavelength   :"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer15.Add(self.staticText_wavelength_beam, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.textCtrl_wavelength = wx.TextCtrl(self.panel_BeamLauncherControls, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        bSizer15.Add(self.textCtrl_wavelength, 1, wx.ALL, 5)
        bSizer4.Add(bSizer15, 0, wx.EXPAND, 5)

        self.panel_Circle_Radius_Beam = wx.Panel(self.panel_BeamLauncherControls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL)
        bSizer82 = wx.BoxSizer(wx.HORIZONTAL)
        self.m_staticText_circle_beam = wx.StaticText(self.panel_Circle_Radius_Beam, wx.ID_ANY, _("Radius    :"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer82.Add(self.m_staticText_circle_beam, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.textCtrl_Ray_Count1 = wx.TextCtrl(self.panel_Circle_Radius_Beam, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), wx.TE_PROCESS_ENTER)
        self.textCtrl_Ray_Count1.SetMaxSize(wx.Size(50, -1))
        bSizer82.Add(self.textCtrl_Ray_Count1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.panel_Circle_Radius_Beam.SetSizer(bSizer82)
        self.panel_Circle_Radius_Beam.Layout()
        bSizer4.Add(self.panel_Circle_Radius_Beam, 0, wx.EXPAND | wx.ALL, 5)

        self.panel_Rectangle_beam = wx.Panel(self.panel_BeamLauncherControls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE | wx.TAB_TRAVERSAL)
        self.panel_Rectangle_beam.Hide()
        bSizer821 = wx.BoxSizer(wx.HORIZONTAL)
        self.staticText_rectangle_beam = wx.StaticText(self.panel_Rectangle_beam, wx.ID_ANY, _("Length :"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer821.Add(self.staticText_rectangle_beam, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.textCtrl_rectangle_length = wx.TextCtrl(self.panel_Rectangle_beam, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), wx.TE_PROCESS_ENTER)
        self.textCtrl_rectangle_length.SetMaxSize(wx.Size(50, -1))
        bSizer821.Add(self.textCtrl_rectangle_length, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.staticText_rectangle_beam_breath = wx.StaticText(self.panel_Rectangle_beam, wx.ID_ANY, _("Breath  :"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer821.Add(self.staticText_rectangle_beam_breath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.textCtrl_rectangle_breath = wx.TextCtrl(self.panel_Rectangle_beam, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1), wx.TE_PROCESS_ENTER)
        self.textCtrl_rectangle_breath.SetMaxSize(wx.Size(50, -1))
        bSizer821.Add(self.textCtrl_rectangle_breath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.panel_Rectangle_beam.SetSizer(bSizer821)
        self.panel_Rectangle_beam.Layout()
        bSizer4.Add(self.panel_Rectangle_beam, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panel5 = wx.Panel(self.panel_BeamLauncherControls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN | wx.TAB_TRAVERSAL)
        bSizer9 = wx.BoxSizer(wx.VERTICAL)
        bSizer81 = wx.BoxSizer(wx.HORIZONTAL)
        self.staticText_beamDirection = wx.StaticText(self.m_panel5, wx.ID_ANY, _("Beam Directioin    :"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer81.Add(self.staticText_beamDirection, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.choice_DirectionRays = wx.Choice(self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.Size(150, -1), [_("X_AXIS_DIRECTION"), _("Y_AXIS_DIRECTION"), _("Z_AXIS_DIRECTION"), _("X_AXIS_NEG_DIRECTION"), _("Y_AXIS_NEG_DIRECTION"), _("Z_AXIS_NEG_DIRECTION")], 0)
        self.choice_DirectionRays.SetSelection(2)
        bSizer81.Add(self.choice_DirectionRays, 0, wx.ALL, 5)
        bSizer9.Add(bSizer81, 0, wx.EXPAND, 5)

        fgSizer1 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer1.Add((0, 0), 1, wx.EXPAND, 5)
        for t in ["X", "Y", "Z"]:
            st = wx.StaticText(self.m_panel5, wx.ID_ANY, _(t))
            fgSizer1.Add(st, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        st_c = wx.StaticText(self.m_panel5, wx.ID_ANY, _("Center :"))
        st_c.SetToolTip(_("Enter the centre positon of the Beam"))
        fgSizer1.Add(st_c, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.textCtrl_XPosition = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.textCtrl_YPosition = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.textCtrl_ZPosition = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        for ctrl in (self.textCtrl_XPosition, self.textCtrl_YPosition, self.textCtrl_ZPosition):
            ctrl.SetMaxSize(wx.Size(40, -1))
            fgSizer1.Add(ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.checkBox_Degrees = wx.CheckBox(self.m_panel5, wx.ID_ANY, _("Degrees"), wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.checkBox_Degrees, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        for t in ["X Angle", "Y Angle", "Z Angle"]:
            fgSizer1.Add(wx.StaticText(self.m_panel5, wx.ID_ANY, _(t)), 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer1.Add(wx.StaticText(self.m_panel5, wx.ID_ANY, _("Angles:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        self.textCtrl_XAngle = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("90"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.textCtrl_YAngle = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("90"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.textCtrl_ZAngle = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        for ctrl in (self.textCtrl_XAngle, self.textCtrl_YAngle, self.textCtrl_ZAngle):
            ctrl.SetMaxSize(wx.Size(40, -1))
            fgSizer1.Add(ctrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer1.Add((0, 0), 1, wx.EXPAND, 5)
        for t in ["l", "m", "n"]:
            fgSizer1.Add(wx.StaticText(self.m_panel5, wx.ID_ANY, _(t)), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer1.Add(wx.StaticText(self.m_panel5, wx.ID_ANY, _("DC:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
        self.textCtrl_DC_l = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.textCtrl_DC_m = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("0"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.textCtrl_DC_n = wx.TextCtrl(self.m_panel5, wx.ID_ANY, _("1"), wx.DefaultPosition, wx.Size(40, -1), wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        for ctrl in (self.textCtrl_DC_l, self.textCtrl_DC_m, self.textCtrl_DC_n):
            ctrl.SetMaxSize(wx.Size(40, -1))
            fgSizer1.Add(ctrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer9.Add(fgSizer1, 1, wx.EXPAND, 5)
        self.m_panel5.SetSizer(bSizer9)
        self.m_panel5.Layout()
        bSizer4.Add(self.m_panel5, 0, wx.EXPAND | wx.ALL, 5)

        bSizer11 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer11.Add(wx.StaticText(self.panel_BeamLauncherControls, wx.ID_ANY, _("Select Color:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.textCtrl_Color = wx.TextCtrl(self.panel_BeamLauncherControls, wx.ID_ANY, wx.EmptyString)
        bSizer11.Add(self.textCtrl_Color, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        self.button_SelectColor = wx.Button(self.panel_BeamLauncherControls, wx.ID_ANY, _("..."), style=wx.BU_EXACTFIT)
        bSizer11.Add(self.button_SelectColor, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        bSizer4.Add(bSizer11, 0, wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer10.Add(wx.StaticText(self.panel_BeamLauncherControls, wx.ID_ANY, _("Total No of Rays:")), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.staticText_RayCount = wx.StaticText(self.panel_BeamLauncherControls, wx.ID_ANY, _("     0       "))
        bSizer10.Add(self.staticText_RayCount, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        bSizer4.Add(bSizer10, 0, wx.EXPAND, 5)

        self.m_scrolledWindow1 = wx.ScrolledWindow(self.panel_BeamLauncherControls, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.m_scrolledWindow1.SetScrollRate(5, 5)
        bSizer17 = wx.BoxSizer(wx.VERTICAL)
        self.dataViewListCtrl_ActiveBeamList = wx.dataview.DataViewListCtrl(self.m_scrolledWindow1, wx.ID_ANY, style=wx.dataview.DV_NO_HEADER | wx.dataview.DV_ROW_LINES | wx.BORDER_SUNKEN)
        bSizer17.Add(self.dataViewListCtrl_ActiveBeamList, 0, wx.ALL | wx.EXPAND, 5)

        bSizer18 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_Addbeam = wx.Button(self.m_scrolledWindow1, wx.ID_ANY, _("Add"))
        self.button_remove_List_Beam = wx.Button(self.m_scrolledWindow1, wx.ID_ANY, _("Remove"))
        self.button_simulateBeam = wx.Button(self.m_scrolledWindow1, wx.ID_ANY, _("Simulate"))
        for btn in (self.button_Addbeam, self.button_remove_List_Beam, self.button_simulateBeam):
            bSizer18.Add(btn, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer17.Add(bSizer18, 0, 0, 5)
        self.m_scrolledWindow1.SetSizer(bSizer17)
        self.m_scrolledWindow1.Layout()
        bSizer4.Add(self.m_scrolledWindow1, 1, wx.ALL | wx.EXPAND, 5)

        self.panel_BeamLauncherControls.SetSizer(bSizer4)
        self.panel_BeamLauncherControls.Layout()

        self.panel_vispy_BeamLauncherPlot = wx.Panel(self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_STATIC | wx.TAB_TRAVERSAL)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)
        self.m_panel6 = wx.Panel(self.panel_vispy_BeamLauncherPlot, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer12.Add(self.m_panel6, 1, wx.EXPAND | wx.ALL, 5)
        self.panel_vispy_BeamLauncherPlot.SetSizer(bSizer12)
        self.panel_vispy_BeamLauncherPlot.Layout()

        self.m_splitter1.SplitVertically(self.panel_BeamLauncherControls, self.panel_vispy_BeamLauncherPlot, 286)
        bSizer3.Add(self.m_splitter1, 1, wx.EXPAND, 5)
        self.SetSizer(bSizer3)
        self.Layout()

        # Event Bindings for Derived Class Overrides
        self.choice_BeamLauncherType.Bind(wx.EVT_CHOICE, self.choice_BeamLauncherType_OnChoice)
        self.choice_DirectionRays.Bind(wx.EVT_CHOICE, self.choice_DirectionRaysOnChoice)
        self.button_SelectColor.Bind(wx.EVT_BUTTON, self.button_SelectColor_OnClick)
        self.button_Addbeam.Bind(wx.EVT_BUTTON, self.button_AddBeam_OnButtonClick)
        self.button_remove_List_Beam.Bind(wx.EVT_BUTTON, self.button_remove_List_BeamOnButtonClick)
        self.button_simulateBeam.Bind(wx.EVT_BUTTON, self.button_simulateBeamOnButtonClick)

    def choice_BeamLauncherType_OnChoice(self, event): event.Skip()
    def choice_DirectionRaysOnChoice(self, event): event.Skip()
    def button_SelectColor_OnClick(self, event): event.Skip()
    def button_AddBeam_OnButtonClick(self, event): event.Skip()
    def button_remove_List_BeamOnButtonClick(self, event): event.Skip()
    def button_simulateBeamOnButtonClick(self, event): event.Skip()

    def m_splitter1OnIdle(self, event):
        self.m_splitter1.SetSashPosition(286)
        self.m_splitter1.Unbind(wx.EVT_IDLE)
