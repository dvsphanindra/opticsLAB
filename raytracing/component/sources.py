import numpy as np
from .primitives.lineVector import LineVector
from .materialProperties import refractiveIndex

class Ray(LineVector):
	def __init__(self, startPoint, rayDirection=None, wavelength=0.55, length=1.0, color="green", degrees=True):
		"""
		Creates a ray which propagates from the rayStart point in the direction given by rayDirection
		:param startPoint: Starting point of the ray
		:param rayDirection: direction cosines of the ray or tilts in degrees with respect to pyOptiCAD coordinates
		:param wavelength: wavelength of the ray in μm.
		:param length: Length of the ray (optional). Default is unit vector
		:param color: Color to be shown when the ray is being visualized (Optional)
		"""
		# TODO select color based on wavelength
		self.wavelength = wavelength
		# if degrees:
		# 	rayDirection=np.cos(rayDirection)
		super().__init__(startPoint, rayDirection, length, color)
		
	def rotate_aboutX(self, angle):
		pass
	def rotate_aboutY(self, angle):
		pass
	def rotate_aboutZ(self, angle):
		pass
	
	def get_StartPoint(self):
		return self.lineStart
	
	def get_Direction(self):
		return self.get_Direction_Cosines()
	
	def get_Wavelength(self):
		return self.wavelength
	
	def get_Color(self):
		return self.color
	
	def update_Ray(self, point):
		self.update_Vector(point)
	
	def calculate_RefractedRay(self, surface):
		intersectionPoint = surface.calculate_RayIntersection(ray=self)
		
		surfaceNormalDirection=surface.calculate_normalDirection(intersectionPoint)
		
		n1 = refractiveIndex(self.get_Wavelength(), surface.mediumBefore)
		n2 = refractiveIndex(self.get_Wavelength(), surface.mediumAfter)
		
		r = n2 / n1# n1 / n2 # TODO: to verify this formula why it is reverse
		print("dir: ", self.get_Direction(), "surfDir: ", surfaceNormalDirection)
		dotProduct = -np.dot(surfaceNormalDirection, self.get_Direction())
		horizontalComp = 1 - (r * r * (1 - dotProduct ** 2))
		assert horizontalComp >= 0, "Error in refraction (negative value under root):" + "normalDir={0}, dot product={1}, r={2}, [1-dot]={3}, horizontalComp**2={4}".format(
			str(surfaceNormalDirection), dotProduct, r, 1 - dotProduct ** 2, horizontalComp)
		
		# refractedRayDir = (r * np.cross(self.normal, a)) - (self.normal * np.sqrt(1 - (r * r * np.dot(b, b))))
		refractedRayDir = np.sqrt(horizontalComp) * surfaceNormalDirection + r * (self.get_Direction() - dotProduct * surfaceNormalDirection)
		
		intersectionPoint=surface.transform(intersectionPoint)
		# refractedRayDir=surface.transform(refractedRayDir)
		self.update_Ray(intersectionPoint) # Extend the ray to meet the surface
		return Ray(intersectionPoint, refractedRayDir, wavelength=self.get_Wavelength(), color=self.get_Color())
	
	def calculate_ReflectedRay(self, surface):
		intersectionPoint = surface.calculate_RayIntersection(ray=self)
		surfaceNormalDirection = surface.calculate_normalDirection(intersectionPoint)
		# i - (2*(i.n)n) -The second part denotes the component of i in the direction of n
		reflectedRayDir = self.get_Direction() - (2 * surfaceNormalDirection * np.dot(self.get_Direction(), surfaceNormalDirection))
		
		#Transform the point from surface coordinates to pyOptiCAD coordinates
		# intersectionPoint+=surface.center
		# print("intersectionPoint: ", intersectionPoint)
		intersectionPoint=surface.transform(intersectionPoint)
		self.update_Ray(intersectionPoint)  # Extend the ray to meet the surface
		
		return Ray(intersectionPoint, reflectedRayDir, wavelength=self.get_Wavelength(), color=self.get_Color())

class Beam:
	def __init__(self, rayLocations=None, noOfRays=None, wavelength=None, beamDirection=(0,0,1), length=None, color=None):
		if length is None:
			length=1
		self.length = length
		self.noOfRays = noOfRays
		self.beamDirection = beamDirection
		self.wavelength = wavelength
		self.rayLocations=rayLocations
		self.color=color
		self.rays=[]
		if self.rayLocations is not None:
			for point in self.rayLocations:
				self.rays.append(Ray(point, self.beamDirection, self.wavelength,self.length, self.color, degrees=False))
			
	def get_Rays(self):
		return self.rays
	
	def combineWith(self, beam):
		# append beams
		assert isinstance(beam, Beam), "Cannot combine a beam with " + str(type(beam))
		self.rays += beam.get_Rays()
		
	def addRay(self, ray):
		assert isinstance(ray, Ray), "Cannot append anything other than a Ray object"
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
		
class CircularBeam(Beam):
	def __init__(self, center, radius=0, noOfRays=None, centerRay=True, wavelength=0.55, beamDirection=(0,0,1), length=None, color=None):
		#TODO: To verify for arbitrary starting point (center) located away from the cardinal planes
		if radius==0:
			noOfRays=1
		self.center = np.array(center)
		rayLocations= []
		if centerRay: rayLocations.append(self.center)
		noOfRays+=1
		l,m,n=beamDirection
		xc,yc,zc=center
		# Find a point # TODO verify this for points away from the cardinal planes
		if n!=0:
			x, y = xc + radius, yc
			z = zc - (l * x + m * y) / n
		elif m!=0:
			x, z = xc + radius, zc
			y = yc - (l * x + n * z) / m
		else:
			y, z = yc + radius, zc
			x = xc - (m * y + n * z) / l
		point=np.array((x,y,z))
		vector = point - center
		for angle in np.linspace(0,2*np.pi, noOfRays-1, endpoint=False):
			newPoint_direction=self.rotate(vector, axis=beamDirection, angle=angle)
			newPoint = self.center + radius * newPoint_direction
			rayLocations.append(newPoint)
			noOfRays+=1
			
		super().__init__(rayLocations, noOfRays, wavelength, beamDirection, length, color)
	
	@staticmethod
	def rotate(vector, axis, angle):
		"""
		Rotate the vector by an angle about an axis using Rodrigues formula
		:param axis: Axis about which the vector will be rotated
		:param angle: angle in degrees about which the vector will be rotated
		:return:
		"""
		# vector = np.array(vector)
		axis = np.array(axis)
		# theta = np.deg2rad(angle)
		direction = vector * np.cos(angle) + (np.cross(axis, vector) * np.sin(angle)) + (
				np.dot(axis, vector) * axis * (1 - np.cos(angle)))  # Rodrigues formula
		return direction


