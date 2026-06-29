#!/usr/bin/env python

import wx

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import cubecolourdialog as CCD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.cubecolourdialog as CCD


class CubeColourDialogDemo(CCD):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)

        static = wx.StaticText(self, -1, "Notice the panel background colour!", (50, 50))
        b = wx.Button(self, -1, "Create and Show a CubeColourDialog", (50, 70))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        # self.log = log


    def OnButton(self, evt):

        if not hasattr(self, "colourData"):
            self.colourData = wx.ColourData()

        self.colourData.SetColour(self.GetBackgroundColour())

        dlg = CCD.CubeColourDialog(self, self.colourData)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            self.colourData = dlg.GetColourData()
            h, s, v, a = dlg.GetHSVAColour()

            # ... then do something with it. The actual colour data will be
            # returned as a three-tuple (r, g, b) in this particular case.
            colour = self.colourData.GetColour()

            self.SetBackgroundColour(self.colourData.GetColour())
            self.Refresh()

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()

#----------------------------------------------------------------------

# overview = CCD.__doc__
#
# if __name__ == '__main__':
#     import sys,os
#     import run
#     run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

class mainFrame ( wx.Frame ):


    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_ColorSelection = CubeColourDialogDemo(self)
        bSizer1.Add(self.panel_ColorSelection, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)


if __name__ == "__main__":
    app = wx.App(False)

    GUI = mainFrame(None)

    GUI.Raise()

    GUI.Show(True)

    app.MainLoop()

