import wx
from wx.lib.agw import ultimatelistctrl as ULC


class MainPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.run_list = []
		self.selected_obj = None
		
		self.colour1 = wx.Colour('lightblue')# wx.Colour(180, 180, 180)
		self.colour2 = wx.Colour('gainsboro')#wx.Colour(250, 250, 250)
		
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		agwStyle = (ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | wx.LC_REPORT | wx.LC_SINGLE_SEL)
		
		self.ul = ULC.UltimateListCtrl(self, agwStyle=agwStyle)
		
		runBtn = wx.Button(self, label="run")
		runBtn.Bind(wx.EVT_BUTTON, self.onRun)
		btnSizer.Add(runBtn, 0, wx.ALL, 5)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.ul, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.CENTER | wx.ALL, 5)
		self.SetSizer(sizer)
		
		mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_FORMAT
		
		def gen_column_header(name, kind=0, mask=mask):
			# Fill the item with details
			info = ULC.UltimateListItem()
			info._mask = mask
			info._format = 0
			info._kind = kind
			info._text = name
			return info
		
		self.types = ['Name', 'Type', 'Description']
		
		self.ul.InsertColumnInfo(0, gen_column_header("Name", 1, mask | ULC.ULC_MASK_CHECK))
		self.ul.SetColumnWidth(0, 100)
		
		for i in range(len(self.types)):
			idx = i + 1
			self.ul.InsertColumnInfo(idx, gen_column_header(self.types[i], 0, mask | ULC.ULC_MASK_CHECK))
			self.ul.SetColumnWidth(idx, 100)
		
		self.Bind(ULC.EVT_LIST_COL_CHECKING, self.checkBoxHeader)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
		
		for i in range(5):
			self.ul.InsertStringItem(i, "name " + str(i))
			if i % 2:
				color = self.colour1
			else:
				color = self.colour2
			self.ul.SetItemBackgroundColour(i, color)
			
			for j in range(len(self.types)):
				name = self.types[j]
				self.ul.SetStringItem(i, j + 1, "Test")
				self.checkBox = wx.CheckBox(self.ul, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0, name=name)
				self.checkBox.SetBackgroundColour(color)
				self.ul.SetItemWindow(i, j + 1, self.checkBox, expand=True)
				self.run_list.append([self.checkBox, i, j + 1])
		
		self.ul.InsertStringItem(50, "")
	
	def onSelect(self, event):
		idx = event.GetIndex()
		print(idx)
		if idx == event.EventObject.GetItemCount() - 1:
			event.EventObject.Select(idx, on=False)
	
	def OnRightClick(self, event):
		idx = event.GetIndex()
		if idx is not event.EventObject.GetItemCount() - 1:
			event.EventObject.Select(idx, on=True)
			self.selected_obj = event
			self.popupmenu = wx.Menu()
			self.popupmenu.Append(-1, "Delete")
			self.Bind(wx.EVT_MENU, self.onSelectContext)
			self.PopupMenu(self.popupmenu, event.GetPoint())
			self.popupmenu.Destroy()
	
	def onSelectContext(self, event):
		idx = self.selected_obj.GetIndex()
		del_list = []
		
		for item in self.run_list:
			if item[1] == idx:
				del_list.append(item)
		
		for d in del_list:
			self.run_list.remove(d)
		
		if not idx == self.selected_obj.EventObject.GetItemCount() - 1:
			self.selected_obj.EventObject.Select(idx, on=False)
			self.selected_obj.EventObject.DeleteItem(idx)
			self.selected_obj = None
			del_list = []
	
	def onRun(self, event):
		comp_list = []
		for i in self.run_list:
			if i[0].IsChecked():
				n = i[0].GetName()
				comp_list.append([n, i[1]])
		print(comp_list)
	
	def checkBoxHeader(self, event):
		header_idx = event.m_col
		is_checked = event.EventObject.GetColumn(event.m_col)._checked
		
		for item in self.run_list:
			if item[2] == header_idx:
				if is_checked:
					item[0].SetValue(False)
				else:
					item[0].SetValue(True)


class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="pyTable", size=(600, 400))
		MainPanel(self)
		self.Show()


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	app.MainLoop()
