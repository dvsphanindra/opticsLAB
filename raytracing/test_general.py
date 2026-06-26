from opticsLAB.raytracing.component import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from opticsLAB.raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
from opticsLAB.raytracing.component.primitives.parabolicSurface import Parabolic_Surface
from opticsLAB.raytracing.component.primitives.lineVector import LineVector
from vispy.color import Color
import numpy as np

from opticsLAB.raytracing.component import dc_from_points, Z_AXIS_DIRECTION
from opticsLAB.raytracing.component.sources import Ray, Ray_throughPoints

canvas = OpticsLabCanvas()

x1 = Point(0, 0, 1)
a = 2.5
b = 2.5
c = -1.0

sur = Parabolic_Surface(a, b, c, center = x1, radius = 0.5, color=Color((0.1, 0.4, 1), alpha=0.1), parentCanvas=canvas)#.translate(point=np.array([0,-1,1]))#.inverse_transform(point=np.array([0,1,1]))

# ray1 = Ray(startPoint=)

startpoint = Point(0, 1, 0)
line = LineVector(start=np.array([0,0.2,0]), direction=Z_AXIS_DIRECTION,name='line1',parentCanvas=canvas)
# line.rotate([0,1,0],90)
canvas.show()