import numpy as np

import sys

from vispy import scene

import vispy as vispy

from raytracing.miscellaneous import XYZAxis_Labeled

from vispy.scene.visuals import Arrow, SurfacePlot, Line, Ellipse, LinePlot, Mesh, GridMesh

from vispy.geometry import curves, MeshData, create_grid_mesh

from vispy.color import Color

from scipy.spatial.transform import Rotation

from pyquaternion import Quaternion

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})

class Coordinate_Axes(XYZAxis_Labeled):
	def __init__(self, parent, labels=("S1", "S2", "S3"), labels_on=True):
		if not labels_on:
			labels=("", "", "")
		XYZAxis_Labeled.__init__(self, parent=parent, labels=labels)

class PoincareSphere:
	def __init__(self, parent, radius=1.0, center=(0.0, 0.0, 0.0), color=Color((0.3, 0.3, 1, 0.4))):
		"""
		Creates the data of a sphere whose center, and radius are given as inputs
		"""
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
		
		Coordinate_Axes(parent=parent)
		# SurfacePlot(x_grid, y_grid, z_grid, parent=parent, color=color)
		mesh=GridMesh(x_grid, y_grid, z_grid, parent=parent, color=color)
		# mesh=MeshData(create_grid_mesh(x_grid, y_grid, z_grid))
		# mesh.cmap='viridis'
		# mesh.shininess=0.5
		mesh.ambient_light_color=Color((0.3, 0.3, 1, 0.1))
		mesh.light_dir=np.array((0,0,1))
		mesh.shading='flat'
		# print("Sphere drawn", mesh.get_face_normals())

class SoP:
	def __init__(self, stokes_vector, parent, label="P0", color='red'):
		self.stokes_vector=stokes_vector
		self.intensity=self.stokes_vector[0]
		self.polarizationVector= self.stokes_vector[1:] #/ self.stokes_vector[0] # TODO: To be verified
		self.label=label
		self.color=color
		self.validate_StokesVector()
		# •◊×
		scene.Text("•", font_size=100, bold=True, color=color, parent=parent, pos=self.polarizationVector)
		self.labelText=scene.Text(self.label, font_size=50, bold=True, color=self.color, parent=parent, pos=self.polarizationVector + (0.15 * self.polarizationVector))
		
	def get_PolarizationVector(self):
		return self.polarizationVector
	def get_label(self):
		return self.label
	def get_color(self):
		return self.color
	def get_intensity(self):
		return self.intensity
	def get_DegreeOfPolarization(self):
		return np.sqrt(np.sum(np.square(self.polarizationVector)))/self.stokes_vector[0]
	def validate_StokesVector(self):
		#
		assert np.sqrt(np.sum(np.square(self.polarizationVector)))<=self.stokes_vector[0], "Irregular Stokes Vector: S0, vector, square, sum of square: {0}, {1}, {2}, {3}".format(self.stokes_vector[0], self.polarizationVector, np.square(self.polarizationVector), np.sum(np.square(self.polarizationVector)))
	# def get_ellipticity(self):
	# 	return np.tan(np.pi/4-self.Xi)
	# def get_orientation(self):
	# 	return self.theta
	
class Retarder:
	def __init__(self, theta, delta, parent, radians=False, color='red', label='R0'):
		self.theta=theta
		self.delta=delta
		self.label=label
		self.color=color
		self.parent=parent
		
		self.position = np.array((1,0,0))
		self.arrowStart = (0,0,0)
		self.arrowDirection = self.position - self.arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.retarder_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5., arrows=arrowHead,
		                            arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True, parent=self.parent)
		self.retarder_Arrow.transform=scene.transforms.MatrixTransform()
		
		self.labelText=scene.Text(self.label, font_size=50, bold=True, color=color, parent=self.parent, pos=self.position+(0.15*self.arrowDirection))
		self.labelText.transform=scene.transforms.MatrixTransform()
		
		self.retarderDirection=np.array([1, 0, 0])
		# Rotate the retarder visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2*theta)
		
		self.__create_quaternion(self.retarderDirection, self.delta)
		
	def get_label(self):
		return self.label
	
	def get_color(self):
		return self.color
		
	def __create_quaternion(self, direction, angle):
		self.quaternion = Quaternion(axis=direction, degrees=2*angle)
		
	def __rotate(self, angle):
		self.retarder_Arrow.transform.rotate(angle, (0, 0, 1)) # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle,(0,0,1))
		q = Quaternion(axis=(0, 0, 1), degrees=angle)
		self.retarderDirection=q.rotate(np.array(self.retarderDirection)) # Update the rotation quaternion direction
		
	def retard(self, incoming_SoP):
		"""
		Rotates the incoming polarization to outgoing polarization using quaternions and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after retardation
		"""
		result=self.quaternion.rotate(incoming_SoP.get_PolarizationVector()) # Calculate the result SoP by rotating the vector using quaternion
		result_SoP=SoP(np.append(np.array([1, ]), result), parent=self.parent, color=incoming_SoP.get_color(), label=incoming_SoP.get_label()+'x'+self.label)
		
		# Find the plane which is normal to the retardance vector and also in which the input SoP lies. Result SoP also lies in the same plane
		# https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
		dotProduct = np.dot(self.retarderDirection, self.retarderDirection)
		
		w = np.array((0,0,0)) # Line start point
		si = np.dot(self.retarderDirection, incoming_SoP.get_PolarizationVector()) / dotProduct
		center = w + si * self.retarderDirection
		print("center=",self.retarderDirection, si, center)
		# scene.Text("◊", font_size=70, bold=True, color=self.color, parent=self.parent, pos=center) # To display the center point
		
		# Draw the arc of rotation of the quaternion
		r = np.sqrt(np.sum((center-incoming_SoP.get_PolarizationVector())**2)) # Radius is the distance from center to the incoming SoP
		# print(self.position, incoming_SoP.get_PolarizationVector(), r)
		angle_of_circle=np.arccos(np.dot(self.retarderDirection, incoming_SoP.get_PolarizationVector()))
		
		# Find the starting direction of circle to determine where to start the arc in the visual
		q = Quaternion(axis=(0, 0, 1), radians=angle_of_circle) # Axis is z-axis (S3 in the visual)
		start_of_circle=q.rotate(np.array(self.retarderDirection))
		start_vector=start_of_circle-center
		SoP_vector=incoming_SoP.get_PolarizationVector()-center
		angle_between_vectors=np.arccos(np.dot(start_vector/np.linalg.norm(start_vector), SoP_vector/np.linalg.norm(SoP_vector)))
		angle_between_vectors = np.sign(SoP_vector[2]) * angle_between_vectors # Multiply with the sign of the S3 coordinate to determine if the rotation is in the lower hemisphere
		print("Angle=", start_vector, SoP_vector, np.rad2deg(angle_between_vectors), np.rad2deg(angle_of_circle))
		
		# Draw the arc using the above data
		t = np.linspace(angle_between_vectors, angle_between_vectors+np.deg2rad(2 * self.delta), 100)
		y = r * np.cos(t)
		z = r * np.sin(t)
		x = np.zeros(y.size)
		arc = LinePlot((x, y, z), width=15, color=self.color, parent=self.parent)
		arc.transform = scene.transforms.MatrixTransform()
		arc.transform.rotate(2 * self.theta, (0, 0, 1))
		arc.transform.translate(center)
		
		# Draw arrow head at the center (51st point) of the above arc to indicate the direction of rotation
		arrowHead = np.array([(x[50],y[50],z[50],x[51],y[51],z[51])])  # Arrow direction, position -Direction determined by the 50th point
		arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5., arrows=arrowHead,
		              arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True, parent=self.parent)
		arrow.transform=scene.transforms.MatrixTransform()
		arrow.transform.rotate(2 * self.theta, (0, 0, 1))
		arrow.transform.translate(center)
		return result_SoP


class Polariser:
	def __init__(self, theta, parent, radians=False, color='purple', label='P0'):
		self.theta = theta
		self.label = label
		self.color = color
		self.parent = parent
		
		self.position = np.array((1, 0, 0))
		self.arrowStart = (0, 0, 0)
		self.arrowDirection = self.position - self.arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.polariser_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                            arrows=arrowHead,
		                            arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True,
		                            parent=self.parent)
		self.polariser_Arrow.transform = scene.transforms.MatrixTransform()
		
		self.labelText = scene.Text(self.label, font_size=50, bold=True, color=color, parent=self.parent,
		                            pos=self.position + (0.15 * self.arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		
		self.polariserDirection = np.array([1, 0, 0])
		# Rotate the polariser visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * theta)
	
	def get_label(self):
		return self.label
	
	def get_color(self):
		return self.color
	
	def __rotate(self, angle):
		self.polariser_Arrow.transform.rotate(angle, (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle, (0, 0, 1))
		q = Quaternion(axis=(0, 0, 1), degrees=angle)
		self.polariserDirection = q.rotate(np.array(self.polariserDirection))  # Update the rotation quaternion direction
	
	def polarise(self, incoming_SoP):
		"""
		Polarises the incoming polarization to outgoing polarization and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after polarisation
		"""
		# gamma is the angle between the orientation of the polariser and orientation of the incoming SoP
		gamma=np.arccos(np.dot(self.polariserDirection, incoming_SoP.get_PolarizationVector()))
		two_psi=np.arctan(self.polariserDirection[1]/self.polariserDirection[0])
		if np.abs(self.theta)>45:
			two_psi+=np.pi
		I=np.cos(gamma / 2) ** 2
		# From the basic relations for S0, S1, S2, S3 given in https://en.wikipedia.org/wiki/Stokes_parameters
		# DoP=1, two_Xi=0, the relations simplify
		result_polarization_vector=np.array((I*np.cos(two_psi), I*np.sin(two_psi), 0))
		result_SoP = SoP(np.append([I],result_polarization_vector), parent=self.parent, color=incoming_SoP.get_color(), label=incoming_SoP.get_label() + 'x' + self.label)
		# print("In Polariser: gamma, 2Psi, result=",np.rad2deg([gamma, two_psi]), result_polarization_vector)
		
		# Draw the transformation visual
		# Calculate mid point for drawing the arrow head
		mid_point=(incoming_SoP.get_PolarizationVector()+result_polarization_vector)/2
		arrowHead = np.array([np.append(incoming_SoP.get_PolarizationVector(), mid_point)]) # Arrow direction, position
		print("arrow=",arrowHead)
		Arrow(pos=np.array([incoming_SoP.get_PolarizationVector(), result_polarization_vector]), color=self.color, method='gl', width=5.,
		                             arrows=arrowHead,
		                             arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True,
		                             parent=self.parent)
		return result_SoP


canvas = scene.SceneCanvas(keys='interactive')
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='z', fov=30)

canvas.bgcolor = Color(color="lightsteelblue", alpha=0.5)
retarder1 = Retarder(30, 35, parent=view.scene, color='teal', label='R0')

sop1=SoP(np.array((1,0,1,0)), parent=view.scene, color='white', label="SoP1")
sop2=retarder1.retard(sop1)

polariser1=Polariser(20, parent=view.scene, color='yellow', label="P1")
out_SoP=polariser1.polarise(sop2)
print("SoP out= ", out_SoP.stokes_vector, "DoP= ",out_SoP.get_DegreeOfPolarization())

sphere = PoincareSphere(parent=view.scene)


if __name__ == '__main__':
	canvas.show()
	if sys.flags.interactive == 0:
		vispy.app.run()
