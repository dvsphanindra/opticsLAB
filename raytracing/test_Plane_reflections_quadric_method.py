import numpy as np

from component.miscellaneous_components import display_point

from component.detectors import RectangularScreen

from component.sources import Ray, Ray_throughPoints, CircularBeam

from component import X_AXIS_DIRECTION, Y_AXIS_DIRECTION, Z_AXIS_DIRECTION, ORIGIN, deg2DC, calculate_DirectionAngles, \
	Z_AXIS_NEG_DIRECTION, Y_AXIS_NEG_DIRECTION, dc_from_points

from component.opticalPrimitives.rectangularSurface import RectangularSurface

from component import OpticsLabCanvas, Point

from vispy.color import Color

from matplotlib import pyplot as plt

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})

canvas = OpticsLabCanvas()
x1 = Point(0, 0, 0)
plane1 = RectangularSurface(x1, name='P1', mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3),
                            parentCanvas=canvas)
# plane1.rotate_aboutX(-60)
# plane1.rotate_aboutY(90)
plane1.showNormal()

# x2=Point(1.7,0,0)
# plane2=RectangularSurface(x2, name='P2', mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
# plane2.rotate_aboutX(20)
# plane2.rotate_aboutY(270)
# plane2.showNormal()

# x3=Point(0.5,0.5,0.5)
# plane3 = RectangularSurface(x3, name='P3', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
# plane3.rotate_aboutY(45)
# plane3.showNormal()


screen = RectangularScreen(Point(0.0, 0.0, 2.5), color=Color('green', alpha=0.9))

ray1Start = Point(0, 0.2, -0.5, parentCanvas=canvas)
# point_z = Point(-0.2, 0.2, 0.3, parentCanvas=canvas)
# point_x = Point(0.2, 0.2, 0.1, parentCanvas=canvas)

# ray1Direction = np.array((90, 90, 0))
ray1Start.show(color='g')
# point_z.show(color='g')
# point_x.show(color='cyan')
# ray2Start = Point(-0.4, -0.1, -0.2, parentCanvas=canvas)
# ray2Start.show(color='y')
# #ray2Direction = np.array((90, 90, 0))
# ray2Direction = Z_AXIS_DIRECTION

incidentRay1 = Ray(ray1Start, rayDirection=Z_AXIS_DIRECTION, name='R1', length=1.2, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)
# incidentRay2 = Ray(ray2Start, ray2Direction, name='R2', wavelength=0.85, color='yellow', parentCanvas=canvas)
# incidentRay3 = Ray_throughPoints(ray1Start, point_x, name='R3', color='cyan', parentCanvas=canvas)

# Reflection
r1 = incidentRay1.calculate_ReflectedRay(plane1)  # .calculate_ReflectedRay(plane3).calculate_ReflectedRay(plane2)
# r2 = incidentRay2.calculate_ReflectedRay(plane1)#.calculate_ReflectedRay(plane2)#.calculate_ReflectedRay(plane2)
# r3 = incidentRay3.calculate_ReflectedRay(plane2)#.calculate_ReflectedRay(plane3).calculate_ReflectedRay(plane1)

# a,b=90, 90
# c=calculate_DirectionAngles(a,b)
# print(a,b,c)
# beam2 = CircularBeam(center=Point(0,-0.1,0,parentCanvas=canvas), beamDirection=(a,b,c), radius=0.3, noOfRays=64, wavelength=0.85, color='green', dc=False, parentCanvas=canvas)
# beam2.calculate_ReflectedBeam(plane1).calculate_ReflectedBeam(plane2).calculate_ReflectedBeam(plane3)

n = plane1.get_chiefNormalDirection()
A = 0;
B = 0;
C = 0;
D = n[0] / 2
E = 0;
F = 0;
G = n[1] / 2;
H = 0
I = n[2] / 2;
J = -np.dot(n, x1.get_coordinates())
print("n=", n, "x1=", x1.get_coordinates())
print("J=", J)
plane1.create_quadric(A, B, C, D, E, F, G, H, I, J)
print("Q = ", plane1.Q)

t = plane1.calculate_quadric_intersection(incidentRay1)
p = incidentRay1.get_StartPoint() + (t * incidentRay1.get_Direction())
print("Intersection point, distance, shape= ", p, t, np.shape(t))
P = Point(p[0], p[1], p[2], parentCanvas=canvas)
P.show(marker='+', color='r')
n1 = plane1.calculate_quadric_normal(p)
print("normals current, actual = ", n1, n)
r1 = Ray(Point(p), n1, name='test', dc=True, color='red', parentCanvas=canvas)
r2 = Ray(Point(p), n, name='actual', dc=True, color='white', parentCanvas=canvas)

# t = plane1.calculate_quadric_intersection(incidentRay2)
# p=incidentRay2.get_StartPoint()+(t*incidentRay2.get_Direction())
# print("Intersection point, distance, shape= ",p, t, np.shape(t))
# P=Point(p[0],p[1],p[2], parentCanvas=canvas)
# P.show(marker='+',color='r')
# n1=plane1.calculate_quadric_normal(p)
# print("normals current, actual = ",n1,plane1.get_chiefNormalDirection())
# r1=Ray(p,n1,name='test',dc=True,color='red',parentCanvas=canvas)
# r2=Ray(p,n,name='actual', dc=True, color='white', parentCanvas=canvas)

# n = plane2.get_chiefNormalDirection()
# A = 0; B = 0; C = 0; D = n[0]/2
# E = 0; F = 0; G = n[1]/2; H = 0
# I = n[2]/2; J = -np.dot(n,x2.get_coordinates())
# print("n=",n,"x2=",x2.get_coordinates())
# print("J=",J)
# plane2.create_quadric(A,B,C,D,E,F,G,H,I,J)
# print("Q = ", plane2.Q)

# t = plane2.calculate_quadric_intersection(incidentRay3)
# p=incidentRay3.get_StartPoint()+(t*incidentRay3.get_Direction())
# print("Intersection point, distance, shape= ",p, t, np.shape(t))
# P=Point(p[0],p[1],p[2], parentCanvas=canvas)
# P.show(marker='+',color='r')
# n1=plane2.calculate_quadric_normal(p)
# print("normals current, actual = ",n1,plane2.get_chiefNormalDirection())
# r1=Ray(p,n1,name='test',dc=True,color='red',parentCanvas=canvas)
# r2=Ray(p,n,name='actual', dc=True, color='white', parentCanvas=canvas)

canvas.show()  # Display the opticsLab canvas
