# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
"""
Plot data with different styles
"""
import sys

import numpy as np

import vispy
from astropy.constants.codata2022 import alpha

from vispy import scene

from vispy.scene.visuals import Arrow

from vispy.color import Color

from scipy.spatial.transform import Rotation as R


# class SpotDiagramPlot(scene.SceneCanvas):
# 	def __init__(self, data, marker='+', marker_color='black', *a, **k):
# 		sizes = k.pop("sizes", (300, 300))  # Default value is (300, 300)
# 		self.marker_color = marker_color
# 		self.marker = marker
# 		self.spots = None
# 		self.x_axis = None
# 		self.y_axis = None
# 		self.stokesVectorArrow_visual = None
# 		scene.SceneCanvas.__init__(self, size=sizes, keys='interactive', *a, **k)
#
# 		self.unfreeze()
# 		self.view = self.central_widget.add_view()
# 		self.view.bgcolor = Color(color="w")
# 		self.view.camera = scene.PanZoomCamera(rect=(-1, -1, 2, 2))
# 		self.view.camera.zoom(0.75)
#
# 		self.draw_axes()
#
# 		self.draw_plot(data)
#
# 		self.show()
#
# 	def draw_axes(self,xLim=(-1,1), yLim=(-1,1)):
# 		if self.x_axis is not None:
# 			self.x_axis.parent=None
# 		self.x_axis = scene.Axis(pos=[[xLim[0], 0], [xLim[1], 0]], font_size=0, axis_color='k', text_color='k',
# 		                         minor_tick_length=0.0,
# 		                         major_tick_length=0.0,
# 		                         parent=self.view.scene)
#
# 		if self.y_axis is not None:
# 			self.y_axis.parent=None
# 		self.y_axis = scene.Axis(pos=[[0, yLim[0]], [0, yLim[1]]], tick_direction=(-1, 0), minor_tick_length=0.0,
# 		                         major_tick_length=0.0,
# 		                         font_size=0, axis_color='k', tick_color='k', text_color='k',
# 		                         parent=self.view.scene)
#
# 	def draw_plot(self, data):
# 		print(np.max(data[:,0]), np.min(data[:,0]), np.max(data[:,1]), np.min(data[:,1]))
# 		self.draw_axes(xLim=(np.min(data[:, 0]), np.max(data[:, 0])), yLim=(np.min(data[:, 1]), np.max(data[:, 1])))
# 		self.spots = scene.LinePlot((data[:,0], data[:,1]), symbol=self.marker, color=self.marker_color, parent=self.view.scene)

# class SpotDiagramPlot(scene.SceneCanvas):
#     def __init__(self, data_dict, *a, **k):
#         sizes = k.pop("sizes", (300, 300))
#         self.spots = []
#         self.x_axis = None
#         self.y_axis = None
#         scene.SceneCanvas.__init__(self, size=sizes, keys='interactive', *a, **k)
#
#         self.unfreeze()
#         self.view = self.central_widget.add_view()
#         self.view.bgcolor = Color(color="w")
#         self.view.camera = scene.PanZoomCamera(rect=(-0.05, -0.05, 0.1, 0.1))
#         self.view.camera.zoom(1.0)
#
#         self.draw_plot(data_dict)
#         self.freeze()
#
#     def draw_axes(self, xLim=(-1, 1), yLim=(-1, 1)):
#         if self.x_axis is not None:
#             self.x_axis.parent = None
#         self.x_axis = scene.Axis(pos=[[xLim[0], 0], [xLim[1], 0]], font_size=0, axis_color='k', text_color='k',
#                                  parent=self.view.scene)
#
#         if self.y_axis is not None:
#             self.y_axis.parent = None
#         self.y_axis = scene.Axis(pos=[[0, yLim[0]], [0, yLim[1]]], tick_direction=(-1, 0), font_size=0, axis_color='k',
#                                  tick_color='k', text_color='k', parent=self.view.scene)
#
#     def draw_plot(self, data_dict):
#         # Find global min and max across all colors to scale axes
#         all_pts = np.vstack(list(data_dict.values()))
#         x_min, x_max = np.min(all_pts[:, 0]), np.max(all_pts[:, 0])
#         y_min, y_max = np.min(all_pts[:, 1]), np.max(all_pts[:, 1])
#
#         self.draw_axes(xLim=(x_min, x_max), yLim=(y_min, y_max))
#
#         # Plot each color
#         for color_name, data in data_dict.items():
#             if len(data) > 0:
#                 spot = scene.LinePlot((data[:, 0], data[:, 1]), symbol='+', color=color_name, parent=self.view.scene)
#                 self.spots.append(spot)

import numpy as np
from vispy import scene
from vispy.color import Color

def wavelength_to_rgb(wl_um):
    wl_nm = wl_um * 1000.0

    if 380 <= wl_nm < 440:
        r = -(wl_nm - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif 440 <= wl_nm < 490:
        r = 0.0
        g = (wl_nm - 440) / (490 - 440)
        b = 1.0
    elif 490 <= wl_nm < 510:
        r = 0.0
        g = 1.0
        b = -(wl_nm - 510) / (510 - 490)
    elif 510 <= wl_nm < 580:
        r = (wl_nm - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif 580 <= wl_nm < 645:
        r = 1.0
        g = -(wl_nm - 645) / (645 - 580)
        b = 0.0
    elif 645 <= wl_nm <= 750:
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        r = g = b = 0.5

    if 380 <= wl_nm < 420:
        a = 0.3 + 0.7 * (wl_nm - 380) / (420 - 380)
    elif 420 <= wl_nm <= 700:
        a = 1.0
    elif 700 < wl_nm <= 750:
        a = 0.3 + 0.7 * (750 - wl_nm) / (750 - 700)
    else:
        a = 0.3

    gamma = 0.8
    return (
        (r * a) ** gamma,
        (g * a) ** gamma,
        (b * a) ** gamma,
        1.0
    )


class SpotDiagramPlot(scene.SceneCanvas):
    def __init__(self, spot_data, wavelengths, *a, **k):
        sizes = k.pop("sizes", (700, 700))
        super().__init__(size=sizes, keys='interactive', *a, **k)

        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.view.bgcolor = Color("white")
        self.view.camera = scene.PanZoomCamera(aspect=1)

        self.x_axis = None
        self.y_axis = None
        self.visuals = []

        self.draw_plot(spot_data, wavelengths)
        self.freeze()
        self.show()

    def draw_axes(self, xlim, ylim):
        if self.x_axis is not None:
            self.x_axis.parent = None
        if self.y_axis is not None:
            self.y_axis.parent = None

        self.x_axis = scene.Axis(
            pos=[[xlim[0], 0], [xlim[1], 0]],
            tick_direction=(0, -1),
            domain=xlim,
            axis_color='black',
            tick_color='black',
            text_color='black',
            minor_tick_length=3,
            major_tick_length=6,
            font_size=15,
            parent=self.view.scene
        )

        self.y_axis = scene.Axis(
            pos=[[0, ylim[0]], [0, ylim[1]]],
            tick_direction=(-1, 0),
            domain=ylim,
            axis_color='black',
            tick_color='black',
            text_color='black',
            minor_tick_length=3,
            major_tick_length=6,
            font_size=15,
            parent=self.view.scene
        )

    def draw_plot(self, spot_data, wavelengths):
        all_pts = [pts for pts in spot_data.values() if len(pts) > 0]
        if not all_pts:
            return

        all_pts = np.vstack(all_pts)
        xmin, xmax = np.min(all_pts[:, 0]), np.max(all_pts[:, 0])
        ymin, ymax = np.min(all_pts[:, 1]), np.max(all_pts[:, 1])

        padx = max(1e-4, 0.15 * max(abs(xmin), abs(xmax), xmax - xmin))
        pady = max(1e-4, 0.15 * max(abs(ymin), abs(ymax), ymax - ymin))

        xlim = (xmin - padx, xmax + padx)
        ylim = (ymin - pady, ymax + pady)

        self.draw_axes(xlim, ylim)
        self.view.camera.set_range(x=xlim, y=ylim, margin=0)

        for name, pts in spot_data.items():
            if len(pts) == 0:
                continue

            rgba = wavelength_to_rgb(wavelengths[name])

            markers = scene.Markers(parent=self.view.scene)
            markers.set_data(
                pts,
                face_color=rgba,
                edge_color=rgba,
                size=8,
                symbol='cross'
            )
            self.visuals.append(markers)

            cx, cy = np.mean(pts[:, 0]), np.mean(pts[:, 1])
            scene.Text(
                f"{name} ({wavelengths[name]:.3f} μm)",
                pos=(cx, cy),
                color=rgba,
                font_size=9,
                anchor_x='left',
                anchor_y='bottom',
                parent=None#self.view.scene
            )

# if __name__ == '__main__':
#     p = SpotDiagramPlot(np.reshape(np.arange(0, 25), (5, 5)))
#
#     if sys.flags.interactive == 0:
#         vispy.app.run()
