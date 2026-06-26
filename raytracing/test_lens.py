from opticsLAB.raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
from opticsLAB.raytracing.component import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from vispy.color import Color
from opticsLAB.raytracing.component import Z_AXIS_DIRECTION, Z_AXIS_NEG_DIRECTION
from opticsLAB.raytracing.component.sources import Ray, CircularBeam


canvas = OpticsLabCanvas()
p1 = Point(0, 0, 2)

# Lens parameters
mjr_axis = 2
mnr_axis = 2


# l1 = ParabolicLens.biconcave(a=mjr_axis, b=mnr_axis, c=-1.0, center= p1 ,thickness=0.5, mediumAfter="BK7",mediumBefore="Air",
#                           color=Color((0.1, 0.5, 1), alpha=0.1), parentCanvas=canvas)

l1 = SphericalLens.biconvex(R1=2,R2=-2,center=p1,radius=1, thickness=0.6,mediumAfter="BK7",mediumBefore="Air",
                         color=Color((0.1, 0.5, 1), alpha=0.1),parentCanvas=canvas)

rp1 = Point(0, 0.5, -3,parentCanvas=canvas)
rp1.show(color='b')

r1 = Ray(rp1,rayDirection=Z_AXIS_DIRECTION, name='R1', length=2, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)

r2 = l1.calculate_RefractedRay(r1)

#########

rp2 = Point(0, -0.5, -3,parentCanvas=canvas)
rp2.show(color='b')

rr1 = Ray(rp2,rayDirection=Z_AXIS_DIRECTION, name='R1', length=2, wavelength=0.35, color='green',
                   dc=False, parentCanvas=canvas)

rr2 = l1.calculate_RefractedRay(rr1)

canvas.show()
