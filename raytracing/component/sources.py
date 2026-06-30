import numpy as np
from scipy.spatial.transform import Rotation as R
from .miscellaneous_components import Z_AXIS_DIRECTION, display_point
from .primitives.miscellaneous import deg2DC
from .primitives.lineVector import LineVector
from .materialProperties import refractiveIndex
from .primitives.miscellaneous import dc_from_points
from .primitives.primitive_point import Primitive_point
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point




class Ray(LineVector):
	def __init__(self, startPoint, rayDirection=None, name=None, dc=False, wavelength=0.55, length=1.0, color="green",
	             parentCanvas=None):
		"""
		Creates a ray which propagates from the rayStart point in the direction given by rayDirection
		:param startPoint: Starting point of the ray passed as a Point object
		:param rayDirection: direction cosines of the ray or tilts in degrees with respect to opticsLab coordinates
		:param: name: Name of the ray for debugging purposes (optional)
		:param: dc: If the rayDirection is specified as dc or not. Default: False, that is direction is specified as angles in degrees
		:param wavelength: wavelength of the ray in μm.
		:param length: Length of the ray (optional). Default is unit vector
		:param color: Color to be shown when the ray is being visualized (Optional)
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		"""

		# TODO select color based on wavelength
		self.wavelength = wavelength
		assert isinstance(startPoint, Point), "Ray class: startPoint is not a Point object"
		self.startPoint = startPoint
		super().__init__(startPoint.get_coordinates(), rayDirection, name, dc, length, color, parentCanvas=parentCanvas)

	"""def set_x_angle(self,angle, radians=False):
		angle = angle if radians else np.deg2rad(angle)
		self.direction[0] = np.cos(angle)
		self.update_Vector(self.lineEnd)
		# x = np.cos(angle)
		# z = np.sqrt(1-x^2)
		# self.direction = np.ar

	def set_y_angle(self,angle, radians=False):
		angle = angle if radians else np.deg2rad(angle)
		self.direction[1] = np.cos(angle)

	def set_z_angle(self,angle, radians=False):
		angle = angle if radians else np.deg2rad(angle)
		self.direction[2] = np.cos(angle)"""

	def rotate_aboutX(self, angle):
		self.rotate(np.array((1, 0, 0)), angle)
	
	def rotate_aboutY(self, angle):
		self.rotate(np.array((0, 1, 0)), angle)
	
	def rotate_aboutZ(self, angle):
		self.rotate(np.array((0, 0, 1)), angle)
	
	def get_StartPoint(self):
		return self.lineStart_point
	
	def get_Direction(self):
		return self.get_Direction_Cosines()
	
	def get_Wavelength(self):
		return self.wavelength
	
	def get_Color(self):
		return self.color
	
	def update_Ray(self, point):
		self.update_Vector(point)

	def calculate_ReflectedRay(self, surface):
		"""
        Delegates the reflection math to the target surface.
        """
		return surface.calculate_ReflectedRay(self)

	def calculate_RefractedRay(self, surface):
		"""
		Delegates the reflection math to the target surface.
		"""
		return surface.calculate_RefractedRay(self)
	
	# def calculate_RefractedRay(self, surface):
	# 	# intersectionPoint = surface.calculate_RayIntersection(ray=self)
	# 	# if intersectionPoint is None:
	# 	# 	# Display a 'no intersection warning' marker on the ray
	# 	# 	fail_mark = self.lineStart_point + self.direction * 0.5
	# 	# 	display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
	# 	# 	return None
	#
	# 	result = surface.calculate_RayIntersection(ray=self)  # JAY edit
	#
	# 	print(result)
	#
	# 	if result is None:
	# 		fail_mark = self.lineStart_point + self.direction * 0.5
	# 		display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
	# 		return None
	#
	# 	intersectionPoint, rayColor = result  # JAy edit 88-92
	#
	# 	n1 = refractiveIndex(self.get_Wavelength(), surface.mediumBefore)
	# 	n2 = refractiveIndex(self.get_Wavelength(), surface.mediumAfter)
	#
	# 	surfaceNormalDirection = surface.calculate_normalDirection(intersectionPoint)
	#
	# 	r = n1 / n2  # n1 / n2  # TODO: to verify this formula why it is reverse
	# 	print("dir: ", self.get_Direction(), "surfDir: ", surfaceNormalDirection)
	# 	dotProduct = -np.dot(surfaceNormalDirection, self.get_Direction())
	# 	horizontalComp = 1 - (r * r * (1 - dotProduct ** 2))
	# 	assert horizontalComp >= 0, "Error in refraction (negative value under root):" + "normalDir={0}, dot product={1}, r={2}, [1-dot]={3}, horizontalComp**2={4}".format(
	# 		str(surfaceNormalDirection), dotProduct, r, 1 - dotProduct ** 2, horizontalComp)
	#
	# 	#refractedRayDir = (r * np.cross(self.normal, a)) - (self.normal * np.sqrt(1 - (r * r * np.dot(b, b))))
	# 	# refractedRayDir = np.sqrt(horizontalComp) * surfaceNormalDirection + r * (
	# 	# 		self.get_Direction() - dotProduct * surfaceNormalDirection)                 #DVS original
	#
	# 	refractedRayDir = (r * self.get_Direction()) + ((r * dotProduct - np.sqrt(horizontalComp)) * surfaceNormalDirection) # jay edit
	#
	# 	#intersectionPoint=surface.transform(intersectionPoint)
	# 	#refractedRayDir=surface.transform(refractedRayDir)
	# 	display_point(intersectionPoint, marker='o', color=self.color, parentCanvas=self.parentCanvas)
	# 	self.update_Ray(intersectionPoint)  # Extend the ray to meet the surface
	# 	return Ray(Point(intersectionPoint), refractedRayDir, wavelength=self.get_Wavelength(), color=self.get_Color(),
	# 	           dc=True, parentCanvas=self.parentCanvas)

	# def calculate_RefractedRay(self, surface):
	# 	result = surface.calculate_RayIntersection(ray=self)
	#
	# 	if result is None:
	# 		fail_mark = self.lineStart_point + self.direction * 0.5
	# 		display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
	# 		return None
	#
	# 	intersectionPoint, rayColor = result
	#
	# 	incidentDir = np.array(self.get_Direction(), dtype=float)
	# 	print("beforwfhks",incidentDir)
	# 	incidentDir = incidentDir / np.linalg.norm(incidentDir)
	# 	print("afterjhdikdf",incidentDir)
	#
	# 	normalDir = np.array(surface.calculate_normalDirection(intersectionPoint), dtype=float)
	# 	normalDir = normalDir / np.linalg.norm(normalDir)
	#
	# 	n1 = refractiveIndex(self.get_Wavelength(), surface.mediumBefore)
	# 	n2 = refractiveIndex(self.get_Wavelength(), surface.mediumAfter)
	#
	# 	cos_i = -np.dot(normalDir, incidentDir)
	# 	print("cos_i",cos_i)
	#
	# 	if cos_i < 0:
	# 		normalDir = -normalDir
	# 		cos_i = -np.dot(normalDir, incidentDir)
	# 		n1, n2 = n2, n1
	#
	# 	eta = n1 / n2
	# 	k = 1.0 - eta ** 2 * (1.0 - cos_i ** 2)
	#
	# 	if k < 0:
	# 		newDir = incidentDir + 2.0 * cos_i * normalDir
	# 		newDir = newDir / np.linalg.norm(newDir)
	# 		new_start = intersectionPoint + 1e-5 * normalDir
	# 	else:
	# 		newDir = eta * incidentDir + (eta * cos_i - np.sqrt(k)) * normalDir
	# 		newDir = newDir / np.linalg.norm(newDir)
	# 		new_start = intersectionPoint - 1e-5 * normalDir
	#
	# 	display_point(intersectionPoint, marker='o', color=self.color, parentCanvas=self.parentCanvas)
	# 	self.update_Ray(intersectionPoint)


		# return Ray(Point(new_start), newDir,
		# 		   wavelength=self.get_Wavelength(),
		# 		   color=self.get_Color(),
		# 		   dc=True,
		# 		   parentCanvas=self.parentCanvas)


	# def calculate_ReflectedRay(self, surface):
	#
	# 	result = surface.calculate_RayIntersection(ray=self)  # JAY edit
	#
	# 	print(result)
	#
	# 	if result is None:
	# 		fail_mark = self.lineStart_point + self.direction * 0.5
	# 		display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
	# 		return None
	#
	# 	intersectionPoint, rayColor = result                  #JAy edit 88-92
	# 	#intersectionPoint = result
	#
	# 	# intersectionPoint = surface.calculate_RayIntersection(ray=self)
	# 	#
	# 	# if intersectionPoint is None:
	# 	# 	# Display a intersection warning marker on the ray
	# 	# 	fail_mark = self.lineStart_point + self.direction * 0.5
	# 	# 	display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
	# 	# 	return None
	#
	# 	surfaceNormalDirection = surface.calculate_normalDirection(intersectionPoint)
	# 	# i - (2*(i.n)n) -The second part denotes the component of i in the direction of n
	# 	reflectedRayDir = self.get_Direction() - (
	# 			2 * surfaceNormalDirection * np.dot(self.get_Direction(), surfaceNormalDirection))
	#
	# 	# Transform the point from surface coordinates to opticsLab coordinates
	# 	#intersectionPoint+=surface.center
	# 	print("intersectionPoint, Dir: ", intersectionPoint, reflectedRayDir)
	# 	#intersectionPoint=surface.transform(intersectionPoint)
	# 	display_point(intersectionPoint, marker='o', color=self.color, parentCanvas=self.parentCanvas)
	# 	self.update_Ray(intersectionPoint)  # Extend the ray to meet the surface
	#
	#
	# 	return Ray(Point(intersectionPoint), reflectedRayDir, wavelength=self.get_Wavelength(), color=self.get_Color(),
	# 	           dc=True, parentCanvas=self.parentCanvas)


class Ray_throughPoints(Ray):
	def __init__(self, point1, point2, name=None, dc=False, wavelength=0.55, length=1.0, color="green",
	             parentCanvas=None):
		"""
		Creates a ray which propagates from the rayStart point in the direction given by rayDirection
		:param point1: Point1 of the ray passed as a Point object
		:param point2: Point1 of the ray passed as a Point object
		:param: name: Name of the ray for debugging purposes (optional)
		:param: dc: If the rayDirection is specified as dc or not. Default: False, that is direction is specified as angles in degrees
		:param wavelength: wavelength of the ray in μm.
		:param length: Length of the ray (optional). Default is unit vector
		:param color: Color to be shown when the ray is being visualized (Optional)
		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
		"""
		# assert isinstance(point1, Point), "Ray_throughPoints class: point1 is not a Point object"
		# assert isinstance(point2, Point), "Ray_throughPoints class: point2 is not a Point object"
		direction = dc_from_points(point1, point2)
		super().__init__(startPoint=point1, rayDirection=direction, name=name, dc=True, wavelength=wavelength,
		                 length=length, color=color, parentCanvas=parentCanvas)


class Beam:
	def __init__(self, rayLocations=None, noOfRays=None, wavelength=None, beamDirection=(0, 0, 1), dc=False,
	             length=None, color=None, parentCanvas=None):
		if length is None:
			length = 1
		self.length = length
		self.noOfRays = noOfRays
		self.beamDirection = beamDirection
		self.wavelength = wavelength
		self.rayLocations = rayLocations
		self.color = color
		self.rays = []
		self.dc = dc
		if self.rayLocations is not None:
			for point in self.rayLocations:
				self.rays.append(
					Ray(startPoint=point, rayDirection=self.beamDirection, dc=self.dc, wavelength=self.wavelength,
					    length=self.length, color=self.color, parentCanvas=parentCanvas))
	
	def get_Rays(self):
		return self.rays
	
	def combineWith(self, beam):
		# append beams
		assert isinstance(beam, Beam), "Cannot combine a beam with " + str(type(beam))
		self.rays += beam.get_Rays()
	
	def addRay(self, ray):
		assert isinstance(ray, Ray), "Cannot append anything other than a Ray object"
		self.rays.append(ray)

	def add_Beam(self, beam):
		assert isinstance(beam, Beam), "Cannot append anything other than a Beam object"
		for ray in beam.get_Rays():
			self.rays.append(ray)

	def calculate_ReflectedBeam(self, surface):
		"""
		Calculates and returns the direction of the reflected beam when a beam is incident on this surface
		:param surface: surface on which the ray is incident
		:return: Reflected Ray or Beam
		"""
		rays = self.get_Rays()
		reflectedBeam = Beam()
		for ray in rays:
			reflectedBeam.addRay(ray.calculate_ReflectedRay(surface=surface))
		return reflectedBeam
	
	def calculate_RefractedBeam(self, surface):
		"""
		Calculates and returns the direction of the refracted ray when a beam of light is incident on this surface
		:param surface: Surface on which the beam is incident
		:return: Refracted Beam
		"""
		rays = self.get_Rays()
		refractedBeam = Beam()
		for ray in rays:
			refractedRay = ray.calculate_RefractedRay(surface=surface)
			refractedBeam.addRay(refractedRay)
		return refractedBeam

	def rotate_aboutX(self, angle):
		for ray in self.rays:
			ray.rotate_aboutX(angle)

	def rotate_aboutY(self, angle):
		for ray in self.rays:
			ray.rotate_aboutY(angle)

	def rotate_aboutZ(self, angle):
		for ray in self.rays:
			ray.rotate_aboutZ(angle)


class CircularBeam(Beam):
	def __init__(self, center, radius=0, noOfRays=None, centerRay=True, wavelength=0.55, beamDirection=Z_AXIS_DIRECTION,
	             dc=False, length=None, color=None, parentCanvas=None):
		
		if radius == 0: noOfRays = 1
		
		self.center = center  #.get_coordinates() if isinstance(center, Primitive_point) else np.array(center)
		rayLocations = []
		
		if centerRay: rayLocations.append(self.center)
		noOfRays += 1
		
		beamDirection_DC = beamDirection if dc else deg2DC(beamDirection)
		
		vector = np.array((1, 0, 0))  # Create a vector pointing from center to the point on circumference
		# Find the axis of rotation between Z-axis and the beam direction
		axis = np.cross(deg2DC(Z_AXIS_DIRECTION), beamDirection_DC)
		dot_product = np.dot(deg2DC(Z_AXIS_DIRECTION), beamDirection_DC)
		rotation_angle = np.arccos(dot_product / np.linalg.norm(beamDirection_DC)) if dot_product not in (1, -1) else 0
		# Find the amount of rotation required along the above axis. rotation_angle is in radians
		beam_rotation_matrix = R.from_rotvec(rotation_angle * axis) if rotation_angle != 0 else R.from_rotvec((0, 0, 0))
		
		# print("axis, angle=", axis, np.rad2deg(rotation_angle), deg2DC(Z_AXIS_DIRECTION), deg2DC(beamDirection))
		
		for rotation_angle in np.linspace(0, 2 * np.pi, noOfRays - 1, endpoint=True):
			point_rotation_matrix = R.from_rotvec(
				rotation_angle * deg2DC(Z_AXIS_DIRECTION))  # Find all the points around the center on the circumference
			newPoint_direction = point_rotation_matrix.apply(vector)  # by rotating the vector at 0 angle and finding the direction wrt center
			newPoint = radius * newPoint_direction  # Find the point on the circumference
			newPoint = beam_rotation_matrix.apply(newPoint)  # Rotate the point to align with the direction of the beam
			rayLocations.append(Point(newPoint + self.center.get_coordinates()))  # Translate the points to the given center from origin
			noOfRays += 1
		super().__init__(rayLocations=rayLocations, noOfRays=noOfRays, wavelength=wavelength,
		                 beamDirection=beamDirection, dc=dc, length=length, color=color, parentCanvas=parentCanvas)
