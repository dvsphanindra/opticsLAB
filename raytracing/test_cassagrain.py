from erfa import apcg13
from jupyter_core.version import parts

from component import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from opticsLAB.raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
from component.opticalPrimitives.rectangularSurface import RectangularSurface
from vispy.color import Color
import numpy as np

from opticsLAB.raytracing.component import dc_from_points, Z_AXIS_DIRECTION
from opticsLAB.raytracing.component.opticalPrimitives.convexParaboloid import Convex_Paraboloid
from opticsLAB.raytracing.component.sources import Ray, Ray_throughPoints
from opticsLAB.raytracing.component.primitives.parabolicSurface import Parabolic_Surface

canvas = OpticsLabCanvas()
x1 = Point(0, 0, 2)

a = 4.5
b = 4.5
r = 1.0
parabolicSurface1 = Concave_Paraboloid(a, b, center=x1,centerHoleRadius=0.2, radius=r, name='Mirror1', mediumBefore='Air', mediumAfter='BK7',
                                      color=Color((0.1, 0.5, 1), alpha=0.1), parentCanvas=canvas)



rectangularSurface1 = RectangularSurface(Point(0, 0, -0.6), mediumBefore='Air', mediumAfter='BK7',
                            color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
#rectangularSurface1.rotate_aboutY(45)
rectangularSurface1.showNormal()

x2 = Point(0.0, 0, 2.3)
c = 0.75
d = 0.75
r = 0.25

convexparabolicSurface1 = Convex_Paraboloid(c,d,center=x2, radius=r, name='Mirror2', mediumBefore='Air',mediumAfter='BK7',
                                            color=Color((0.3, 0.3, 1), alpha=0.3),parentCanvas=canvas)
# convexparabolicSurface1.rotate_aboutY(90)

# parabolicSurface1 = RectangularSurface(Point(0, 0, 0.5), mediumBefore='Air', mediumAfter='BK7',
#                             color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
#
# parabolicSurface1.rotate_aboutY(45)

# parabolicSurface1.rotate_aboutX(30)
# parabolicSurface1.rotate_aboutY(180)

ray1Start = Point(-0.2, 0.2, -1.0, parentCanvas=canvas)

#ray1Start = np.array((1,0,0))
ray1Start.show(color='b')
incidentRay1 = Ray(ray1Start, rayDirection=Z_AXIS_DIRECTION, name='R1', length=2, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)
r1 = incidentRay1.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)
# rr1 = r1.calculate_ReflectedRay(rectangularSurface1)
# rrr1 = rr1.calculate_RefractedRay(convexparabolicSurface1)



ray2Start = Point(0.2, -0.2, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray2Start.show(color='b')
incidentRay2 = Ray(ray2Start, rayDirection=Z_AXIS_DIRECTION, name='R2', length=0.5, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)
r2 = incidentRay2.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)
# rr2 = r2.calculate_ReflectedRay(rectangularSurface1)



ray3Start = Point(-0.2, -0.2, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray3Start.show(color='b')
incidentRay3 = Ray(ray3Start, rayDirection=Z_AXIS_DIRECTION, name='R3', length=0.5, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)
r3 = incidentRay3.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)
# rr3 = r3.calculate_ReflectedRay(rectangularSurface1)



ray4Start = Point(0.2, 0.2, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray4Start.show(color='b')
incidentRay4 = Ray(ray4Start, rayDirection=Z_AXIS_DIRECTION, name='R4', length=0.5, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)
r4 = incidentRay4.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)
#rr4 = r4.calculate_ReflectedRay(rectangularSurface1)
#
#
# ################################################################
#
ray11Start = Point(-0.4, 0.4, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray11Start.show(color='b')
incidentRay11 = Ray(ray11Start, rayDirection=Z_AXIS_DIRECTION, name='R11', length=0.5, wavelength=0.35, color='red',
                   dc=False, parentCanvas=canvas)
r11 = incidentRay11.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)

ray12Start = Point(0.4, -0.4, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray12Start.show(color='b')
incidentRay12 = Ray(ray12Start, rayDirection=Z_AXIS_DIRECTION, name='R12', length=0.5, wavelength=0.35, color='red',
                   dc=False, parentCanvas=canvas)
r12 = incidentRay12.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)

ray13Start = Point(-0.4, -0.4, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray13Start.show(color='b')
incidentRay13 = Ray(ray13Start, rayDirection=Z_AXIS_DIRECTION, name='R13', length=0.5, wavelength=0.35, color='red',
                   dc=False, parentCanvas=canvas)
r13 = incidentRay13.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)


ray14Start = Point(0.4, 0.4, -1.0, parentCanvas=canvas)

# ray1Start = np.array((1,0,0))
ray14Start.show(color='b')
incidentRay14 = Ray(ray14Start, rayDirection=Z_AXIS_DIRECTION, name='R14', length=0.5, wavelength=0.35, color='red',
                   dc=False, parentCanvas=canvas)
r14 = incidentRay14.calculate_ReflectedRay(parabolicSurface1).calculate_ReflectedRay(rectangularSurface1).calculate_RefractedRay(convexparabolicSurface1)#.calculate_RefractedRay(convexparabolicSurface2)

"""ray1Start = Point(-0.3, 0.2, 0.0, parentCanvas=canvas)
point_z = Point(-0.2, 0.2, 0.3, parentCanvas=canvas)
point_x = Point(0.2, 0.2, 0.1, parentCanvas=canvas)

ray1Start.show(color='g')
point_z.show(color='g')
point_x.show(color='cyan')
ray2Start = Point(-0.4, -0.1, 0.2, parentCanvas=canvas)
ray2Start.show(color='y')
# ray2Direction = np.array((90, 90, 0))
ray2Direction = Z_AXIS_DIRECTION

incidentRay1 = Ray_throughPoints(ray1Start, point_z, name='R1', length=1.2, wavelength=0.35, color='green', dc=True,
                                 parentCanvas=canvas)
incidentRay2 = Ray(ray2Start, ray2Direction, name='R2', wavelength=0.85, color='yellow', parentCanvas=canvas)"""

canvas.show()  # Display the opticsLab canvas

