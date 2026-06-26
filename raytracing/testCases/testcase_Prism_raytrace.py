from component import opticsLabCanvas, Point, Z_AXIS_DIRECTION, dc_from_points

from component.detectors import RectangularScreen

from component.sources import Ray, CircularBeam

from component.opticalPrimitives.rectangularSurface import RectangularSurface

from vispy.color import Color

from spotDiagram_matplotlib import SpotDiagram

from matplotlib import pyplot as plt

import numpy as np

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})


canvas=opticsLabCanvas()
plane1=RectangularSurface((0,0,0.5), name='P1', mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
plane1.rotate_aboutX(-20)
plane1.rotate_aboutY(180)
plane1.showNormal()

plane2=RectangularSurface((0,0,1.1), name='P2', mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
plane2.rotate_aboutX(20)
plane2.rotate_aboutY(180)
plane2.showNormal()

screen = RectangularScreen((0.0, 0.0, 2.5), color= Color('green', alpha=0.9))


ray1Start = Point(0.0, 0.1, 0.0, parentCanvas=canvas)
ray1Direction = Z_AXIS_DIRECTION

ray2Start = Point(0.0, -0.1, 0.0, parentCanvas=canvas)
ray2Direction = Z_AXIS_DIRECTION

incidentRay1 = Ray(ray1Start, ray1Direction, length=1.2, wavelength=0.35, color='green', parentCanvas=canvas)
incidentRay2 = Ray(ray2Start, ray2Direction, wavelength=0.85, color='yellow', parentCanvas=canvas)

# Reflection
reflectedRay1 = incidentRay1.calculate_ReflectedRay(plane1)
reflectedRay2 = incidentRay2.calculate_ReflectedRay(plane2)

# Refraction
refractedRay11=incidentRay1.calculate_RefractedRay(plane1)
refractedRay21=incidentRay2.calculate_RefractedRay(plane1)

refractedRay12=refractedRay11.calculate_RefractedRay(plane2)
refractedRay22=refractedRay21.calculate_RefractedRay(plane2)


point1=Point(0,0,0, parentCanvas=canvas)
point2=Point(0,0,1, parentCanvas=canvas)
direction = dc_from_points(point1, point2)
print(direction)

# testRay=Ray(point1,direction,length=l,color='cyan')
beam1 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.85, color='red', dc=True, parentCanvas=canvas)
beam2 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.35, color='indigo', dc=True, parentCanvas=canvas)
beam3 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.55, color='green', dc=True, parentCanvas=canvas)
beam1.combineWith(beam2)
beam1.combineWith(beam3)

refractedBeam1 = beam1.calculate_RefractedBeam(surface=plane1)
refractedBeam2 = refractedBeam1.calculate_RefractedBeam(surface=plane2)
screenIntersections, colors = screen.calculate_BeamIntersectionPoints(beam=refractedBeam2)

spotDiagram = SpotDiagram(screenIntersections[:,0], screenIntersections[:,1], marker='+', colors=colors)
canvas.show()
plt.show()
