# import numpy as np
# from vispy import scene
# from vispy.scene.visuals import SurfacePlot
# from scipy.spatial.transform import Rotation
# from ..miscellaneous_components import Z_AXIS_DIRECTION, display_point
# from ..materialProperties import refractiveIndex
# from ..sources import Ray
#
# from .lineVector import LineVector
# from .constants import Z_AXIS_DIRECTION
# from .primitive_point import Primitive_point
# from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
#
#
# class Surface:
# 	def __init__(self, center, x_grid, y_grid, z_grid, name=None, xTilt=0.0, yTilt=0.0, color="black", parentCanvas=None):
# 		"""
# 		Creates a surface with the given center and normal with the specified media
# 		:param center: Center of the plane with respect to the opticsLab coordinates. Can be a Point object or numpy array.
# 		:param xTilt: tilt of the plane with respect to opticsLab X axis
# 		:param yTilt: tilt of the plane with respect to opticsLab Y axis
# 		:param: name: Name of the surface for debugging purposes (optional)
# 		:param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "Green"
# 		:param parentCanvas: Canvas on which the object is to be rendered. Default is None
# 		"""
# 		self.center = np.array((0, 0, 0))
# 		self.name = name
# 		final_center = center.get_coordinates() if isinstance(center, Point) else np.array(center)
# 		normalDirection = Z_AXIS_DIRECTION  # Create a surface with normal parallel to z-axis direction (xy plane)
# 		self.xTilt = xTilt
# 		self.yTilt = yTilt
# 		self.color = color
# 		self.parentCanvas = parentCanvas
#
# 		self.Q = None
#
# 		self.__translationMatrix = np.zeros(3)
# 		self.__rotationMatrix = Rotation.from_rotvec(np.zeros(3)) # Create a rotation matrix with zero degrees rotation
# 		#print("translationMatrix: ",self.__translationMatrix)
# 		#print("rot=\n", self.__rotationMatrix.as_matrix())
#
# 		self.normal = LineVector(start=self.center, direction=normalDirection, color='w')
#
# 		parent = None if self.parentCanvas is None else self.parentCanvas.view.scene
# 		self.visual = SurfacePlot(x=x_grid, y=y_grid, z=z_grid, color=color, parent=parent)
# 		self.visual.transform = scene.transforms.MatrixTransform()
# 		self.rotate_aboutX(self.xTilt)
# 		self.rotate_aboutY(self.yTilt)
# 		#print("Here:")
# 		self.translate(final_center)
#
# 	def get_Visual(self):
# 		return self.visual
#
# 	def get_normalVisual(self):
# 		return self.normal.get_visual()
#
# 	def showNormal(self):
# 		self.parentCanvas.view.add(self.normal.get_visual())
#
# 	def function(self, x, y):
# 		"""To be implemented by the child surface"""
# 		pass
#
# 	def calculate_normalDirection(self, point):
# 		""" To be implemented by the child surface"""
# 		pass
#
# 	def calculate_RayIntersection(self, ray):
# 		""" To be implemented by the child surface"""
# 		pass
#
# 	def calculate_BeamIntersection(self, beam):
# 		""" To be implemented by the child surface"""
# 		pass
#
# 	def get_chiefNormalDirection(self):
# 		return self.normal.get_Direction_Cosines()
#
# 	# def __rotate(self, angle, axis):
# 	# 	if not all(self.center == 0):
# 	# 		self.visual.transform.translate(-self.center) # Bring to origin
# 	# 	self.visual.transform.rotate(angle, axis)
# 	# 	self.visual.transform.translate(self.center)
# 	# 	self.normal.rotate(axis, angle)
# 	#
# 	# 	self.__rotationMatrix *= Rotation.from_rotvec(np.deg2rad(angle)*np.array(axis)) # Multiply quaternions
# 	# 	print(self.name, " rot matrix: ", np.rad2deg(self.__rotationMatrix.as_rotvec()))
#
# 	def translate(self, point):
# 		point_arr = np.array(point.get_coordinates()) if hasattr(point, 'get_coordinates') else np.array(point)
# 		if not all(self.center == 0):
# 			self.visual.transform.translate(-self.center)
#
# 		self.visual.transform.translate(point_arr)
# 		self.center = point_arr
# 		self.normal.translate(self.center)
#
# 		# CRITICAL FIX: Replace the matrix, do NOT use +=
# 		self.__translationMatrix = self.center.copy()
#
# 	def __rotate(self, angle, axis, pivot=None):
# 		# If no pivot is provided, spin around its own center
# 		if pivot is None:
# 			pivot = self.center
# 		pivot = np.array(pivot)
#
# 		# 1. Vispy Visual Orbit
# 		self.visual.transform.translate(-pivot)  # Bring pivot to origin
# 		self.visual.transform.rotate(angle, axis)
# 		self.visual.transform.translate(pivot)  # Move back to pivot
#
# 		self.normal.rotate(axis, angle)
#
# 		# 2. Mathematical Orbit (CRITICAL for Ray Tracing)
# 		rot = Rotation.from_rotvec(np.deg2rad(angle) * np.array(axis))
#
# 		# Calculate new center by rotating the offset from the pivot
# 		offset = self.center - pivot
# 		self.center = pivot + rot.apply(offset)
#
# 		# Update tracking matrices for calculate_RayIntersection
# 		self.__translationMatrix = self.center.copy()
# 		self.__rotationMatrix = rot * self.__rotationMatrix
# 		#print(self.name, " rot matrix: ", np.rad2deg(self.__rotationMatrix.as_rotvec()))
#
#
# 	# def rotate_aboutX(self, angle):
# 	# 	self.__rotate(angle, (1, 0, 0))
# 	#
# 	# def rotate_aboutY(self, angle):
# 	# 	self.__rotate(angle, (0, 1, 0))
# 	#
# 	# def rotate_aboutZ(self, angle):
# 	# 	self.__rotate(angle, (0, 0, 1))
#
# 	def rotate_aboutX(self, angle, pivot=None):
# 		self.__rotate(angle, (1, 0, 0), pivot)
#
# 	def rotate_aboutY(self, angle, pivot=None):
# 		self.__rotate(angle, (0, 1, 0), pivot)
#
# 	def rotate_aboutZ(self, angle, pivot=None):
# 		self.__rotate(angle, (0, 0, 1), pivot)
#
# 	# def translate(self, point):
# 	# 	#p = point.get_coordinates() if isinstance(point, Point) else np.array(point)
# 	# 	# Shift the surface back to origin of the opticsLab as the point is defined wrt this origin
# 	# 	if not all(self.center == 0):
# 	# 		self.visual.transform.translate(-self.center)
# 	# 	self.visual.transform.translate(point)
# 	# 	self.center = point      #JAY edit
# 	# 	self.normal.translate(self.center)
# 	# 	self.__translationMatrix += self.center.copy()  # Update the translation matrix for transformation of coordinates
# 	#
# 	# def transform(self, point):
# 	# 	# TODO First rotate, then translate
# 	# 	print("Point: ",point)#, self.translationMatrix)
# 	# 	transformedPoint = np.array(self.__rotationMatrix.apply(point))# + self.__translationMatrix) #Just uncommented the + part
# 	# 	transformedPoint = np.array(point+self.__translationMatrix)
# 	# 	print("translated Point: ",transformedPoint)
# 	# 	return transformedPoint
#
# 	def transform(self, point): #jay edit
# 		#print("Point:", point)
# 		rotatedPoint = np.array(self.__rotationMatrix.apply(point))
# 		transformedPoint = rotatedPoint + self.__translationMatrix
# 		#print("transformed Point:", transformedPoint)
# 		return transformedPoint
#
# 	# def inverse_transform(self, point):
# 	# 	#rotation = self.__rotationMatrix.inv()
# 	# 	transformedPoint = np.array(self.__rotationMatrix.apply(point, inverse=True))# - self.__translationMatrix)
# 	# 	return transformedPoint
#
# 	def inverse_transform(self, point): # jay edit
# 		shiftedPoint = np.array(point - self.__translationMatrix)
# 		transformedPoint = np.array(self.__rotationMatrix.apply(shiftedPoint, inverse=True))
# 		return transformedPoint
#
#
# 	def create_quadric(self, A,B,C,D,E,F,G,H,I,J):
# 		self.Q = np.matrix([[A,B,C,D],[B,E,F,G],[C,F,H,I],[D,G,I,J]])
#
# 	def calculate_quadric_intersection(self, ray):
# 		p = np.array([np.append(ray.get_StartPoint(),[1])]).T # To convert to quadric equation compatible form
# 		d = np.array([np.append(ray.get_Direction(),[1])]).T # To convert to quadric equation compatible form
#
# 		# squeeze is used to remove the axes of length 1. Since the output is a scalar, but the numpy product results in a 2D array
# 		dTQ = d.T * self.Q
# 		A = np.squeeze(np.array((dTQ * d)))
# 		B = 2 * np.squeeze(np.array(dTQ * p))
# 		C = np.squeeze(np.array(p.T * self.Q * p))
# 		#
# 		# A = np.dot(np.dot(d.T,self.Q),d) ** 2
# 		# B = 2 * np.dot(np.dot(d.T, self.Q), p)
# 		# C = np.dot(np.dot(p.T, self.Q), p)
#
# 		if A == 0:
# 			print("A=0, returning -C/B")
# 			return -C/B
# 		# else:
# 		discriminant = B ** 2 - (4*A*C)
#
# 		print("d,p,dTQ, A,B,C, discriminant, {d, dTQ shape} = ", d,p, dTQ, A, B, C, discriminant, "{",np.shape(d), np.shape(dTQ), "}")
# 		if discriminant < 0:
# 			print("No intersection")
# 			return None
# 		elif discriminant == 0:
# 			print("Ray is tangent to the quadric surface ", self.name)
# 			return  -B/(2*A)
# 		else: # if discriminant > 0
# 			x1 = (-B + np.sqrt(discriminant))/(2*A)
# 			x2 = (-B - np.sqrt(discriminant))/(2*A)
# 			print("x1,x2 = ",x1,x2)
# 			if x1 >= 0:
# 				print("Selecting first root")
# 				return x1
# 			elif x2 >= 0:
# 				print("Selecting second root")
# 				return x2
# 			else:
# 				print("Unknown case")
# 				return x1
#
# 	def calculate_quadric_normal(self, point):
# 		n = np.squeeze(np.array(self.Q[:-1,:] * np.array([np.append(point,[1])]).T))
# 		return n/np.linalg.norm(n)
#
# 	def rotate_vector(self, vector):
# 		return np.array(self._Surface__rotationMatrix.apply(vector), dtype=float)
#
# 	def calculate_RefractedRay(self, ray):
# 		"""
#         Calculates the refraction of an incoming ray through this surface.
#         Handles total internal reflection automatically.
#         """
# 		# 1. Self handles the intersection
# 		result = self.calculate_RayIntersection(ray)
#
# 		#print(result)
#
# 		if result is None:
# 			fail_mark = ray.get_StartPoint() + ray.get_Direction() * 0.5
# 			display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
# 			return None
#
# 		intersectionPoint, rayColor = result
#
# 		# 2. Extract direction and normal
# 		incidentDir = np.array(ray.get_Direction(), dtype=float)
# 		incidentDir = incidentDir / np.linalg.norm(incidentDir)
#
# 		normalDir = np.array(self.calculate_normalDirection(intersectionPoint), dtype=float)
# 		normalDir = normalDir / np.linalg.norm(normalDir)
#
# 		# 3. Get refractive indices
# 		# Import your refractiveIndex function here if needed
# 		# from opticsLAB.raytracing.component.materials import refractiveIndex
# 		n1 = refractiveIndex(ray.get_Wavelength(), self.mediumBefore)
# 		n2 = refractiveIndex(ray.get_Wavelength(), self.mediumAfter)
#
# 		# 4. Snell's Law Vector Math
# 		cos_i = -np.dot(normalDir, incidentDir)
#
# 		# If the ray hit the surface from the "inside" or back, the normal
# 		# is facing the wrong way. We must flip it and swap n1/n2.
# 		if cos_i < 0:
# 			normalDir = -normalDir
# 			cos_i = -np.dot(normalDir, incidentDir)
# 			n1, n2 = n2, n1
#
# 		eta = n1 / n2
# 		k = 1.0 - (eta ** 2) * (1.0 - cos_i ** 2)
#
# 		# 5. Visual updates
# 		display_point(intersectionPoint, marker='o', color=ray.get_Color(), parentCanvas=self.parentCanvas)
# 		ray.update_Ray(intersectionPoint)
#
# 		# Import Ray locally
# 		from opticsLAB.raytracing.component.sources import Ray
# 		from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
#
# 		eps = 1e-5
#
# 		# 6. Branch: Total Internal Reflection vs Refraction
# 		if k < 0:
# 			print(f"Total Internal Reflection at {self.name}!")
# 			# Reflection formula: r = i + 2*cos_i*n
# 			reflectedRayDir = incidentDir + (2.0 * cos_i * normalDir)
# 			reflectedRayDir = reflectedRayDir / np.linalg.norm(reflectedRayDir)
#
# 			# Offset slightly ALONG the normal (stays on incident side)
# 			new_start = intersectionPoint + eps * normalDir
#
# 			return Ray(Point(new_start),
# 					   rayDirection=reflectedRayDir,
# 					   wavelength=ray.get_Wavelength(),
# 					   color=ray.get_Color(),
# 					   dc=True,
# 					   parentCanvas=self.parentCanvas)
#
# 		else:
# 			# Standard Refraction
# 			refractedRayDir = (eta * incidentDir) + ((eta * cos_i - np.sqrt(k)) * normalDir)
# 			refractedRayDir = refractedRayDir / np.linalg.norm(refractedRayDir)
#
# 			# Offset slightly AGAINST the normal (enters transmitted side)
# 			new_start = intersectionPoint - eps * normalDir
#
# 			return Ray(Point(new_start),
# 					   rayDirection=refractedRayDir,
# 					   wavelength=ray.get_Wavelength(),
# 					   color=ray.get_Color(),
# 					   dc=True,
# 					   parentCanvas=self.parentCanvas)
#
# 	def calculate_ReflectedRay(self, ray):
# 		"""
#         Calculates the reflection of an incoming ray off this surface.
#         """
# 		result = self.calculate_RayIntersection(ray)
#
# 		if result is None:
# 			fail_mark = ray.get_StartPoint() + ray.get_Direction() * 0.5
# 			display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=self.parentCanvas)
# 			return None
#
# 		intersectionPoint, rayColor = result
#
# 		incidentDir = np.array(ray.get_Direction(), dtype=float)
# 		incidentDir /= np.linalg.norm(incidentDir)
#
# 		normalDir = np.array(self.calculate_normalDirection(intersectionPoint), dtype=float)
# 		normalDir /= np.linalg.norm(normalDir)
#
# 		# CRITICAL FIX: make the normal face the incoming ray
# 		if np.dot(incidentDir, normalDir) > 0:
# 			normalDir = -normalDir
#
# 		reflectedRayDir = incidentDir - 2.0 * np.dot(incidentDir, normalDir) * normalDir
# 		reflectedRayDir /= np.linalg.norm(reflectedRayDir)
#
# 		display_point(intersectionPoint, marker='o', color=ray.get_Color(), parentCanvas=self.parentCanvas)
# 		ray.update_Ray(intersectionPoint)
#
# 		# Push the new ray slightly away from the surface along the reflected direction
# 		new_start = np.array(intersectionPoint, dtype=float) + 1e-5 * reflectedRayDir
#
# 		return Ray(
# 			Point(new_start),
# 			rayDirection=reflectedRayDir,
# 			wavelength=ray.get_Wavelength(),
# 			color=ray.get_Color(),
# 			dc=True,
# 			parentCanvas=self.parentCanvas
# 		)
#
import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot
from scipy.spatial.transform import Rotation
from ..miscellaneous_components import Z_AXIS_DIRECTION, display_point
from ..materialProperties import refractiveIndex
from ..sources import Ray
from .lineVector import LineVector
from .constants import Z_AXIS_DIRECTION
from .primitive_point import Primitive_point
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point

class Surface:
    # ... [Keep __init__, transforms, translations, rotations, and quadric
    # calculations EXACTLY the same] ...
    def __init__(self, center, x_grid, y_grid, z_grid, name=None, xTilt=0.0, yTilt=0.0, color="black",
                 parentCanvas=None):
        """
        Creates a surface with the given center and normal with the specified media
        :param center: Center of the plane with respect to the opticsLab coordinates. Can be a Point object or numpy array.
        :param xTilt: tilt of the plane with respect to opticsLab X axis
        :param yTilt: tilt of the plane with respect to opticsLab Y axis
        :param: name: Name of the surface for debugging purposes (optional)
        :param color: Colour of the surface. Can be among vispy colors or HTML colour (optional). Default: "Green"
        :param parentCanvas: Canvas on which the object is to be rendered. Default is None
        """
        self.center = np.array((0, 0, 0))
        self.name = name
        final_center = center.get_coordinates() if isinstance(center, Point) else np.array(center)
        normalDirection = Z_AXIS_DIRECTION  # Create a surface with normal parallel to z-axis direction (xy plane)
        self.xTilt = xTilt
        self.yTilt = yTilt
        self.color = color
        self.parentCanvas = parentCanvas

        self.Q = None

        self.__translationMatrix = np.zeros(3)
        self.__rotationMatrix = Rotation.from_rotvec(np.zeros(3)) # Create a rotation matrix with zero degrees rotation
        #print("translationMatrix: ",self.__translationMatrix)
        #print("rot=\n", self.__rotationMatrix.as_matrix())

        self.normal = LineVector(start=self.center, direction=normalDirection, color='w')

        parent = None if self.parentCanvas is None else self.parentCanvas.view.scene
        self.visual = SurfacePlot(x=x_grid, y=y_grid, z=z_grid, color=color, parent=parent)
        self.visual.transform = scene.transforms.MatrixTransform()
        self.rotate_aboutX(self.xTilt)
        self.rotate_aboutY(self.yTilt)
        #print("Here:")
        self.translate(final_center)

    def get_Visual(self):
        return self.visual

    def get_normalVisual(self):
        return self.normal.get_visual()

    def showNormal(self):
        self.parentCanvas.view.add(self.normal.get_visual())

    def function(self, x, y):
        """To be implemented by the child surface"""
        pass

    def calculate_normalDirection(self, point):
        """ To be implemented by the child surface"""
        pass

    def calculate_RayIntersection(self, ray):
        """ To be implemented by the child surface"""
        pass

    def calculate_BeamIntersection(self, beam):
        """ To be implemented by the child surface"""
        pass

    def get_chiefNormalDirection(self):
        return self.normal.get_Direction_Cosines()

    # def __rotate(self, angle, axis):
    # 	if not all(self.center == 0):
    # 		self.visual.transform.translate(-self.center) # Bring to origin
    # 	self.visual.transform.rotate(angle, axis)
    # 	self.visual.transform.translate(self.center)
    # 	self.normal.rotate(axis, angle)
    #
    # 	self.__rotationMatrix *= Rotation.from_rotvec(np.deg2rad(angle)*np.array(axis)) # Multiply quaternions
    # 	print(self.name, " rot matrix: ", np.rad2deg(self.__rotationMatrix.as_rotvec()))

    def translate(self, point):
        point_arr = np.array(point.get_coordinates()) if hasattr(point, 'get_coordinates') else np.array(point)
        if not all(self.center == 0):
            self.visual.transform.translate(-self.center)

        self.visual.transform.translate(point_arr)
        self.center = point_arr
        self.normal.translate(self.center)

        # CRITICAL FIX: Replace the matrix, do NOT use +=
        self.__translationMatrix = self.center.copy()

    def __rotate(self, angle, axis, pivot=None):
        # If no pivot is provided, spin around its own center
        if pivot is None:
            pivot = self.center
        pivot = np.array(pivot)

        # 1. Vispy Visual Orbit
        self.visual.transform.translate(-pivot)  # Bring pivot to origin
        self.visual.transform.rotate(angle, axis)
        self.visual.transform.translate(pivot)  # Move back to pivot

        self.normal.rotate(axis, angle)

        # 2. Mathematical Orbit (CRITICAL for Ray Tracing)
        rot = Rotation.from_rotvec(np.deg2rad(angle) * np.array(axis))

        # Calculate new center by rotating the offset from the pivot
        offset = self.center - pivot
        self.center = pivot + rot.apply(offset)

        # Update tracking matrices for calculate_RayIntersection
        self.__translationMatrix = self.center.copy()
        self.__rotationMatrix = rot * self.__rotationMatrix
        #print(self.name, " rot matrix: ", np.rad2deg(self.__rotationMatrix.as_rotvec()))


    # def rotate_aboutX(self, angle):
    # 	self.__rotate(angle, (1, 0, 0))
    #
    # def rotate_aboutY(self, angle):
    # 	self.__rotate(angle, (0, 1, 0))
    #
    # def rotate_aboutZ(self, angle):
    # 	self.__rotate(angle, (0, 0, 1))

    def rotate_aboutX(self, angle, pivot=None):
        self.__rotate(angle, (1, 0, 0), pivot)

    def rotate_aboutY(self, angle, pivot=None):
        self.__rotate(angle, (0, 1, 0), pivot)

    def rotate_aboutZ(self, angle, pivot=None):
        self.__rotate(angle, (0, 0, 1), pivot)

    # def translate(self, point):
    # 	#p = point.get_coordinates() if isinstance(point, Point) else np.array(point)
    # 	# Shift the surface back to origin of the opticsLab as the point is defined wrt this origin
    # 	if not all(self.center == 0):
    # 		self.visual.transform.translate(-self.center)
    # 	self.visual.transform.translate(point)
    # 	self.center = point      #JAY edit
    # 	self.normal.translate(self.center)
    # 	self.__translationMatrix += self.center.copy()  # Update the translation matrix for transformation of coordinates
    #
    # def transform(self, point):
    # 	# TODO First rotate, then translate
    # 	print("Point: ",point)#, self.translationMatrix)
    # 	transformedPoint = np.array(self.__rotationMatrix.apply(point))# + self.__translationMatrix) #Just uncommented the + part
    # 	transformedPoint = np.array(point+self.__translationMatrix)
    # 	print("translated Point: ",transformedPoint)
    # 	return transformedPoint

    def transform(self, point): #jay edit
        #print("Point:", point)
        rotatedPoint = np.array(self.__rotationMatrix.apply(point))
        transformedPoint = rotatedPoint + self.__translationMatrix
        #print("transformed Point:", transformedPoint)
        return transformedPoint

    # def inverse_transform(self, point):
    # 	#rotation = self.__rotationMatrix.inv()
    # 	transformedPoint = np.array(self.__rotationMatrix.apply(point, inverse=True))# - self.__translationMatrix)
    # 	return transformedPoint

    def inverse_transform(self, point): # jay edit
        shiftedPoint = np.array(point - self.__translationMatrix)
        transformedPoint = np.array(self.__rotationMatrix.apply(shiftedPoint, inverse=True))
        return transformedPoint


    def create_quadric(self, A,B,C,D,E,F,G,H,I,J):
        self.Q = np.matrix([[A,B,C,D],[B,E,F,G],[C,F,H,I],[D,G,I,J]])

    def calculate_quadric_intersection(self, ray):
        p = np.array([np.append(ray.get_StartPoint(),[1])]).T # To convert to quadric equation compatible form
        d = np.array([np.append(ray.get_Direction(),[1])]).T # To convert to quadric equation compatible form

        # squeeze is used to remove the axes of length 1. Since the output is a scalar, but the numpy product results in a 2D array
        dTQ = d.T * self.Q
        A = np.squeeze(np.array((dTQ * d)))
        B = 2 * np.squeeze(np.array(dTQ * p))
        C = np.squeeze(np.array(p.T * self.Q * p))
        #
        # A = np.dot(np.dot(d.T,self.Q),d) ** 2
        # B = 2 * np.dot(np.dot(d.T, self.Q), p)
        # C = np.dot(np.dot(p.T, self.Q), p)

        if A == 0:
            print("A=0, returning -C/B")
            return -C/B
        # else:
        discriminant = B ** 2 - (4*A*C)

        print("d,p,dTQ, A,B,C, discriminant, {d, dTQ shape} = ", d,p, dTQ, A, B, C, discriminant, "{",np.shape(d), np.shape(dTQ), "}")
        if discriminant < 0:
            print("No intersection")
            return None
        elif discriminant == 0:
            print("Ray is tangent to the quadric surface ", self.name)
            return  -B/(2*A)
        else: # if discriminant > 0
            x1 = (-B + np.sqrt(discriminant))/(2*A)
            x2 = (-B - np.sqrt(discriminant))/(2*A)
            print("x1,x2 = ",x1,x2)
            if x1 >= 0:
                print("Selecting first root")
                return x1
            elif x2 >= 0:
                print("Selecting second root")
                return x2
            else:
                print("Unknown case")
                return x1

    def calculate_quadric_normal(self, point):
        n = np.squeeze(np.array(self.Q[:-1,:] * np.array([np.append(point,[1])]).T))
        return n/np.linalg.norm(n)

    def rotate_vector(self, vector):
        return np.array(self._Surface__rotationMatrix.apply(vector), dtype=float)

    def calculate_RefractedRay(self, ray):
       result = self.calculate_RayIntersection(ray)

       if result is None:
          if ray.parentCanvas is not None:
              fail_mark = ray.get_StartPoint() + ray.get_Direction() * 0.5
              display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=ray.parentCanvas)
          return None

       intersectionPoint, rayColor = result

       incidentDir = np.array(ray.get_Direction(), dtype=float)
       incidentDir = incidentDir / np.linalg.norm(incidentDir)

       normalDir = np.array(self.calculate_normalDirection(intersectionPoint), dtype=float)
       normalDir = normalDir / np.linalg.norm(normalDir)

       n1 = refractiveIndex(ray.get_Wavelength(), self.mediumBefore)
       n2 = refractiveIndex(ray.get_Wavelength(), self.mediumAfter)

       cos_i = -np.dot(normalDir, incidentDir)

       if cos_i < 0:
          normalDir = -normalDir
          cos_i = -np.dot(normalDir, incidentDir)
          n1, n2 = n2, n1

       eta = n1 / n2
       k = 1.0 - (eta ** 2) * (1.0 - cos_i ** 2)

       # OPTIMIZATION: Only update UI elements if canvas is active
       if ray.parentCanvas is not None:
           display_point(intersectionPoint, marker='o', color=ray.get_Color(), parentCanvas=ray.parentCanvas)
           ray.update_Ray(intersectionPoint)

       eps = 1e-5

       if k < 0:
          reflectedRayDir = incidentDir + (2.0 * cos_i * normalDir)
          reflectedRayDir = reflectedRayDir / np.linalg.norm(reflectedRayDir)
          new_start = intersectionPoint + eps * normalDir

          # OPTIMIZATION: Use ray.parentCanvas
          return Ray(Point(new_start),
                   rayDirection=reflectedRayDir,
                   wavelength=ray.get_Wavelength(),
                   color=ray.get_Color(),
                   dc=True,
                   parentCanvas=ray.parentCanvas)

       else:
          refractedRayDir = (eta * incidentDir) + ((eta * cos_i - np.sqrt(k)) * normalDir)
          refractedRayDir = refractedRayDir / np.linalg.norm(refractedRayDir)
          new_start = intersectionPoint - eps * normalDir

          # OPTIMIZATION: Use ray.parentCanvas
          return Ray(Point(new_start),
                   rayDirection=refractedRayDir,
                   wavelength=ray.get_Wavelength(),
                   color=ray.get_Color(),
                   dc=True,
                   parentCanvas=ray.parentCanvas)

    def calculate_ReflectedRay(self, ray):
       result = self.calculate_RayIntersection(ray)

       if result is None:
          if ray.parentCanvas is not None:
              fail_mark = ray.get_StartPoint() + ray.get_Direction() * 0.5
              display_point(fail_mark, marker='!', color='r', size=50, parentCanvas=ray.parentCanvas)
          return None

       intersectionPoint, rayColor = result

       incidentDir = np.array(ray.get_Direction(), dtype=float)
       incidentDir /= np.linalg.norm(incidentDir)

       normalDir = np.array(self.calculate_normalDirection(intersectionPoint), dtype=float)
       normalDir /= np.linalg.norm(normalDir)

       if np.dot(incidentDir, normalDir) > 0:
          normalDir = -normalDir

       reflectedRayDir = incidentDir - 2.0 * np.dot(incidentDir, normalDir) * normalDir
       reflectedRayDir /= np.linalg.norm(reflectedRayDir)

       # OPTIMIZATION
       if ray.parentCanvas is not None:
           display_point(intersectionPoint, marker='o', color=ray.get_Color(), parentCanvas=ray.parentCanvas)
           ray.update_Ray(intersectionPoint)

       new_start = np.array(intersectionPoint, dtype=float) + 1e-5 * reflectedRayDir

       # OPTIMIZATION: Use ray.parentCanvas
       return Ray(
          Point(new_start),
          rayDirection=reflectedRayDir,
          wavelength=ray.get_Wavelength(),
          color=ray.get_Color(),
          dc=True,
          parentCanvas=ray.parentCanvas
       )