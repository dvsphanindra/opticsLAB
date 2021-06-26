# -*- coding: utf-8 -*-

import sys

import numpy as np

import vispy

from vispy import scene

from vispy.scene.visuals import Arrow

from vispy.color import Color

from scipy.spatial.transform import Rotation as R


class PolarizationEllipse_VispyCanvas(scene.SceneCanvas):
	def __init__(self, stokesVector=None, color='r', *a, **k):
		sizes = k.pop("sizes", (300, 300))  # Default value is (300, 300)
		# print(sizes)
		self.color = color
		self.stokesVector=stokesVector
		self.stokesVector_visual = None
		self.stokesVectorArrow_visual = None
		scene.SceneCanvas.__init__(self, size=sizes, keys='interactive', *a, **k)
		
		self.unfreeze()
		self.view = self.central_widget.add_view()
		self.view.bgcolor = Color(color="lightsteelblue")
		self.view.camera = scene.PanZoomCamera(rect=(-1, -1, 2, 2))
		self.view.camera.zoom(0.75)
		
		self.draw_axes()
		
		if self.stokesVector is not None:
			self.draw_StokesVector()
		
		self.show()
		
	def draw_axes(self):
		xax = scene.Axis(pos=[[-0.5, 0], [0.5, 0]], font_size=0, axis_color='k', text_color='k', minor_tick_length=0.0,
		                 major_tick_length=0.0,
		                 parent=self.view.scene)
		
		yax = scene.Axis(pos=[[0, -0.5], [0, 0.5]], tick_direction=(-1, 0), minor_tick_length=0.0,
		                 major_tick_length=0.0,
		                 font_size=0, axis_color='k', tick_color='k', text_color='k',
		                 parent=self.view.scene)
		
		scene.Text('E', font_size=20, color=self.color, parent=self.view.scene, pos=(0.55, 0.01, 0))
		scene.Text('x', font_size=10, color=self.color, parent=self.view.scene, pos=(0.6, -0.015, 0))
		scene.Text('E', font_size=20, color=self.color, parent=self.view.scene, pos=(-0.03, 0.57, 0))
		scene.Text('y', font_size=10, color=self.color, parent=self.view.scene, pos=(0.02, 0.55, 0))
	
	def draw_StokesVector(self):
		# Refer https://en.wikipedia.org/wiki/Stokes_parameters for theory and notations of the polarization ellipse
		I, Q, U, V = self.stokesVector  # Separate the stokes components
		L = complex(Q,U)  # L: Intensity (Complex) of Linear Polarization, V: Intensity of Circular Polarization, I: Total Intensity
		I_p = np.sqrt(Q ** 2 + U ** 2 + V ** 2)  # Intensity of polarized fraction of light
		
		# Calculate the major (A) and minor (B) axes, orientation of the polarization ellipse (theta) and handedness of polarization (h)
		A = np.sqrt((I_p + np.absolute(L)) / 2)
		B = np.sqrt((I_p - np.absolute(L)) / 2)
		theta = np.angle(L)/2
		h = np.sign(V)
		
		# Plot the ellipse
		t = np.linspace(0, 2 * np.pi, 50)
		a, b = A / 2, B / 2
		points = np.vstack((a * np.cos(t), b * np.sin(t), np.zeros(np.shape(t)))).T
		rotation = R.from_euler('z', theta)
		
		x_values, y_values, _ = rotation.apply(points).T
		
		# print("(A,B), (L,absL), theta, (I_p, h) = ({0},{1}), ({2},{3}), {4},({5}, {6})".format(A, B, L, np.absolute(L), np.rad2deg(theta), I_p, h))
		
		if self.stokesVector_visual is not None:
			self.stokesVector_visual.parent=None
			self.stokesVectorArrow_visual.parent=None
		
		self.stokesVector_visual = scene.LinePlot((x_values, y_values), parent=self.view.scene)
		
		if h == -1:
			arrowHead = np.array([(x_values[7], y_values[7], 0, x_values[8], y_values[8], 0)])  # Arrow direction, position
			
			self.stokesVectorArrow_visual = Arrow(pos=np.array([(x_values[8], y_values[8], 0), (x_values[7], y_values[7], 0)]), color=self.color,
			              method='gl', width=5., arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0,
			              arrow_color=self.color, antialias=True, parent=self.view.scene)
		else:
			arrowHead = np.array([(x_values[8], y_values[8], 0, x_values[7], y_values[7], 0)])  # Arrow direction, position
			
			self.stokesVectorArrow_visual = Arrow(pos=np.array([(x_values[8], y_values[8], 0), (x_values[7], y_values[7], 0)]), color=self.color,
			              method='gl', width=5., arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0,
			              arrow_color=self.color, antialias=True, parent=self.view.scene)
			
		
	def validate_StokesVector(self, stokesVector):
		polarization_vector = stokesVector[1:]
		assert np.sqrt(np.sum(np.square(polarization_vector))) <= stokesVector[0], "Irregular Stokes Vector: Q*Q + U*U + V*V > I+I I = {0}, [Q,U,V]={1}, sum of squares = {2}".format(
			stokesVector[0], polarization_vector, np.sum(np.square(polarization_vector)))
		
	def set_StokesVector(self, stokesVector):
		self.validate_StokesVector(stokesVector)
		self.stokesVector=stokesVector
		if stokesVector is not None:
			self.draw_StokesVector()
		
		

if __name__ == '__main__':
	p=PolarizationEllipse_VispyCanvas()
	p.set_StokesVector(np.array((1,0,0,-1)))
	
	if sys.flags.interactive == 0:
		vispy.app.run()
