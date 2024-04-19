import numpy as np

import sys

from vispy import scene

import vispy as vispy

from raytracing.component.miscellaneous_components import XYZAxis_Labeled, OpticalAxis

from raytracing.component.detectors import RectangularScreen

from raytracing.component.sources import Ray, CircularBeam

from raytracing.component.opticalPrimitives.rectangularSurface import RectangularSurface

from raytracing.component.pyOptiCADCanvas import PyOptiCADCanvas

from vispy.color import Color

from matplotlib import pyplot as plt

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})

canvas = PyOptiCADCanvas()
# canvas = scene.SceneCanvas(keys='interactive', bgcolor='w')
# view = canvas.central_widget.add_view()
# view.camera = scene.TurntableCamera(up='y', fov=30)
#
# canvas.bgcolor = Color(color="lightsteelblue", alpha=0.5)
XYZAxis_Labeled(parent=canvas)#view.scene)

opticalAxis=OpticalAxis()
# view.add(opticalAxis.get_visual())

plane1=RectangularSurface((0,0,0.5), mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
plane1.rotate_aboutX(-20)
plane1.rotate_aboutY(180)
# view.add(plane1.get_Visual())
# view.add(plane1.get_normalVisual())

plane2=RectangularSurface((0,0,1.1),mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3), parentCanvas=canvas)
plane2.rotate_aboutX(20)
plane2.rotate_aboutY(180)
# view.add(plane2.get_Visual())
# view.add(plane2.get_normalVisual())
"""
screen = RectangularScreen(np.array((0.0, 0.0, 2.5)), color= Color('green', alpha=0.9), parent=canvas)


ray1Start = np.array((0.0, 0.0, 0.0))
ray1Direction = np.array((0, 0, 1))

ray2Start = np.array((0.0, -0.1, 0.0))
ray2Direction = np.array((0, 0, 1))

incidentRay1 = Ray(ray1Start, ray1Direction, length=1.2, wavelength=0.35, color='green', dc=True)
incidentRay2 = Ray(ray2Start, ray2Direction, wavelength=0.85, color='yellow', dc=True)


# Reflection
# reflectedRay1 = incidentRay1.calculate_ReflectedRay(plane1)
# reflectedRay2 = incidentRay2.calculate_ReflectedRay(plane2)
# view.add(reflectedRay1.get_visual())
# view.add(reflectedRay2.get_visual())
#
# Refraction
refractedRay11=incidentRay1.calculate_RefractedRay(plane1)
refractedRay21=incidentRay2.calculate_RefractedRay(plane1)

refractedRay12=refractedRay11.calculate_RefractedRay(plane2)
refractedRay22=refractedRay21.calculate_RefractedRay(plane2)


point1=np.array((0,0,0))
point2=np.array((0,0,1))
l=np.linalg.norm(point2-point1)
direction_ratios = point2-point1
direction = direction_ratios / np.linalg.norm(direction_ratios)
# print(direction)
testRay=Ray(point1,direction,length=l,color='cyan')
beam1 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.85, color='red')
beam2 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.35, color='indigo')
beam3 = CircularBeam(point1, beamDirection=direction, radius=0.2, noOfRays=32, wavelength=0.55, color='green')
beam1.combineWith(beam2)
beam1.combineWith(beam3)

refractedBeam1 = beam1.calculate_RefractedBeam(surface=plane1)
refractedBeam2 = refractedBeam1.calculate_RefractedBeam(surface=plane2)
screenIntersections, colors = screen.calculate_BeamIntersectionPoints(beam=refractedBeam2)
#
# --------  Display beams ----------------
for ray in beam1.get_Rays():
	view.add(ray.get_visual())
for ray in refractedBeam1.get_Rays():
	view.add(ray.get_visual())
for ray in refractedBeam2.get_Rays():
	view.add(ray.get_visual())
#"" "
view.add(incidentRay1.get_visual())
view.add(incidentRay2.get_visual())
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
# """
if __name__ == '__main__':
	canvas.show()
	if sys.flags.interactive == 0:
		vispy.app.run()
