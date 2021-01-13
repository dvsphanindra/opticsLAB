import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy.spatial.transform import Rotation as R


class wx_PolarizationEllipse:
	def __init__(self, axes=None, stokes_vector=np.array((1,1,0,0)), color='r'):
		self.color=color
		# Refer https://en.wikipedia.org/wiki/Stokes_parameters for theory and notations of the polarization ellipse
		I,Q,U,V=stokes_vector # Separate the stokes components
		L = np.complex(Q,U) # L: Intensity (Complex) of Linear Polarization, V: Intensity of Circular Polarization, I: Total Intensity
		I_p = Q**2+U**2+V**2 # Intensity of polarized fraction of light
		# Calculate the major (A) and minor (B) axes, orientation of the polarization ellipse (theta) and handedness of polarization (h)
		
		A = np.sqrt((I_p+np.absolute(L))/2)
		B = np.sqrt((I_p-np.absolute(L))/2)
		theta=np.angle(L)/2
		h=np.sign(V)
		
		# Plot the ellipse
		t = np.linspace(0, 2 * np.pi, 50)
		a,b = A/2, B/2
		points = np.vstack((a * np.cos(t), b * np.sin(t), np.zeros(np.shape(t)))).T
		rotation=R.from_euler('z', theta)
		self.x, self.y, _ = rotation.apply(points).T
		
		print("(A,B), (L,absL), theta, (h) = ({0},{1}), ({2},{3}), {4},({5})".format(A,B, L,np.absolute(L), np.rad2deg(theta), h))
		if axes is None:
			fig = plt.figure(figsize=(9, 9), facecolor='AliceBlue')
			self.axes = fig.add_subplot(111, facecolor='Gainsboro', frame_on=True)
			plt.tight_layout()
		else:
			self.axes = axes
		
		self.axes.plot(self.x, self.y, color=self.color, linewidth='2.5')
		if h == -1:
			self.axes.arrow(self.x[7], self.y[7], self.x[8]-self.x[7], self.y[8]-self.y[7], color=self.color, length_includes_head=True, head_width=0.05, head_length=0.1)
		else:
			self.axes.arrow(self.x[7], self.y[7], self.x[7]-self.x[8], self.y[7]-self.y[8], color=self.color, length_includes_head=True, head_width=0.05, head_length=0.1)
		
		# Set and align axes labels
		self.axes.set_xlabel("$E_X$", fontsize=9)
		self.axes.set_ylabel("$E_Y$", fontsize=9, rotation=0)
		self.axes.xaxis.set_label_coords(1.025,0.51)
		self.axes.yaxis.set_label_coords(0.5, 1.0)
		self.axes.set_xlim((-0.51,0.51))
		self.axes.set_ylim((-0.51,0.51))
		
		# Place the origin at the center of the figure
		self.axes.spines['left'].set_position('center')
		self.axes.spines['bottom'].set_position('center')
		
		# Remove the outer box
		self.axes.spines['right'].set_color('none')
		self.axes.spines['top'].set_color('none')
		
		# Do not show ticks
		self.axes.tick_params(axis='both', which='both', length=0)
		plt.setp(self.axes.get_xticklabels(), visible=False)
		plt.setp(self.axes.get_yticklabels(), visible=False)
		
	def updatePoincareSphere(self):
		# print(x_points, y_points, z_points, markers)
		for xx, yy, zz, marker, color, text in zip(self.x_points, self.y_points, self.z_points, self.markers,
		                                           self.markerColors, self.markerTexts):
			self.axes.scatter(xx, yy, zz, color=color, s=self.markerSize, marker=marker, zorder=10)
			self.axes.text(xx + .1, yy + .1, zz + .1, text, color=color)

if __name__ == "__main__":
	polarizationEllipse=wx_PolarizationEllipse(stokes_vector=np.array((1,0,-1,0)))
	plt.show()