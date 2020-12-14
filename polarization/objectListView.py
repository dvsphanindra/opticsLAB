import wx
from ObjectListView import ObjectListView, ColumnDefn, OLVEvent

class objectList(ObjectListView):
	# ----------------------------------------------------------------------
	def __init__(self, parent, componentsList=None):
		ObjectListView.__init__(self, parent=parent, id=wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		
		self.componentsList = componentsList
		
		self.noOfObjects = 0 if componentsList is None else len(componentsList)
		
		self.setColumns() # Initialize column headers
		
		# Allow the cell values to be edited when double-clicked
		self.cellEditMode = ObjectListView.CELLEDIT_NONE
		self.oddRowsBackColor = "Light Blue"
		
		self.Bind(OLVEvent.EVT_ITEM_CHECKED, self.on_item_checked)
		# self.Bind(self.OnListItemSelected, self.on_item_checked)
		
		if self.componentsList is not None:
			self.updateList(self.componentsList)
		
	# ----------------------------------------------------------------------
	def updateList(self, data):
		self.SetObjects(data) # Replaces the existing columns
		for obj in self.GetObjects():
			self.SetCheckState(obj, True) # Select all objects for display
		self.noOfObjects = len(data)
		self.RepopulateList()
	
	# ----------------------------------------------------------------------
	def append2List(self, data):
		self.AddObjects([data]) # Appends to the list
		self.noOfObjects += 1
		self.SetCheckState(self.GetObjectAt(self.noOfObjects-1), True) # Set the checked state as True for the recently added object
		self.RepopulateList()
	
	# ----------------------------------------------------------------------
	def setColumns(self):
		self.SetColumns([
			ColumnDefn("Name", "left", 100, valueGetter="name"),#,groupKeyGetter="ProjectName", groupKeyConverter="ProjectName", ),
			ColumnDefn("Type", "left", 200, valueGetter="type"),#,groupKeyGetter="ProjectName", groupKeyConverter="ProjectName"),
			ColumnDefn("Description", "left", 400, valueGetter="description")#,groupKeyGetter="ProjectName", groupKeyConverter="ProjectName"),
		])
		
		d = self.CreateCheckStateColumn() # Create a checkbox in the first column)
		
	def on_item_checked(self, event):
		obj = self.GetSelectedObject()
		if obj is not None:
			checked = 'Checked' if self.IsChecked(obj) else 'Unchecked'
			print('{} row is {}'.format(obj.name, checked))


########################################################################
class MainFrame(wx.Frame):
	# ----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
		                  title="ObjectListView Demo", size=(800, 600))
		panel = objectList(self)


########################################################################
class TestApp(wx.App):
	
	# ----------------------------------------------------------------------
	def __init__(self, redirect=False, filename=None):
		wx.App.__init__(self, redirect, filename)
	
	# ----------------------------------------------------------------------
	def OnInit(self):
		# create frame here
		frame = MainFrame()
		frame.Show()
		return True


# ----------------------------------------------------------------------
def main():
	"""
	Run the demo
	"""
	app = TestApp()
	app.MainLoop()


if __name__ == "__main__":
	main()
