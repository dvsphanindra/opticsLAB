import numpy as np

from vispy import scene

class SoP:
	def __init__(self, stokes_vector, parent, name="P0", color='red'):
		self.stokes_vector = stokes_vector
		self.intensity = self.stokes_vector[0]
		self.polarizationVector = self.stokes_vector[1:]  # / self.stokes_vector[0] # TODO: To be verified
		self.name = name
		self.color = color
		self.validate_StokesVector()
		
		self.labelObject=scene.Text("•", font_size=100, bold=True, color=color, parent=parent, pos=self.polarizationVector)
		self.labelText = scene.Text(self.name, font_size=50, bold=True, color=self.color, parent=parent,
		                            pos=self.polarizationVector + (0.15 * self.polarizationVector))
		self.labelObject.interactive=True
		self.labelText.interactive=True
	
	def get_PolarizationVector(self):
		return self.polarizationVector
	
	def get_label(self):
		return self.name
	
	def get_color(self):
		return self.color
	
	def get_intensity(self):
		return self.intensity
	
	def get_DegreeOfPolarization(self):
		return np.sqrt(np.sum(np.square(self.polarizationVector))) / self.stokes_vector[0]
	
	def validate_StokesVector(self):
		#
		assert np.sqrt(np.sum(np.square(self.polarizationVector))) <= self.stokes_vector[0], "Irregular Stokes Vector: S0, vector, square, sum of square: {0}, {1}, {2}, {3}".format(self.stokes_vector[0], self.polarizationVector, np.square(self.polarizationVector), np.sum(np.square(self.polarizationVector)))
# def get_ellipticity(self):
# 	return np.tan(np.pi/4-self.Xi)
# def get_orientation(self):
# 	return self.theta
