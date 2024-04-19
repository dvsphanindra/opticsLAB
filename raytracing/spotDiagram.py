# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
"""
Plot data with different styles
"""
import sys

import numpy as np

import vispy

from vispy import scene

from vispy.scene.visuals import Arrow

from vispy.color import Color

from scipy.spatial.transform import Rotation as R


class SpotDiagramPlot(scene.SceneCanvas):
	def __init__(self, data, marker='+', marker_color='black', *a, **k):
		sizes = k.pop("sizes", (300, 300))  # Default value is (300, 300)
		self.marker_color = marker_color
		self.marker = marker
		self.spots = None
		self.x_axis = None
		self.y_axis = None
		self.stokesVectorArrow_visual = None
		scene.SceneCanvas.__init__(self, size=sizes, keys='interactive', *a, **k)
		
		self.unfreeze()
		self.view = self.central_widget.add_view()
		self.view.bgcolor = Color(color="w")
		self.view.camera = scene.PanZoomCamera(rect=(-1, -1, 2, 2))
		self.view.camera.zoom(0.75)
		
		self.draw_axes()
		
		self.draw_plot(data)
		
		self.show()
	
	def draw_axes(self,xLim=(-1,1), yLim=(-1,1)):
		if self.x_axis is not None:
			self.x_axis.parent=None
		self.x_axis = scene.Axis(pos=[[xLim[0], 0], [xLim[1], 0]], font_size=0, axis_color='k', text_color='k',
		                         minor_tick_length=0.0,
		                         major_tick_length=0.0,
		                         parent=self.view.scene)
		
		if self.y_axis is not None:
			self.y_axis.parent=None
		self.y_axis = scene.Axis(pos=[[0, yLim[0]], [0, yLim[1]]], tick_direction=(-1, 0), minor_tick_length=0.0,
		                         major_tick_length=0.0,
		                         font_size=0, axis_color='k', tick_color='k', text_color='k',
		                         parent=self.view.scene)
		
	def draw_plot(self, data):
		print(np.max(data[:,0]), np.min(data[:,0]), np.max(data[:,1]), np.min(data[:,1]))
		self.draw_axes(xLim=(np.min(data[:, 0]), np.max(data[:, 0])), yLim=(np.min(data[:, 1]), np.max(data[:, 1])))
		self.spots = scene.LinePlot((data[:,0], data[:,1]), symbol=self.marker, color=self.marker_color, parent=self.view.scene)
	
if __name__ == '__main__':
	p = SpotDiagramPlot(np.reshape(np.arange(0,25), (5,5)))
	
	if sys.flags.interactive == 0:
		vispy.app.run()
