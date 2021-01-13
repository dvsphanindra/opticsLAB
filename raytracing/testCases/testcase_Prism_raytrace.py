import numpy as np

import sys

from vispy import scene

import vispy as vispy

from miscellaneous import XYZAxis_Labeled, OpticalAxis

from detectors import RectangularScreen

from sources import Ray, CircularBeam

from opticalPrimitives import RectangularSurface

from vispy.color import Color

from spotDiagram_matplotlib import SpotDiagram

from matplotlib import pyplot as plt

np.set_printoptions(precision=4, suppress=True, formatter={'float_kind': '{:0.2f}'.format})



canvas = scene.SceneCanvas(keys='interactive', bgcolor='w')
view = canvas.central_widget.add_view()
view.camera = scene.TurntableCamera(up='y', fov=30)

canvas.bgcolor = Color(color="lightsteelblue", alpha=0.5)
XYZAxis_Labeled(parent=view.scene)

opticalAxis=OpticalAxis()
view.add(opticalAxis.get_visual())

plane1=RectangularSurface((0,0,0.5), mediumBefore='Air', mediumAfter='BK7', color=Color((0.3, 0.3, 1), alpha=0.3))
plane1.rotate_aboutX(-20)
plane1.rotate_aboutY(180)
view.add(plane1.get_Visual())
view.add(plane1.get_normalVisual())

plane2=RectangularSurface((0,0,1.1),mediumBefore='BK7', mediumAfter='Air', color=Color((0.3, 0.3, 1), alpha=0.3))
plane2.rotate_aboutX(20)
plane2.rotate_aboutY(180)
view.add(plane2.get_Visual())
view.add(plane2.get_normalVisual())

screen = RectangularScreen(np.array((0.0, 0.0, 2.5)), color= Color('green', alpha=0.9))


ray1Start = np.array((0.0, 0.1, 0.0))
ray1Direction = np.array((0, 0, 1))

ray2Start = np.array((0.0, -0.1, 0.0))
ray2Direction = np.array((0, 0, 1))

incidentRay1 = Ray(ray1Start, ray1Direction, length=1.2, wavelength=0.35, color='green')
incidentRay2 = Ray(ray2Start, ray2Direction, wavelength=0.85, color='yellow')


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
#"""
view.add(incidentRay1.get_visual())
view.add(incidentRay2.get_visual())
view.add(refractedRay11.get_visual())
view.add(refractedRay21.get_visual())
view.add(refractedRay12.get_visual())
view.add(refractedRay22.get_visual())

view.add(screen.get_Visual())

spotDiagram = SpotDiagram(screenIntersections[:,0], screenIntersections[:,1], marker='+', colors=colors)

# """
if __name__ == '__main__':
	canvas.show()
	plt.show()
	if sys.flags.interactive == 0:
		vispy.app.run()
