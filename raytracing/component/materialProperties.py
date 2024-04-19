import numpy as np

catalogue = {  "Air": ([0.0,0.0,0.0],[0.0,0.0,0.0]),
					"BK7" : ([1.03961212, 0.231792344, 1.01046945], [6.00069867E-3, 2.00179144E-2, 103.560653]),
					"sapphire" : ([1.43134930, 0.65054713, 5.3414021], [5.2799261E-3, 1.42382647E-2, 325.017834]),
					"sapphire-EWave" : ([1.5039759, 0.55069141, 6.5927379], [5.4804112E-3, 1.47994281E-2, 402.89514]),
					"fused silica" : ([0.696166300, 0.407942600, 0.897479400], [4.67914826E-3, 1.35120631E-2, 97.9340025]),
                    "MgF" : ([0.48755108, 0.39875031, 2.3120353], [0.001882178, 0.008951888, 566.13559])}

def refractiveIndex(wavelength, medium="BK7"):
	"""From Sellmeier Equation
	:param wavelength: Specify in μm (0.2 <= wavelength <= 2)
	:param medium: The material of the medium. Ex: "BK7".
	:return: The refractive index at the given wavelength will be calculated and returned
	"""
	assert 0.2<= wavelength <= 2, "Wavelength is not in the range [0.2, 2]. Specify in μm"
	
	B,C = catalogue[medium]
	w2 = wavelength*wavelength
	n = np.sqrt(1 + ((B[0]*w2/(w2-C[0])) + (B[1]*w2/(w2-C[1])) + (B[2]*w2/(w2-C[2]))))
	# print(n)
	return n
