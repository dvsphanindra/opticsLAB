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
plane1 = RectangularSurface(Point(0, 0, 0.8), mediumBefore='Air', mediumAfter='BK7',
                            color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
# plane1.rotate_aboutX(-60)
# plane1.rotate_aboutY(150)
plane1.showNormal()

# plane2=RectangularSurface(Point(1.7,0,0), mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
# plane2.rotate_aboutX(20)
# plane2.rotate_aboutY(270)
# plane2.showNormal()

plane3 = RectangularSurface(Point(0, 0, 1.5), color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
plane3.rotate_aboutY(45)
plane3.showNormal()

screen = RectangularScreen(Point(0.0, 0.0, 2.5), color=Color('green', alpha=0.9))

ray1Start = Point(-0.3, 0.2, 0.0, parentCanvas=canvas)
point_z = Point(-0.2, 0.2, 0.3, parentCanvas=canvas)
point_x = Point(0.2, 0.2, 0.1, parentCanvas=canvas)

# ray1Direction = np.array((90, 90, 0))
ray1Start.show(color='g')
point_z.show(color='g')
point_x.show(color='cyan')
ray2Start = Point(-0.3, -0.1, 0.0, parentCanvas=canvas)
ray2Start.show(color='y')
# ray2Direction = np.array((90, 90, 0))
ray2Direction = Z_AXIS_DIRECTION

incidentRay1 = Ray_throughPoints(ray1Start, point_z, length=1.2, wavelength=0.35, color='green', dc=True,
                                 parentCanvas=canvas)
incidentRay2 = Ray(ray2Start, ray2Direction, wavelength=0.85, color='yellow', parentCanvas=canvas)
incidentRay3 = Ray_throughPoints(ray1Start, point_x, color='cyan', parentCanvas=canvas)

# Reflection
# r1 = incidentRay1.calculate_ReflectedRay(plane1).calculate_ReflectedRay(plane3)#.calculate_ReflectedRay(plane2)
# r2 = incidentRay2.calculate_ReflectedRay(plane1)#.calculate_ReflectedRay(plane3).calculate_ReflectedRay(plane2)
# r3 = incidentRay3.calculate_ReflectedRay(plane2).calculate_ReflectedRay(plane3).calculate_ReflectedRay(plane1)
#
# Refraction
rr1 = incidentRay1.calculate_RefractedRay(plane1).calculate_RefractedRay(plane3)
rr2 = incidentRay2.calculate_RefractedRay(plane1).calculate_RefractedRay(plane3)

"""
# testRay=Ray(point1,direction,length=l,color='cyan')
# a,b=90, 180
# # c=calculate_DirectionAngles(a,b)
# # print(a,b,c)
# # beam1 = CircularBeam(center=ORIGIN, beamDirection=Y_AXIS_NEG_DIRECTION, radius=0.4, noOfRays=32, wavelength=0.85, color='red', dc=False)
# # beam2 = CircularBeam(center=ORIGIN, beamDirection=(a,b,c), radius=0.3, noOfRays=64, wavelength=0.85, color='green', dc=False, parentCanvas=canvas)
# # beam3 = CircularBeam(center=(0.1,0.1,0.1), beamDirection=(b,a,c), radius=0.25, noOfRays=32, wavelength=0.85, color='green', dc=False)
beam1.combineWith(beam2)
beam1.combineWith(beam3)

refractedBeam1 = beam1.calculate_RefractedBeam(surface=plane1)
refractedBeam2 = refractedBeam1.calculate_RefractedBeam(surface=plane2)
screenIntersections, colors = screen.calculate_BeamIntersectionPoints(beam=refractedBeam2)
#
#"""
"""

colorInfo=[]
for color in colors:
	colorInfo.append(Color(color).__getattribute__("rgb"))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.scatter(screenIntersections[:,0],screenIntersections[:,1],marker='+',color=colorInfo)
#Move left y-axis and bottom x-axis to centre, passing through (0,0)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
plt.grid(True)

# Eliminate upper and right axes
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
#
# Show ticks in the left and lower axes only
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
plt.show()
# """

canvas.show()  # Display the PyOptiCAD canvas
