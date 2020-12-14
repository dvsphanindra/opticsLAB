import wx
from ObjectListView import ObjectListView, ColumnDefn, OLVEvent


########################################################################
class Book(object):
	"""
	Model of the Book object

	Contains the following attributes:
	'ISBN', 'Author', 'Manufacturer', 'Title', 'available'
	"""
	
	# ----------------------------------------------------------------------
	def __init__(self, title, author, isbn, mfg, available):
		self.isbn = isbn
		self.author = author
		self.mfg = mfg
		self.title = title
		self.available = available


########################################################################
class objectListPanel(wx.Panel):
	# ----------------------------------------------------------------------
	def __init__(self, parent):
		wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
		# self.templateDict = {'Detector': {'Type': 'Detector', 'Name': 'Detector_1', 'Description': '', 'Theta': -45.0, 'Color': 'Blue', 'Enabled': True}, 'Polariser': {'Type': 'Polariser', 'Name': 'Polariser_1', 'Description': '', 'Delta': 30.0, 'Theta': 45.0, 'Mueller': [[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]], 'Jones': [[1.0, 1.0], [1.0, 1.0]], 'Color': 'Blue', 'Enabled': True}, 'project': {'Type': 'project', 'Name': 'Polarimeter_Project', 'Description': '', 'Version': '1.0.0', 'Author': '', 'Created': '', 'Modified': ''}, 'Retarder': {'Type': 'Retarder', 'Name': 'Retarder_1', 'Description': '', 'Delta': 30.0, 'Theta': -45.0, 'Mueller': [[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]], 'Jones': [[1.0, 1.0], [1.0, 1.0]], 'Color': 'Blue', 'Enabled': True}, 'Source': {'Type': 'Source', 'Name': 'Source_1', 'Description': '', 'Theta': -45.0, 'Mueller': [1.0, 0.0, 0.0, 0.0], 'Jones': [1, 1], 'Color': 'Blue', 'Enabled': True}}
		self.products = [Book("wxPython in Action", "Robin Dunn",
		                      "1932394621", "Manning", available=True),
		                 Book("Hello World", "Warren and Carter Sande",
		                      "1933988495", "Manning", False)
		                 ]
		
		self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.setData(self.products)
		
		# Allow the cell values to be edited when double-clicked
		self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
		
		self.dataOlv.Bind(OLVEvent.EVT_ITEM_CHECKED, self.on_item_checked)
		# create an update button
		updateBtn = wx.Button(self, wx.ID_ANY, "Update OLV")
		updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)
		
		# Create some sizers
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		
		mainSizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
		mainSizer.Add(updateBtn, 0, wx.ALL | wx.CENTER, 5)
		self.SetSizer(mainSizer)
	
	# ----------------------------------------------------------------------
	def updateControl(self, data):
		"""

		"""
		print("updating...")
		product_dict = [{"title": "Core Python Programming", "author": "Wesley Chun",
		                 "isbn": "0132269937", "mfg": "Prentice Hall"},
		                {"title": "Python Programming for the Absolute Beginner",
		                 "author": "Michael Dawson", "isbn": "1598631128",
		                 "mfg": "Course Technology"},
		                {"title": "Learning Python", "author": "Mark Lutz",
		                 "isbn": "0596513984", "mfg": "O'Reilly"}
		                ]
		data = self.products + product_dict
		# self.dataOlv.SetObjects(data)
		self.dataOlv.AddObjects(data) # Appends to the list
	
	# ----------------------------------------------------------------------
	def setData(self, data=None):
		self.dataOlv.SetColumns([
			ColumnDefn("Title", "left", 220, "title"),
			ColumnDefn("Author", "left", 200, "author"),
			ColumnDefn("ISBN", "right", 100, "isbn"),
			ColumnDefn("Mfg", "left", 180, "mfg")
		])
		available_Column = ColumnDefn("Available", "center", 60, "available")
		self.dataOlv.AddColumnDefn(available_Column)
		# self.dataOlv.InstallCheckStateColumn(available_Column)
		
		self.dataOlv.CreateCheckStateColumn(0)
		
		self.dataOlv.SetObjects(data)
		data = [Book("Harry Potter", "Harry",
		             "895587422", "TATA", available=True),
		        Book("Python", "DVS",
		             "4255742155", "McGraw", False),
		        Book("wxPython in Action2", "Robin Dunn2",
		             "45721452", "Manning", available=True),
		        Book("Hello World2", "Warren and Carter Sande2",
		             "58368536", "Manning", True)]
		self.dataOlv.AddObjects(data)
	
	def on_item_checked(self, event):
		obj = self.dataOlv.GetSelectedObject()
		checked = 'Checked' if self.dataOlv.IsChecked(obj) else 'Unchecked'
		print('{} row is {}'.format(obj.title, checked))


########################################################################
class MainFrame(wx.Frame):
	# ----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
		                  title="ObjectListView Demo", size=(800, 600))
		panel = objectListPanel(self)


########################################################################
class GenApp(wx.App):
	
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
	app = GenApp()
	app.MainLoop()


if __name__ == "__main__":
	main()
