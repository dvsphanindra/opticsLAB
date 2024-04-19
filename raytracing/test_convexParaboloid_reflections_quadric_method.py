import numpy as np

from component.miscellaneous_components import display_point

from component.detectors import RectangularScreen
from component.opticalPrimitives.convexParaboloid import Convex_Paraboloid

from component.sources import Ray, Ray_throughPoints, CircularBeam

from component import X_AXIS_DIRECTION, Y_AXIS_DIRECTION, Z_AXIS_DIRECTION, ORIGIN, deg2DC, calculate_DirectionAngles, \
	Z_AXIS_NEG_DIRECTION, Y_AXIS_NEG_DIRECTION, dc_from_points

from component import PyOptiCADCanvas, Point

from vispy.color import Color

from matplotlib import pyplot as plt

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})

canvas = PyOptiCADCanvas()
x1 = Point(0, 0, 0)
a = 1.5
b = 1.5
r = 0.5
parabolicSurface1 = Convex_Paraboloid(a, b, center=x1, radius=r, name='P1', mediumBefore='Air', mediumAfter='BK7',
                                      color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
parabolicSurface1.showNormal()

# screen = RectangularScreen(Point(0.0, 0.0, 2.5), color= Color('green', alpha=0.9))


ray1Start = Point(0.2, 0.2, -0.5, parentCanvas=canvas)
ray1Start.show(color='b')
ray2Start = Point(0.2, 0.3, -0.3, parentCanvas=canvas)
ray2Start.show(color='b')
ray_dir = dc_from_points(ray1Start, ray2Start)
# incidentRay1 = Ray(ray1Start, rayDirection=ray_dir, name='R1', length=1.2, wavelength=0.35, color='green', dc=True, parentCanvas=canvas)
incidentRay1 = Ray(ray2Start, rayDirection=Z_AXIS_DIRECTION, name='R1', length=1.2, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)

xc, yc, zc = x1.get_coordinates()

A, E = b ** 2, a ** 2
I = -A * E / 2  # -a^2*b^2/2
D = -A * xc
G = -E * yc
B = 0
C = 0
H = 0
F = 0
J = (b * b * xc * xc) + (a * a * yc * yc) + (a * a * b * b * zc)
print("n=", incidentRay1.get_Direction(), "x1=", x1.get_coordinates())
print("J=", J)
parabolicSurface1.create_quadric(A, B, C, D, E, F, G, H, I, J)
print("Q = ", parabolicSurface1.Q)

intersection_distance = parabolicSurface1.calculate_quadric_intersection(incidentRay1)
intersection_point = incidentRay1.get_StartPoint() + (intersection_distance * incidentRay1.get_Direction())
print("Intersection point, distance, shape= ", intersection_point, intersection_distance,
      np.shape(intersection_distance))
P = Point(intersection_point[0], intersection_point[1], intersection_point[2], parentCanvas=canvas)
P.show(color='r')

n1 = parabolicSurface1.calculate_quadric_normal(Point(intersection_point))

# Reflection
# r1 = incidentRay1.calculate_ReflectedRay(parabolicSurface1)
# ray1 = r1.get_Direction()
print("normals current, actual = ", n1)  # , ray1)

normal_quadric = Ray(intersection_point, n1, name='quadric_normal', dc=True, color='red', parentCanvas=canvas)
# normal_actual=Ray(intersection_point, ray1, name='actual', dc=True, color='yellow', parentCanvas=canvas)

canvas.show()  # Display the PyOptiCAD canvas
