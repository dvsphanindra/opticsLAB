import numpy as np

import sys

from vispy import scene

import vispy as vispy

from pyOptiCAD.raytracing.component.miscellaneous_components import XYZAxis_Labeled, OpticalAxis

from pyOptiCAD.raytracing.component.detectors import RectangularScreen

from pyOptiCAD.raytracing.component.sources import Ray, CircularBeam

from vispy.color import Color

from matplotlib import pyplot as plt

from pyOptiCAD.raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
from pyOptiCAD.raytracing.component.opticalPrimitives.convexParaboloid import Convex_Paraboloid


np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})



canvas = scene.SceneCanvas(keys='interactive', bgcolor='w')
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='y', fov=30)

canvas.bgcolor = Color(color="lightsteelblue", alpha=0.5)
XYZAxis_Labeled(parent=view.scene)

opticalAxis=OpticalAxis()
view.add(opticalAxis.get_visual())

# Add screen
screen = RectangularScreen(np.array((0.0, 0.0, 1.5)), color= Color('green', alpha=0.9))

ray1Start = np.array((0, 0.45, -0.4))
ray1Direction = np.array((0, 0, 1))

ray2Start = np.array((0, -0.35, -0.4))
ray2Direction = np.array((0, 0, 1))

incidentRay1 = Ray(ray1Start, ray1Direction, wavelength=0.35, color='green')
incidentRay2 = Ray(ray2Start, ray2Direction, wavelength=0.85, color='yellow')

parabolicSurface1 = Convex_Paraboloid(1.5, 1.5, center=(0, 0, 0.1), radius=0.5, mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3))
# parabolicSurface1.rotate_aboutY(90)
view.add(parabolicSurface1.get_Visual())
point=parabolicSurface1.calculate_RayIntersection(ray=incidentRay1)
normDir=parabolicSurface1.calculate_normalDirection(point)
print("normDir: ", normDir)
norm=Ray(point, normDir, color='black')
view.add(norm.get_visual())

center2=np.array((0,0,0.4))
parabolicSurface2 = Concave_Paraboloid(1.5, 1.5, center=center2, mediumBefore='BK7', mediumAfter='Air', radius=0.5, color=Color((0.3, 0.3, 1), alpha=0.3))
# parabolicSurface2.rotate_aboutY(90)
view.add(parabolicSurface2.get_Visual())
point=parabolicSurface2.calculate_RayIntersection(ray=incidentRay1)
normDir=parabolicSurface2.calculate_normalDirection(point)
print("normDir= ",normDir)
point=parabolicSurface2.transform(point)
norm=Ray(point, normDir, color='black')
view.add(norm.get_visual())

# Reflection
# reflectedRay1 = incidentRay1.calculate_ReflectedRay(parabolicSurface2)
# reflectedRay2 = incidentRay2.calculate_ReflectedRay(parabolicSurface2)

#
# Refraction
refractedRay11 = incidentRay1.calculate_RefractedRay(parabolicSurface1)
refractedRay21 = incidentRay2.calculate_RefractedRay(parabolicSurface1)

refractedRay12=refractedRay11.calculate_RefractedRay(parabolicSurface2)
refractedRay22=refractedRay21.calculate_RefractedRay(parabolicSurface2)

point1=np.array((0,0,-0.5))
point2=np.array((0,0,1))
l=np.linalg.norm(point2-point1)
direction_ratios = point2-point1
direction = direction_ratios / np.linalg.norm(direction_ratios)
print(direction)

beam1 = CircularBeam(point1, beamDirection=direction, radius=0.5, noOfRays=32, wavelength=0.85, color='red')
beam2 = CircularBeam(point1, beamDirection=direction, radius=0.5, noOfRays=32, wavelength=0.35, color='indigo')
beam3 = CircularBeam(point1, beamDirection=direction, radius=0.5, noOfRays=32, wavelength=0.55, color='green')
beam1.combineWith(beam2)
beam1.combineWith(beam3)

refractedBeam1 = beam1.calculate_RefractedBeam(surface=parabolicSurface1)
refractedBeam2 = refractedBeam1.calculate_RefractedBeam(surface=parabolicSurface2)
screenIntersections, colors = screen.calculate_BeamIntersectionPoints(beam=refractedBeam2)
#
# --------  Display beams ----------------
for ray in beam1.get_Rays():
	view.add(ray.get_visual())
for ray in refractedBeam1.get_Rays():
	view.add(ray.get_visual())
for ray in refractedBeam2.get_Rays():
	view.add(ray.get_visual())
#
#"""
view.add(incidentRay1.get_visual())
view.add(incidentRay2.get_visual())

# view.add(reflectedRay1.get_visual())
# view.add(reflectedRay2.get_visual())

view.add(refractedRay11.get_visual())
view.add(refractedRay21.get_visual())

view.add(refractedRay12.get_visual())
view.add(refractedRay22.get_visual())

view.add(screen.get_Visual())

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
#"""
if __name__ == '__main__':
	canvas.show()
	if sys.flags.interactive == 0:
		vispy.app.run()
