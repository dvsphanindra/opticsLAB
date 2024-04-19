import numpy as np
from numpy import pi as PI

np.set_printoptions(precision=4, suppress=True)


class Polarimeter:
	"""
		Generic Polarimeter object containing the configuration of the components, modulation parameters and optimization parameters
	"""
	
	def __init__(self, component=None):
		self.componentList = list()
		self.modulationParameterList = list()  # List of functions to be given as parameters
		self.modulationParameterDict = dict()
		self.mueller = np.identity(4)  # Create an identity matrix of size 4 for initialization
		self.modulation_matrix = None
		self.demodulation_matrix = None
		self.initial_params = list()
		self.optimization_parameterList = list()
		self.optimization_parameterDict = dict()
		self.efficiencies = np.empty((0, 4))  # Create an empty array to stack with I,Q,U,V efficiencies later
		self.wavelength_range = (6000, 16000, 100)
		self.optimization_parameterBounds = list()
		self.opt_parameter_bounds = list()
		self.modulation_scheme = None
		
		self.wavelengths = np.arange(self.wavelength_range[0], self.wavelength_range[1] + 1, self.wavelength_range[2])
		
		if component is not None:
			self.add_component(component)
	
	def add_component(self, component, modulation_parameter=None, optimization_parameters=(), opt_parameter_bounds=()):
		assert modulation_parameter in ("theta", "delta",
		                                None), "Unknown modulation parameter. Parameter should be one among 'theta' or 'delta' or 'None'"
		assert all(e in ("theta", "delta") for e in
		           optimization_parameters), "Unknown optimization parameter encountered. Parameters should be either 'delta' or 'theta'"
		if optimization_parameters.__len__() != 0:
			if opt_parameter_bounds.__len__() == 0:
				self.opt_parameter_bounds += [0, 2 * PI] * optimization_parameters.__len__()
			else:
				assert optimization_parameters.__len__() == opt_parameter_bounds.__len__(), "Each optimization parameter should have a corresponding bound: {0},{1}".format(
					optimization_parameters.__len__(), opt_parameter_bounds.__len__())
				self.opt_parameter_bounds += list(opt_parameter_bounds)
		
		self.componentList.append(component)
		
		if modulation_parameter == "delta":
			assert component.get_Type() == "Retarder", "Component '{0}' has no parameter 'delta'".format(
				component.get_Name())
			self.modulationParameterList.append(component.set_Retardance)
			self.initial_params.append(component.get_Retardance())
			self.modulationParameterDict[component.get_Name()] = u"\u03B4"
		elif modulation_parameter == "theta":
			self.modulationParameterList.append(component.set_OrientationAngle)
			self.initial_params.append(component.get_OrientationAngle())
			self.modulationParameterDict[component.get_Name()] = u"\u03B8"
		
		if "delta" in optimization_parameters:
			assert component.get_Type() == "Retarder", "Component '{0}' has no parameter 'delta'".format(
				component.get_Name())
			self.optimization_parameterList.append(component.set_Retardance)
			if component.get_Name() not in self.optimization_parameterDict:
				self.optimization_parameterDict[component.get_Name()] = u"\u03B4"
			else:
				self.optimization_parameterDict.update(
					self.optimization_parameterDict[component.get_Name()] + u',\u03B4')
		if "theta" in optimization_parameters:
			self.optimization_parameterList.append(component.set_OrientationAngle)
			if component.get_Name() not in self.optimization_parameterDict:
				self.optimization_parameterDict[component.get_Name()] = u"\u03B8"
			else:
				self.optimization_parameterDict.update(
					{component.get_Name(): self.optimization_parameterDict[component.get_Name()] + u',\u03B8'})
	
	def get_ModulationParameters(self):
		return self.modulationParameterList
	
	def get_OptimizationParameters(self):
		return self.optimization_parameterList
	
	def get_OptimizationParameterBounds(self):
		return self.opt_parameter_bounds
	
	def get_modulationParameterCount(self):
		return self.modulationParameterList.__len__()
	
	def get_optimizationParameterCount(self):
		return self.optimization_parameterList.__len__()
	
	def remove_component(self, component):
		self.componentList.remove(component)
	
	def print_components(self):
		print("----------------------------------------------------------------------------------------")
		print("Polarimeter configuration:\n", " => ".join(c.get_Name() for c in self.componentList))
		print("------------------------------------Component Details-----------------------------------")
		for component in self.componentList:
			component_type = component.get_Type()
			if component_type == 'Retarder':
				print(
					u"|{0:20s}| \u03B8: {1:<7s}  | \u03B4: {2:<7s}  | Mod Params: {3:<4s} | Opt Params: {4:<4s} |".format(
						component.get_Name(), str(component.get_OrientationAngle()), str(component.get_Retardance()),
						self.modulationParameterDict.get(component.get_Name(), 'None'),
						self.optimization_parameterDict.get(component.get_Name(), 'None')))
			else:
				print(u"|{0:20s}| \u03B8: {1:<7s}  |{2:13s}| Mod Params: {3:<4s} | Opt Params: {4:<4s} |".format(
					component.get_Name(), str(component.get_OrientationAngle()), ' ',
					self.modulationParameterDict.get(component.get_Name(), 'None'),
					self.optimization_parameterDict.get(component.get_Name(), 'None')))
	
	def get_MuellerMatrix(self):
		return self.mueller
	
	def calculate_MuellerMatrix(self):
		self.mueller = np.identity(4)  # Initialize the mueller matrix
		for component in reversed(self.componentList):
			# print(component.get_Name(), component.get_MuellerMatrix())
			self.mueller = np.array(np.matrix(self.mueller) * np.matrix(component.get_MuellerMatrix()))
	
	def set_ModulationScheme(self, scheme, radians=False):
		if not radians:
			scheme = np.deg2rad(scheme)
		else:
			scheme = np.array(scheme)
		assert self.modulationParameterList.__len__() == scheme.shape[
			1], "Modulation scheme should have the same number of columns as the number of modulation parameters"
		self.modulation_scheme = scheme
	
	def set_wavelength_range(self, wavelength_range):
		self.wavelength_range = wavelength_range
		self.wavelengths = np.arange(self.wavelength_range[0], self.wavelength_range[1] + 1, self.wavelength_range[2])
	
	def get_wavelength_range(self):
		return self.wavelength_range
	
	def get_ModulationScheme(self):
		return self.modulation_scheme
	
	def modulate_polarimeter(self, wavelength=6563):
		assert self.modulation_scheme is not None, "Cannot modulate: modulation scheme is not set."
		assert self.modulationParameterList.__len__() == self.modulation_scheme.shape[
			1], "Cannot modulate: modulation scheme should have the same number of columns as the number of modulation parameters"
		self.__modulate__(self.modulationParameterList, wavelength)
	
	def __modulate__(self, params, wavelength):
		# print("--------Modulation-------------")
		self.modulation_matrix = np.zeros((4, 4))
		
		# Calculate the retardance at the operating wavelength for all the retarders
		for component in self.componentList:
			if component.get_Type() == "Retarder":
				component.set_OperatingWavelength(wavelength)
		
		for count, row in enumerate(self.modulation_scheme):
			for func, value in zip(params, row):
				func(value, radians=True)  # The angles are already converted into radians
			self.calculate_MuellerMatrix()
			# print("Modulation matrix in Step {0}, with modulation parameters: ".format(count+1), np.rad2deg(row), ":\n", self.mueller)
			self.modulation_matrix[count, :] = self.mueller[0, :]  # Collect the row corresponding to intensity
		# print("-----Modulation matrix--------")
		# print(self.modulation_matrix)
		self.demodulation_matrix = np.linalg.pinv(self.modulation_matrix)  # Calculate the Moore-Penrose pseudo inverse
# print("------Demodulation matrix--------")
# print(self.demodulation_matrix)
