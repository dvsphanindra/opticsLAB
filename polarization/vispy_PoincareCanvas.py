import numpy as np

import sys

from vispy import scene

import vispy as vispy

from raytracing.miscellaneous import XYZAxis_Labeled

from vispy.scene.visuals import GridMesh

from vispy.color import Color

from polarization_sources import SoP

from polarization_components import Retarder, Polariser

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})

# •◊×

#sys.path.append("/media/DATA/Python_projects/pyOptiCAD/")

class Coordinate_Axes(XYZAxis_Labeled):
	def __init__(self, parent, labels=("S1", "S2", "S3"), labels_on=True):
		if not labels_on:
			labels=("", "", "")
		XYZAxis_Labeled.__init__(self, parent=parent, labels=labels)


class PoincareSphere_Canvas(scene.SceneCanvas):
	def __init__(self, *a, **k):
		sizes = k.pop("sizes", (300, 300))  # Default value is (300, 300)
		azimuth = k.pop("azimuth", 100)
		elevation = k.pop("elevation", 15)
		labels = k.pop("labels", ("S1", "S2", "S3"))
		scene.SceneCanvas.__init__(self, size=sizes, keys='interactive', *a, **k)
		
		self.unfreeze()
		self.view = self.central_widget.add_view()
		self.view.bgcolor = Color(color="lightsteelblue")
		self.view.camera = scene.TurntableCamera(up='+z', azimuth=azimuth, elevation=elevation, fov=30)
		
		# Draw a Poincare Sphere
		# self.poincareSphere=PoincareSphere(radius=1.0, center=(0.0,0.0,0.0), parent=self.view.scene, labels=labels)
		
		self.selected_object=None
		self.selected_object_name=None
		
		self.show()
	
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
	def __init__(self, parent, radius=1.0, center=(0.0, 0.0, 0.0), color=Color((0.3, 0.3, 1, 0.4)), labels=("S1", "S2", "S3")):
		"""
		Creates the data of a sphere whose center, and radius are given as inputs
		"""
		self.parent=parent
		# Generate the grid in spherical coordinates
		# Names of the spherical coordinate axes according to ISO convention
		theta = np.linspace(0, np.pi, 50)
		phi = np.linspace(0, 2 * np.pi, 50)
		PHI, THETA = np.meshgrid(phi, theta)
		RHO = radius  # Size of the sphere
		
		# Convert to cartesian coordinates
		x_grid = (RHO * np.sin(THETA) * np.cos(PHI)) + center[0]
		y_grid = (RHO * np.sin(THETA) * np.sin(PHI)) + center[1]
		z_grid = (RHO * np.cos(THETA)) + center[2]
		
		Coordinate_Axes(parent=self.parent, labels=labels)
		
		mesh=GridMesh(x_grid, y_grid, z_grid, parent=self.parent, color=color)
		mesh.ambient_light_color=Color((0.3, 0.3, 1, 0.1))
		mesh.light_dir=np.array((0,0,1))
		mesh.shading='flat'
		
if __name__ == '__main__':
	canvas = scene.SceneCanvas(keys='interactive')
	view = canvas.central_widget.add_view()
	view.camera = scene.TurntableCamera(up='z', fov=30)
	
	sphere = PoincareSphere(parent=view.scene)
	
	canvas.bgcolor = Color(color="lightsteelblue", alpha=0.5)
	# retarder1 = Retarder(delta=40, theta=-60, parent=view.scene, color='teal', name='R1')
	# retarder1 = Retarder(delta=40, theta=20, parent=view.scene, color='teal', name='R1', draw=True)
	retarder1 = Retarder(delta=35, theta=60, parent=view.scene, color='teal', name='R1')
	
	sop1=SoP(np.array((1,0,-1,0)), parent=view.scene, color='white', name="SoP1")
	sop2=retarder1.retard(sop1, draw=True)

	retarder2 = Retarder(delta=40, theta=30, parent=view.scene, color='indigo', name='R2', draw=True)
	sop3=retarder2.retard(sop2,draw=True)

	retarder3 = Retarder(delta=10, theta=-40, parent=view.scene, color='magenta', name='R3', draw=True)
	sop4=retarder3.retard(sop3,draw=True)

	polariser1=Polariser(20, parent=view.scene, color='yellow', name="P1", draw=True)
	out_SoP=polariser1.polarise(sop4,draw=True)
	print("SoP out= ", out_SoP.stokes_vector, "DoP= ",out_SoP.get_DegreeOfPolarization())
	#
	# retarder1 = Retarder(delta=60, theta=20, parent=view.scene, color='green', name='R1', draw=True)
	# sop2 = retarder1.retard(sop1, draw=True)
	#
	# retarder2 = Retarder(delta=130, theta=60, parent=view.scene, color='yellow', name='R2', draw=True)
	# sop3=retarder2.retard(sop2,draw=True)
	#
	# polariser1=Polariser(35, parent=view.scene, color='blue', name="P1", draw=True)
	# out_SoP=polariser1.polarise(sop3,draw=True)
	print("SoP out= ", out_SoP.stokes_vector, "DoP= ",out_SoP.get_DegreeOfPolarization())

	sphere = PoincareSphere(parent=view.scene)
	canvas.show()
	
	if sys.flags.interactive == 0:
		vispy.app.run()
