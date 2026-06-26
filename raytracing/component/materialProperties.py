import numpy as np

catalogue = {  "Air": ([0.0,0.0,0.0],[0.0,0.0,0.0]),
					"BK7" : ([1.03961212, 0.231792344, 1.01046945], [6.00069867E-3, 2.00179144E-2, 103.560653]),
					"sapphire" : ([1.43134930, 0.65054713, 5.3414021], [5.2799261E-3, 1.42382647E-2, 325.017834]),
					"sapphire-EWave" : ([1.5039759, 0.55069141, 6.5927379], [5.4804112E-3, 1.47994281E-2, 402.89514]),
					"fused silica" : ([0.696166300, 0.407942600, 0.897479400], [4.67914826E-3, 1.35120631E-2, 97.9340025]),
                    "MgF" : ([0.48755108, 0.39875031, 2.3120353], [0.001882178, 0.008951888, 566.13559]),
				   "N-SK4": ([1.32993741, 0.228542996, 0.988465211],
					   [0.00716874107, 0.0246455892, 100.886364]),

				   "N-SF2": ([1.47343127, 0.163681849, 1.36920899],
					   [0.0109019098, 0.0585683687, 127.404933]),
					"F2": ([1.34533359, 0.209073176, 0.937357162],
						   [0.00997743871, 0.0470450767, 111.886764])
				   }

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
