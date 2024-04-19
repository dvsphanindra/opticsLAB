import numpy as np

from component.miscellaneous_components import display_point

from component.detectors import RectangularScreen

from component.sources import Ray, Ray_throughPoints, CircularBeam

from component import X_AXIS_DIRECTION, Y_AXIS_DIRECTION, Z_AXIS_DIRECTION, ORIGIN, deg2DC, calculate_DirectionAngles, \
	Z_AXIS_NEG_DIRECTION, Y_AXIS_NEG_DIRECTION, dc_from_points

from component.opticalPrimitives.rectangularSurface import RectangularSurface

from component import PyOptiCADCanvas, Point

from vispy.color import Color

from matplotlib import pyplot as plt

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})

canvas = PyOptiCADCanvas()
x1 = Point(0, 0, 1.5)
plane1 = RectangularSurface(x1, name='P1', mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3),
                            parentCanvas=canvas)
# plane1.rotate_aboutX(-60)
plane1.rotate_aboutY(150)
plane1.showNormal()

x2 = Point(1.7, 0, 0.45)
plane2 = RectangularSurface(x2, name='P2', mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3),
                            parentCanvas=canvas)
plane2.rotate_aboutX(-0.5)
plane2.rotate_aboutY(270)
plane2.showNormal()

x3 = Point(0.7, 0.35, 0.7)
plane3 = RectangularSurface(x3, name='P3', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
plane3.rotate_aboutY(40)
plane3.showNormal()

screen = RectangularScreen(Point(0.0, 0.0, 2.5), color=Color('green', alpha=0.9))

ray1Start = Point(-0.3, 0.2, 0.0, parentCanvas=canvas)
point_z = Point(-0.2, 0.2, 0.3, parentCanvas=canvas)
point_x = Point(0.2, 0.2, 0.1, parentCanvas=canvas)

# ray1Direction = np.array((90, 90, 0))
ray1Start.show(color='g')
point_z.show(color='g')
point_x.show(color='cyan')
ray2Start = Point(-0.4, -0.1, 0.2, parentCanvas=canvas)
ray2Start.show(color='y')
# ray2Direction = np.array((90, 90, 0))
ray2Direction = Z_AXIS_DIRECTION

incidentRay1 = Ray_throughPoints(ray1Start, point_z, name='R1', length=1.2, wavelength=0.35, color='green', dc=True,
                                 parentCanvas=canvas)
incidentRay2 = Ray(ray2Start, ray2Direction, name='R2', wavelength=0.85, color='yellow', parentCanvas=canvas)
incidentRay3 = Ray_throughPoints(ray1Start, point_x, name='R3', color='cyan', parentCanvas=canvas)

# Reflection
r1 = incidentRay1.calculate_ReflectedRay(plane1)  # .calculate_ReflectedRay(plane3).calculate_ReflectedRay(plane2)
r2 = incidentRay2.calculate_ReflectedRay(plane1).calculate_ReflectedRay(plane2)  # .calculate_ReflectedRay(plane2)
r3 = incidentRay3.calculate_ReflectedRay(plane2).calculate_ReflectedRay(plane3).calculate_ReflectedRay(plane1).calculate_ReflectedRay(plane2)

a, b = 76, 90
c = calculate_DirectionAngles(a, b)
print(a, b, c)
beam2 = CircularBeam(center=Point(-0.6, 0.25, 0, parentCanvas=canvas), beamDirection=(a, b, c), radius=0.3, noOfRays=64,
                     wavelength=0.85, color='maroon', dc=False, parentCanvas=canvas)
beam2.calculate_ReflectedBeam(plane1).calculate_ReflectedBeam(plane2).calculate_ReflectedBeam(plane3)

canvas.show()  # Display the PyOptiCAD canvas
