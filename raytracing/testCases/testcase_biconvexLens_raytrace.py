from component import PyOptiCADCanvas, Point, Z_AXIS_DIRECTION, dc_from_points

from component.detectors import RectangularScreen

from component.sources import Ray, CircularBeam

from spotDiagram_matplotlib import SpotDiagram

from vispy.color import Color

from matplotlib import pyplot as plt

from component.opticalPrimitives.convexParaboloid import Convex_Paraboloid
from component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid

import numpy as np
np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})



canvas=PyOptiCADCanvas()
# Add screen
screen = RectangularScreen(np.array((0.0, 0.0, 1.5)), color= Color('green', alpha=0.9))

ray1Start = Point(0, 0.45, -0.4, parentCanvas=canvas)
ray1Direction = Z_AXIS_DIRECTION

ray2Start = Point(0, -0.35, -0.4, parentCanvas=canvas)
ray2Direction = Z_AXIS_DIRECTION

incidentRay1 = Ray(ray1Start, ray1Direction, length=1.2, wavelength=0.35, color='green', parentCanvas=canvas)
incidentRay2 = Ray(ray2Start, ray2Direction, wavelength=0.85, color='yellow', parentCanvas=canvas)

parabolicSurface1 = Convex_Paraboloid(1.5, 1.5, center=(0, 0, 0.1), radius=0.5, name='P1', mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
# parabolicSurface1.rotate_aboutY(90)

point=parabolicSurface1.calculate_RayIntersection(ray=incidentRay1)
normDir=parabolicSurface1.calculate_normalDirection(point)
print("normDir: ", normDir)
norm=Ray(point, normDir, color='black', parentCanvas=canvas, dc=True)

center2=Point(0,0,0.4, parentCanvas=canvas)
parabolicSurface2 = Concave_Paraboloid(1.5, 1.5, center=center2, radius=0.5, name='P2', mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
# parabolicSurface2.rotate_aboutY(90)
point=parabolicSurface2.calculate_RayIntersection(ray=incidentRay1)
normDir=parabolicSurface2.calculate_normalDirection(point)
print("normDir= ",normDir)
point=parabolicSurface2.transform(point)
norm=Ray(point, normDir, color='black', parentCanvas=canvas, dc=True)

# Reflection
# reflectedRay1 = incidentRay1.calculate_ReflectedRay(parabolicSurface2)
# reflectedRay2 = incidentRay2.calculate_ReflectedRay(parabolicSurface2)

#
# Refraction
refractedRay11 = incidentRay1.calculate_RefractedRay(parabolicSurface1)
refractedRay21 = incidentRay2.calculate_RefractedRay(parabolicSurface1)

refractedRay12=refractedRay11.calculate_RefractedRay(parabolicSurface2)
refractedRay22=refractedRay21.calculate_RefractedRay(parabolicSurface2)


point1=Point(0,0,0, parentCanvas=canvas)
point2=Point(0,0,1, parentCanvas=canvas)
direction = dc_from_points(point1, point2)
print(direction)

beam1 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.85, color='red', dc=True, parentCanvas=canvas)
beam2 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.35, color='indigo', dc=True, parentCanvas=canvas)
beam3 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.55, color='green', dc=True, parentCanvas=canvas)
beam1.combineWith(beam2)
beam1.combineWith(beam3)

refractedBeam1 = beam1.calculate_RefractedBeam(surface=parabolicSurface1)
refractedBeam2 = refractedBeam1.calculate_RefractedBeam(surface=parabolicSurface2)
screenIntersections, colors = screen.calculate_BeamIntersectionPoints(beam=refractedBeam2)

SpotDiagram(screenIntersections[:,0],screenIntersections[:,1], marker='+',colors=colors)

canvas.show()
plt.show()
