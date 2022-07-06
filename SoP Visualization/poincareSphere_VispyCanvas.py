import numpy as np

from vispy import scene
from vispy.visuals.transforms import STTransform

from vispy.scene.visuals import GridMesh, XYZAxis

from vispy.color import Color

class XYZAxis_Labeled(XYZAxis):
	def __init__(self, label=True, labels=("X", "Y", "Z"), pos=None, parentCanvas=None, **kwargs):
		kwargs.setdefault('parent', parentCanvas.view.scene)
		super().__init__(**kwargs)
		self.unfreeze()
		self.labeling = label
		self.position = pos
		if self.position is None:
			self.position = np.array([0, 0, 0])
			self.transform = STTransform(translate=self.position)
		
		self.x = self.position + [1.05, 0, 0]
		self.y = self.position + [0, 1.05, 0]
		self.z = self.position + [0, 0, 1.05]
		
		if self.labeling:
			scene.Text(labels[0], font_size=50, bold=True, color='red', parent=parentCanvas.view.scene, pos=self.x)
			scene.Text(labels[1], font_size=50, bold=True, color='green', parent=parentCanvas.view.scene, pos=self.y)
			scene.Text(labels[2], font_size=50, bold=True, color='blue', parent=parentCanvas.view.scene, pos=self.z)


class Coordinate_Axes(XYZAxis_Labeled):
	def __init__(self, parentCanvas, labels=("X", "Y", "Z"), labels_off=False):
		if labels_off:
			labels=("", "", "")
		XYZAxis_Labeled.__init__(self, parentCanvas=parentCanvas, labels=labels)


class PoincareSphere_VispyCanvas:
	def __init__(self, bgColor='lightsteelblue', *a, **k):
		azimuth = k.pop("azimuth", 100)
		elevation = k.pop("elevation", 15)
		labels = k.pop("labels", ("X", "Y", "Z"))
		self.bgColor = bgColor
		self.canvas = scene.SceneCanvas(keys='interactive', bgcolor=Color(color=self.bgColor, alpha=0.5), *a, **k)
		self.view = self.canvas.central_widget.add_view()
		self.view.camera = scene.TurntableCamera(up='z', fov=30)
		
		self.selected_object=None
		self.selected_object_name=None
		self.axesLabels = labels
		self.earth = Poincare_Sphere(radius=1.0, center=(0.0, 0.0, 0.0), parentCanvas=self, labels=self.axesLabels)
		
		self.canvas.show()
	
	def on_mouse_press(self, event):
		tr = self.scene.node_transform(self.view.scene)
		# pos = tr.map(event.pos)
		self.view.interactive = False
		self.selected_object = self.visuals_at(event.pos)
		# print("Vispy selected:", self.selected_object)
		try:
			# print("buttonpressed= ",self.selected_object)
			self.selected_object_name = self.selected_object[0].text
		except:
			self.selected_object = None
			self.selected_object_name = None
			
		self.view.interactive = True

		if event.button == 1:
			if self.selected_object is not None:
				self.selected_object = self.selected_object[0].parent
				# update transform to selected object
				tr = self.scene.node_transform(self.selected_object)
				pos = tr.map(event.pos)
				

class Poincare_Sphere:
	def __init__(self, parentCanvas, radius=1.0, center=(0.0, 0.0, 0.0), color=Color((0.3, 0.3, 1, 0.4)), labels=("X", "Y", "Z")):
		"""
		Creates the data of a sphere whose center, and radius are given as inputs
		"""
		self.parentCanvas=parentCanvas
		self.color = color
		self.axesLabels = labels
		# Generate the grid in spherical coordinates
		# Names of the spherical coordinate axes according to ISO convention
		theta = np.linspace(0, np.pi, 50)
		phi = np.linspace(0, 2 * np.pi, 50)
		PHI, THETA = np.meshgrid(phi, theta)
		RHO = radius  # Size of the sphere
		
		# Convert to cartesian coordinates
		self.x_grid = (RHO * np.sin(THETA) * np.cos(PHI)) + center[0]
		self.y_grid = (RHO * np.sin(THETA) * np.sin(PHI)) + center[1]
		self.z_grid = (RHO * np.cos(THETA)) + center[2]
		
		self.axes = None
		self.mesh = None
		
		self.update_sphere()
		
	def update_sphere(self):
		if self.axes is not None:
			self.axes.parent = None
			self.mesh.parent = None
			
		self.axes = Coordinate_Axes(parentCanvas=self.parentCanvas, labels=self.axesLabels)
		
		self.mesh = GridMesh(self.x_grid, self.y_grid, self.z_grid, parent=self.parentCanvas.view.scene, color=self.color)
		self.mesh.unfreeze()
		self.mesh.ambient_light_color = Color((0.3, 0.3, 1, 0.1))
		self.mesh.light_dir = np.array((0,0,1))
		self.mesh.shading = 'flat'
		self.mesh.freeze()
