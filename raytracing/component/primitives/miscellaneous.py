import numpy as np
from .primitive_point import Primitive_point

def deg2DC(angles, decimals=5):
	"""
	Converts the input angles into direction cosines and rounds them to avoid floating point errors when used in further processing
	:param angles: An np.array or tuple of angles in degrees
	:param decimals: The number of decimals to which the output direction cosines should be rounded to. Default: 5
	:return: Direction cosines corresponding to the input angles
	"""
	dc = np.around(np.cos(np.deg2rad(np.array(angles))), decimals=decimals)
	# print("dc, sum=",dc, np.around(np.sum(dc**2)))
	assert np.around(np.sum(dc**2), decimals=3) == 1, "Invalid angles for Direction Cosines. Sum!=1. Set dc=True if passing dc instead of angles"
	return dc

def dc2deg(dc):
	# norm = np.linalg.norm(dc)
	return np.arccos(dc/np.linalg.norm(dc))

def dc_from_points(point1, point2, angles=False):
	"""
	Calculates Direction Cosines of the line drawn between the two points.
	:param point1: point1 on the line. Can be a Point object or numpy array.
	:param point2: point2 on the line. Can be a Point object or numpy array.
	:param angles: to return the dc in direction angles
	:return: Direction Cosines of the line between the two points
	"""
	p1 = point1.get_coordinates() if isinstance(point1, Primitive_point) else np.array(point1)
	p2 = point2.get_coordinates() if isinstance(point2, Primitive_point) else np.array(point2)
	direction_ratios = p2 - p1
	dc = direction_ratios / np.linalg.norm(direction_ratios)
	if angles: return np.rad2deg(np.arccos(dc))
	else: return dc

def calculate_DirectionAngles(dc_angle1, dc_angle2):
	"""
	Determines the third Direction Cosine Angle if any of the two of the angles are given
	:param dc_angle1: Direction Cosine1 in degrees
	:param dc_angle2: Direction Cosine2 in degrees
	:return: Third Direction Cosine in degrees
	"""
	dc = np.around(1.0 - np.cos(np.deg2rad(dc_angle1))**2 - np.cos(np.deg2rad(dc_angle2))**2, decimals=3)
	assert dc >= 0, "Invalid angles for Direction Angles: l={0:5.3f} for {1}, m={2:5.3f} for {3}".format(np.cos(np.deg2rad(dc_angle1))**2, dc_angle1, np.cos(np.deg2rad(dc_angle2))**2, dc_angle2)
	return np.around(np.rad2deg(np.arccos(np.sqrt(dc))),decimals=3) # Calculate angle and return

