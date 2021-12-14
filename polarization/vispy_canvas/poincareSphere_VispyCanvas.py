import numpy as np

import sys

from vispy import scene

import vispy as vispy

from raytracing.component.miscellaneous_components import XYZAxis_Labeled

from vispy.scene.visuals import GridMesh

from vispy.color import Color

from ..components import Linear_Polariser
from ..components import Generic_Waveplate
from ..components import StateofPolarization

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.3f}'.format})

# •◊×

#sys.path.append("/media/DATA/Python_projects/pyOptiCAD/")

class Coordinate_Axes(XYZAxis_Labeled):
	def __init__(self, parentCanvas, labels=("S1", "S2", "S3"), labels_off=False):
		if labels_off:
			labels=("", "", "")
		XYZAxis_Labeled.__init__(self, parentCanvas=parentCanvas, labels=labels)


class PoincareSphere_VispyCanvas:
	def __init__(self, bgColor='lightsteelblue', *a, **k):
		sizes = k.pop("sizes", (300, 300))  # Default value is (300, 300)
		azimuth = k.pop("azimuth", 100)
		elevation = k.pop("elevation", 15)
		labels = k.pop("labels", ("S1", "S2", "S3"))
		self.bgColor = bgColor
		self.canvas = scene.SceneCanvas(keys='interactive', bgcolor=Color(color=self.bgColor, alpha=0.5))
		self.view = self.canvas.central_widget.add_view()
		self.view.camera = scene.TurntableCamera(up='z', fov=30)
		# scene.SceneCanvas.__init__(self, size=sizes, keys='interactive', *a, **k)
		
		# self.unfreeze()
		# self.view = self.central_widget.add_view()
		# self.view.bgcolor = Color(color="lightsteelblue")
		# self.view.camera = scene.TurntableCamera(up='+z', azimuth=azimuth, elevation=elevation, fov=30)
		
		# Draw a Poincare Sphere
		# self.poincareSphere=PoincareSphere(radius=1.0, center=(0.0,0.0,0.0), parentCanvas=self.view.scene, labels=labels)
		
		self.selected_object=None
		self.selected_object_name=None
		self.axesLabels = labels
		# self.poincareSphere = PoincareSphere(radius=1.0, center=(0.0, 0.0, 0.0), parentCanvas=self, labels=self.axesLabels)
		
		# self.show()
	
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
				
	def show(self):
		self.canvas.show()
		if sys.flags.interactive == 0:
			vispy.app.run()
				
	# def on_mouse_release(self, event):
	# 	self.print_mouse_event(event, 'Mouse release')
	#
	# def print_mouse_event(self, event, what):
	# 	modifiers = ', '.join([key.name for key in event.modifiers])
	# 	print('%s - pos: %r, button: %s, modifiers: %s, delta: %r' %
	# 	      (what, event.pos, event.button, modifiers, event.delta))
		
	# def on_resize(self, event):
	# 	Set canvas viewport and reconfigure visual transforms to match.
		# vp = (0, 0, self.physical_size[0], self.physical_size[1])
		# self.context.set_viewport(*vp)
		# self.axis_x.transforms.configure(canvas=self, viewport=vp)
		# self.axis_y.transforms.configure(canvas=self, viewport=vp)
		# self.line.transforms.configure(canvas=self, viewport=vp)

	"""
	def on_key_press(self, event):
		modifiers = [key.name for key in event.modifiers]
		print('Key pressed - text: %r, key: %s, modifiers: %r' % (
			event.text, event.key.name, modifiers))
	
	def on_key_release(self, event):
		modifiers = [key.name for key in event.modifiers]
		print('Key released - text: %r, key: %s, modifiers: %r' % (
			event.text, event.key.name, modifiers))
	
	
	
	
	
	# def on_mouse_move(self, event):
	# 	self.print_mouse_event(event, 'Mouse move')
	
	def on_mouse_wheel(self, event):
		self.print_mouse_event(event, 'Mouse wheel')
	
	
	"""
	
class PoincareSphere:
	def __init__(self, parentCanvas, radius=1.0, center=(0.0, 0.0, 0.0), color=Color((0.3, 0.3, 1, 0.4)), labels=("S1", "S2", "S3")):
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
			
		self.axes=Coordinate_Axes(parentCanvas=self.parentCanvas, labels=self.axesLabels)
		
		self.mesh=GridMesh(self.x_grid, self.y_grid, self.z_grid, parent=self.parentCanvas.view.scene, color=self.color)
		self.mesh.ambient_light_color=Color((0.3, 0.3, 1, 0.1))
		self.mesh.light_dir=np.array((0,0,1))
		self.mesh.shading='flat'
		
if __name__ == '__main__':
	canvas = scene.SceneCanvas(keys='interactive')
	view = canvas.central_widget.add_view()
	view.camera = scene.TurntableCamera(up='z', fov=30)
	
	# sphere = PoincareSphere(parent=view.scene)
	
	canvas.bgcolor = Color(color="lightsteelblue", alpha=0.5)
	# retarder1 = Retarder(delta=40, theta=-60, parent=view.scene, color='teal', name='R1', draw=True)
	# retarder1 = Retarder(delta=40, theta=20, parent=view.scene, color='teal', name='R1', draw=True)
	# retarder1 = Retarder(delta=35, theta=60, parent=view.scene, color='teal', name='R1', draw=True)
	
	retarder1 = Generic_Waveplate(name="R1", delta=45, theta=20, color='indigo', parent=view.scene)
	retarder2 = Generic_Waveplate(name="R2", delta=30, theta=60, color='magenta', parent=view.scene)
	retarder3 = Generic_Waveplate(name="R3", delta=100, theta=40, color='green', parent=view.scene)
	polariser1 = Linear_Polariser(name="P1", theta=80, color='yellow', parent=view.scene)
	
	sop1=StateofPolarization(mueller=np.array((1,0,0,1)), parent=view.scene, color='white', name="SoP1")
	
	sop2=retarder1.analyse(sop1)
	print("SoP2=",sop2.get_StokesVector())
	sop3=retarder2.analyse(sop2)
	sop4=retarder3.analyse(sop3)
	
	out_SoP=polariser1.analyse(sop4)

	print("SoP out= ", out_SoP.stokes_vector, "DoP= ",out_SoP.get_DegreeOfPolarization())
	
	

	sphere = PoincareSphere(parentCanvas=view.scene)
	canvas.show()
	
	if sys.flags.interactive == 0:
		vispy.app.run()
