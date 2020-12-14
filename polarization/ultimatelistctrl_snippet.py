
import sys

import wx
import wx.lib.agw.ultimatelistctrl as ULC

class MyFrame(wx.Frame):
	
	def __init__(self, parent):
		
		wx.Frame.__init__(self, parent, -1, "UltimateListCtrl Demo")
		
		listItem = ULC.UltimateListCtrl(self, wx.ID_ANY, agwStyle=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES|wx.LC_SINGLE_SEL|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
		
		listItem.InsertColumn(0, "Column 1")
		listItem.InsertColumn(1, "Column 2")
		
		index = listItem.InsertStringItem(2000, "Item 1")
		listItem.SetStringItem(index, 1, "Sub-item 1")
		
		index = listItem.InsertStringItem(3000, "Item 2")
		listItem.SetStringItem(index, 1, "Sub-item 2")
		
		choice = wx.Choice(listItem, -1, choices=["one", "two"])
		index = listItem.InsertStringItem(5000, "A widget")
		
		listItem.SetItemWindow(index, 1, choice, expand=True)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(listItem, 1, wx.EXPAND)
		self.SetSizer(sizer)
	
	
	# our normal wxApp-derived class, as usual

app = wx.App()

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()

