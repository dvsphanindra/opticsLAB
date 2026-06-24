import numpy as np
from ..primitives.parabolicSurface import Parabolic_Surface
from ..primitives.plane import Plane
from ..opticalPrimitives.Lens import Lens

class ParabolicLens(Lens):
    def __init__(self, a=1.0, b=1.0, c_front=-1.0, c_back=1.0, **kwargs):
        self.a = a
        self.b = b
        self.c_front = c_front
        self.c_back = c_back
        super().__init__(**kwargs)

    def _build_surfaces(self):
        front_center = self.center - np.array([0.0, 0.0, self.thickness / 2.0])
        back_center  = self.center + np.array([0.0, 0.0, self.thickness / 2.0])

        if abs(self.c_front) < 1e-12:
            self.front = Plane(
                radius=self.radius, width=2*self.radius, length=2*self.radius,
                center=front_center, name="Front", color=self.color,
                mediumBefore=self.mediumBefore, mediumAfter=self.mediumAfter,
                parentCanvas=self.parentCanvas
            )
        else:
            self.front = Parabolic_Surface(
                a=self.a, b=self.b, c=self.c_front,
                radius=self.radius, center=front_center,
                name="Front", color=self.color,
                mediumBefore=self.mediumBefore, mediumAfter=self.mediumAfter,
                parentCanvas=self.parentCanvas
            )

        if abs(self.c_back) < 1e-12:
            self.back = Plane(
                radius=self.radius, width=2*self.radius, length=2*self.radius,
                center=back_center, name="Back", color=self.color,
                mediumBefore=self.mediumAfter, mediumAfter=self.mediumBefore,
                parentCanvas=self.parentCanvas
            )
        else:
            self.back = Parabolic_Surface(
                a=self.a, b=self.b, c=self.c_back,
                radius=self.radius, center=back_center,
                name="Back", color=self.color,
                mediumBefore=self.mediumAfter, mediumAfter=self.mediumBefore,
                parentCanvas=self.parentCanvas
            )

    def _front_local_z(self, x, y):
        return self.c_front * ((x / self.a) ** 2 + (y / self.b) ** 2)

    def _back_local_z(self, x, y):
        return self.c_back * ((x / self.a) ** 2 + (y / self.b) ** 2)

    @classmethod
    def biconvex(cls, a=1.0, b=1.0, c=1.0, **kwargs):
        """
        Both surfaces bulge outward.
        front: convex (c_front > 0)
        back:  convex (c_back < 0)
        """
        return cls(a=a, b=b, c_front=abs(c), c_back=-abs(c), **kwargs)

    @classmethod
    def biconcave(cls, a=1.0, b=1.0, c=1.0, **kwargs):
        """
        Both surfaces curve inward.
        front: concave (c_front < 0)
        back:  concave (c_back > 0)
        """
        return cls(a=a, b=b, c_front=-abs(c), c_back=abs(c), **kwargs)

    @classmethod
    def plano_convex(cls, a=1.0, b=1.0, c=1.0, flat_surface="front", **kwargs):
        """
        One flat surface, one outward-bulging surface.
        Default: front flat, back convex (converging lens).

        flat_surface: "front" or "back"
        """
        if flat_surface == "front":
            c_front = 0.0
            c_back = -abs(c)  # back convex
        else:  # flat_surface == "back"
            c_front = abs(c)  # front convex
            c_back = 0.0
        return cls(a=a, b=b, c_front=c_front, c_back=c_back, **kwargs)

    @classmethod
    def plano_concave(cls, a=1.0, b=1.0, c=1.0, flat_surface="front", **kwargs):
        """
        One flat surface, one inward-curving surface.
        Default: front flat, back concave (diverging lens).

        flat_surface: "front" or "back"
        """
        if flat_surface == "front":
            c_front = 0.0
            c_back = abs(c)  # back concave
        else:  # flat_surface == "back"
            c_front = -abs(c)  # front concave
            c_back = 0.0
        return cls(a=a, b=b, c_front=c_front, c_back=c_back, **kwargs)

    @classmethod
    def meniscus(cls, a=1.0, b=1.0, c=None, c_front=None, c_back=None, **kwargs):
        """
        Both surfaces curve in the same direction.
        Default (when c is given): front convex, back less convex (converging meniscus).
        """
        if c is not None:
            if c_front is None:
                c_front = abs(c)
            if c_back is None:
                c_back = 0.5 * abs(c)

        if c_front is None:
            c_front = 1.0
        if c_back is None:
            c_back = 0.5

        return cls(a=a, b=b, c_front=c_front, c_back=c_back, **kwargs)