import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm



class wxPoincareSphereAxes:
	def __init__(self, points=None, axes=None, markers=None, markerSize=40, markerColors=None, markerTexts=None):
		# Names of the spherical coordinate variables according to ISO convention
		theta = np.linspace(0, np.pi, 45)
		phi = np.linspace(0, 2*np.pi, 90)
		PHI, THETA = np.meshgrid(phi, theta)
		RHO=1 # Size of the sphere: Unit circle
		# The Cartesian coordinates of the Poincare sphere
		self.xGrid = RHO*np.sin(THETA) * np.cos(PHI)
		self.yGrid = RHO*np.sin(THETA) * np.sin(PHI)
		self.zGrid = RHO*np.cos(THETA)
		
		# Set the aspect ratio to 1 so our sphere looks spherical
		if axes is None:
			fig = plt.figure(figsize=(9,9), facecolor='AliceBlue')
			self.axes = fig.add_subplot(111, projection='3d', facecolor='Gainsboro', frame_on=True)
			plt.tight_layout()
		else:
			self.axes = axes
		
		self.axes.plot_wireframe(self.xGrid, self.yGrid, self.zGrid,  rstride=4, cstride=3, color='Peru', zorder=1)
		
		self.zGrid = np.zeros(np.shape(self.xGrid))
		self.axes.plot_surface(self.xGrid,self.yGrid,self.zGrid, color='Azure', rstride=5, cstride=5, alpha=0.5, zorder=5)
		
		self.components = None
		self.points_count = 0
		self.x_points = None
		self.y_points = None
		self.z_points = None
		
		self.markerSize = markerSize
		
		# Turn off the axis planes
		self.axes.set_axis_off()
		# self.axes.text(0,1,0, "(0,0)", color='r')
		self.axes.quiver(0, 0, 0, 0, 1.2, 0, arrow_length_ratio=0.1)
		self.axes.view_init(20, 60)
		self.axes.set_xlabel("X")
		self.axes.set_ylabel("Y")
		self.axes.set_zlabel("Z")
		
		if points is not None:
			self.add_points(points)
			if markers is not None:
				self.add_markers(markers)
			else:
				self.markers = ['o'] * self.points_count
				
			if markerColors is not None:
				self.add_markerColors(markerColors)
			else:
				self.markerColors = ['DarkSlateGray'] * self.points_count
				
			if markerTexts is not None:
				self.add_markerTexts(markerTexts)
			else:
				self.markerTexts = [''] * self.points_count
			
			self.updatePoincareSphere()
		
		
	def add_points(self, points):
		azimuth = points[:,0]
		elevation = points[:,1]
		# The Cartesian coordinates of the points (r=1)
		self.x_points = np.cos(elevation) * np.sin(azimuth)
		self.y_points = np.cos(elevation) * np.cos(azimuth)
		self.z_points = np.sin(elevation)
		
		self.points_count = points.shape[0]
		
	def add_markers(self, markers):
		marker_count = len(markers)
		if len(markers) == 1:
			self.markers *= self.points_count
		else:
			assert marker_count == self.points_count, "Number of markers (={0}) should be equal to number of points (={1})".format(marker_count, self.points_count)
			self.markers = markers
		
	def add_markerColors(self, markerColors):
		markerColor_count = len(markerColors)
		if markerColor_count == 1:
			markerColors *= self.points_count
		else:
			assert markerColor_count == self.points_count, "Number of markerColors (={0}) should be equal to number of points (={1})".format(markerColor_count, self.points_count)
			self.markerColors = markerColors
			
	def add_markerTexts(self, markerTexts):
		markerText_count = len(markerTexts)
		if len(markerTexts) == 1:
			markerTexts *= self.points_count
		else:
			assert markerText_count == self.points_count, "Number of markerTexts (={0}) should be equal to number of points (={1})".format(markerText_count, self.points_count)
			self.markerTexts = markerTexts
			
	def updatePoincareSphere(self):
		# print(x_points, y_points, z_points, markers)
		for xx, yy,zz, marker, color, text in zip(self.x_points, self.y_points, self.z_points, self.markers, self.markerColors, self.markerTexts):
			self.axes.scatter(xx, yy, zz, color=color, s=self.markerSize, marker=marker, zorder=10)
			self.axes.text(xx+.1, yy+.1, zz+.1, text, color=color)
			
	def drawArc(self, start, end, degrees=True):
		if degrees:
			start = np.deg2rad(start)
			end = np.deg2rad(end)
		azimuth = start[0] # Rotate along great circles only
		elevation = np.linspace(start[1],end[1],10)
		
		# The Cartesian coordinates of the points (r=1)
		x_arc = np.cos(elevation) * np.sin(azimuth)
		y_arc = np.cos(elevation) * np.cos(azimuth)
		z_arc = np.sin(elevation)
		self.axes.plot(x_arc,y_arc,z_arc)
		
# class tempClass(PoincareSphere):
# 	pass
#
# class wxPoincareSphereWidget(PoincareSphere, wx.Control):
# 	def __init__(self, parent, points=None, markers=None, markerSize=40, markerColors=None, markerTexts=None):
# 		wx.Control.__init__(parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, name="wxPoincareSphereWidget")
# 		PoincareSphere.__init__(parent, points=points, markers=markers, markerSize=markerSize, markerColors=markerColors,markerTexts=markerTexts)
# 		pass
		
		

# point = np.array([[0,0],[30,60],[90,180]])
# marker = ['o','x','+']
# texts = ['p1', 'p2', 'p3']
# colors = ['r', 'g', 'b']
# sphere=wxPoincareSphereWidget(None, np.deg2rad(point), markers=marker, markerColors=colors, markerTexts=texts,  markerSize=60)
# sphere.drawArc([90,180], [90,90])
# plt.show()
