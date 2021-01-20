import numpy as np

from vispy import scene

from vispy.scene.visuals import Arrow, LinePlot, GridMesh, Line

from pyquaternion import Quaternion

from polarization_sources import SoP

class Retarder:
	def __init__(self, theta, delta, parent, radians=False, color='red', name='R0', draw=False):
		self.theta = theta
		self.delta = delta
		self.name = name
		self.color = color
		self.parent = parent
		self.quaternion = None
		
		self.position = np.array((1, 0, 0))
		
		if draw:
			self.__draw_visual()
		
	def __draw_visual(self):
		self.arrowStart = (0, 0, 0)
		self.arrowDirection = self.position - self.arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.retarder_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                            arrows=arrowHead,
		                            arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color, antialias=True,
		                            parent=self.parent)
		self.retarder_Arrow.transform = scene.transforms.MatrixTransform()
		self.retarder_Arrow.interactive=True
		
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parent,
		                            pos=self.position + (0.15 * self.arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		self.labelText.interactive=True
		
		self.retarderDirection = np.array([1, 0, 0])
		# Rotate the retarder visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * self.theta)
		
		self.__create_quaternion(self.retarderDirection, self.delta)
	
	def get_label(self):
		return self.name
	
	def get_color(self):
		return self.color
	
	def __create_quaternion(self, direction, angle):
		self.quaternion = Quaternion(axis=direction, radians=2 * angle)
	
	def __rotate(self, angle):
		self.retarder_Arrow.transform.rotate(angle, (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle, (0, 0, 1))
		q = Quaternion(axis=(0, 0, 1), degrees=angle)
		self.retarderDirection = q.rotate(np.array(self.retarderDirection))  # Update the rotation quaternion direction
	
	def retard(self, incoming_SoP, draw=False):
		"""
		Rotates the incoming polarization to outgoing polarization using quaternions and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after retardation
		"""
		result = self.quaternion.rotate(incoming_SoP.get_PolarizationVector())  # Calculate the result SoP by rotating the vector using quaternion
		result_SoP = SoP(np.append(np.array([1, ]), result), parent=self.parent, color=incoming_SoP.get_color(), name=incoming_SoP.get_label() + 'x' + self.name)
		
		if draw:
			self.__draw_retard(incoming_SoP)
		
		return result_SoP
	
	def __draw_retard(self, incoming_SoP):
		# Find the plane which is normal to the retardance vector and also in which the input SoP lies. Result SoP also lies in the same plane
		# https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
		dotProduct = np.dot(self.retarderDirection, self.retarderDirection)
		
		w = np.array((0, 0, 0))  # Line start point
		si = np.dot(self.retarderDirection, incoming_SoP.get_PolarizationVector()) / dotProduct
		center = w + si * self.retarderDirection  # Find the center of rotation which is located on this plane
		
		# To draw the arc of rotation of the retarder
		r = np.sqrt(np.sum((center - incoming_SoP.get_PolarizationVector()) ** 2))  # Radius is the distance from center to the incoming SoP
		
		# Find the line of intersection of the plane (Normal: retarder direction vector) and the XY plane (Normal: z-axis)
		# https://en.wikipedia.org/wiki/Intersection_curve#Intersection_line_of_two_planes
		direction_of_intersection = np.cross(self.retarderDirection, np.array((0, 0, 1)))
		arcStart = center + (-r) * direction_of_intersection  # Find the point towards the right side of the center (-r)
		circle_StartVector = arcStart - center
		
		# Find the SoP Vector to determine the starting angle of the arc
		SoP_vector = incoming_SoP.get_PolarizationVector() - center
		arc_StartAngle = np.arccos(
			np.dot(SoP_vector / np.linalg.norm(SoP_vector), circle_StartVector / np.linalg.norm(circle_StartVector)))
		if SoP_vector[2] < 0:  # If the SoP is in the lower hemisphere,
			arc_StartAngle = 2 * np.pi - arc_StartAngle  # determine the outer angle between the vectors
		
		# Debug Info
		# print("center=",self.retarderDirection, si, center)
		# scene.Text("◊", font_size=70, bold=True, color=self.color, parent=self.parent, pos=center)  # To display the center point
		# Line(np.array([center, arcStart]), connect='strip', method='gl', width=2, color=self.color, parent=self.parent)
		# print("line=", direction_of_intersection)
		# print("Angle=", arcStart, circle_StartVector, SoP_vector, np.rad2deg(arc_StartAngle))#, np.rad2deg(arcAngle))
		
		# Draw the arc using the above data
		t = np.linspace(arc_StartAngle, arc_StartAngle + np.deg2rad(2 * self.delta), 100)
		y = r * np.cos(t)
		z = r * np.sin(t)
		x = np.zeros(y.size)
		arc = LinePlot((x, y, z), width=15, color=self.color, parent=self.parent)
		arc.transform = scene.transforms.MatrixTransform()
		arc.transform.rotate(2 * self.theta, (0, 0, 1))
		arc.transform.translate(center)
		
		# Draw arrow head at the center (51st point) of the above arc to indicate the direction of rotation
		arrowHead = np.array([(x[50], y[50], z[50], x[51], y[51],
		                       z[51])])  # Arrow direction, position -Direction determined by the 50th point
		arrowSize = 5.
		if self.delta < np.deg2rad(20):
			arrowSize = 3.
		# The pos parameter is simply a line of short length same as that of the arrowhead
		arrow = Arrow(pos=np.array([(x[50], y[50], z[50]), (x[51], y[51], z[51])]), color=self.color, method='gl',
		              width=arrowSize, arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color,
		              antialias=True, parent=self.parent)
		arrow.transform = scene.transforms.MatrixTransform()
		arrow.transform.rotate(2 * self.theta, (0, 0, 1))
		arrow.transform.translate(center)


class Polariser:
	def __init__(self, theta, parent, radians=False, color='purple', name='P0', draw=False):
		self.theta = theta
		self.name = name
		self.color = color
		self.parent = parent
		
		self.position = np.array((1, 0, 0))
		
		if draw:
			self.__draw_Polariser()
		
	def __draw_Polariser(self):
		self.arrowStart = (0, 0, 0)
		self.arrowDirection = self.position - self.arrowStart
		# Derive arrow position from the point and direction of arrow from the tangent (or direction cosine) of the line at the point
		arrowHead = np.array([(0, 0, 0, 1, 0, 0)])  # Arrow direction, position
		self.polariser_Arrow = Arrow(pos=np.array([(0, 0, 0), self.position]), color=self.color, method='gl', width=5.,
		                             arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0, arrow_color=self.color,
		                             antialias=True, parent=self.parent)
		self.polariser_Arrow.transform = scene.transforms.MatrixTransform()
		self.polariser_Arrow.interactive=True
		
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=self.parent,
		                            pos=self.position + (0.15 * self.arrowDirection))
		self.labelText.transform = scene.transforms.MatrixTransform()
		self.labelText.interactive=True
		
		self.polariserDirection = np.array([1, 0, 0])
		# Rotate the polariser visual after creating the arrow and head from the origin to the proper position
		self.__rotate(2 * self.theta)
	
	def get_label(self):
		return self.name
	
	def get_color(self):
		return self.color
	
	def __rotate(self, angle):
		self.polariser_Arrow.transform.rotate(angle, (0, 0, 1))  # Rotate on the XY plane (about Z axis)
		self.labelText.transform.rotate(angle, (0, 0, 1))
		q = Quaternion(axis=(0, 0, 1), degrees=angle)
		self.polariserDirection = q.rotate(
			np.array(self.polariserDirection))  # Update the rotation quaternion direction
	
	def polarise(self, incoming_SoP, draw=False):
		"""
		Polarises the incoming polarization to outgoing polarization and displays the same on Poincare sphere
		:param incoming_SoP: incoming state of polarization
		:return: resulting state of polarization after polarisation
		"""
		# gamma is the angle between the orientation of the polariser and orientation of the incoming SoP
		gamma = np.arccos(np.dot(self.polariserDirection, incoming_SoP.get_PolarizationVector()))
		two_psi = np.arctan(self.polariserDirection[1] / self.polariserDirection[0])
		if np.abs(self.theta) > 45:
			two_psi += np.pi
		I = np.cos(gamma / 2) ** 2
		# From the basic relations for S0, S1, S2, S3 given in https://en.wikipedia.org/wiki/Stokes_parameters
		# DoP=1, two_Xi=0, the relations simplify
		result_polarization_vector = np.array((I * np.cos(two_psi), I * np.sin(two_psi), 0))
		result_SoP = SoP(np.append([I], result_polarization_vector), parent=self.parent, color=incoming_SoP.get_color(),
		                 name=incoming_SoP.get_label() + '+' + self.name)
		# print("In Polariser: gamma, 2Psi, result=",np.rad2deg([gamma, two_psi]), result_polarization_vector)
		
		if draw:
			self.__draw_polarise(incoming_SoP, result_polarization_vector)
		
		return result_SoP
	
	def __draw_polarise(self, incoming_SoP, result_polarization_vector):
		""" Draw the transformation visual """
		# Calculate mid point for drawing the arrow head
		mid_point = (incoming_SoP.get_PolarizationVector() + result_polarization_vector) / 2
		arrowHead = np.array([np.append(incoming_SoP.get_PolarizationVector(), mid_point)])  # Arrow direction, position
		Arrow(pos=np.array([incoming_SoP.get_PolarizationVector(), result_polarization_vector]), color=self.color,
		      method='gl', width=5., arrows=arrowHead, arrow_type="angle_30", arrow_size=5.0,
		      arrow_color=self.color, antialias=True, parent=self.parent)
		
