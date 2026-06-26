import numpy as np
from ..primitives.sphericalSurface import Spherical_Surface
from ..primitives.plane import Plane
from ..opticalPrimitives.Lens import Lens


class SphericalLens(Lens):
    def __init__(self, R1=None, R2=None, **kwargs):
        self.R1 = R1
        self.R2 = R2
        super().__init__(**kwargs)

    def _build_surfaces(self):
        # Front = first surface hit by rays traveling in +z
        front_center = self.center - np.array([0.0, 0.0, self.thickness / 2.0])
        back_center  = self.center + np.array([0.0, 0.0, self.thickness / 2.0])

        if self.R1 is None or np.isinf(self.R1):
            self.front = Plane(
                radius=self.radius,
                width=2 * self.radius,
                length=2 * self.radius,
                center=front_center,
                name="Front",
                color=self.color,
                mediumBefore=self.mediumBefore,
                mediumAfter=self.mediumAfter,
                parentCanvas=self.parentCanvas
            )
        else:
            self.front = Spherical_Surface(
                radius_of_curvature=self.R1,
                aperture_radius=self.radius,
                center=front_center,
                name="Front",
                color=self.color,
                mediumBefore=self.mediumBefore,
                mediumAfter=self.mediumAfter,
                parentCanvas=self.parentCanvas
            )

        if self.R2 is None or np.isinf(self.R2):
            self.back = Plane(
                radius=self.radius,
                width=2 * self.radius,
                length=2 * self.radius,
                center=back_center,
                name="Back",
                color=self.color,
                mediumBefore=self.mediumAfter,
                mediumAfter=self.mediumBefore,
                parentCanvas=self.parentCanvas
            )
        else:
            self.back = Spherical_Surface(
                radius_of_curvature=self.R2,
                aperture_radius=self.radius,
                center=back_center,
                name="Back",
                color=self.color,
                mediumBefore=self.mediumAfter,
                mediumAfter=self.mediumBefore,
                parentCanvas=self.parentCanvas
            )

    def _front_local_z(self, x, y):
        return self._sag(self.R1, x, y)

    def _back_local_z(self, x, y):
        return self._sag(self.R2, x, y)

    @staticmethod
    def _sag(R, x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if R is None or np.isinf(R):
            return np.zeros_like(x, dtype=float)

        r2 = x * x + y * y
        R2 = R * R

        sag = np.full_like(r2, np.nan, dtype=float)
        inside = r2 <= R2
        sag[inside] = R - np.sign(R) * np.sqrt(R2 - r2[inside])

        return sag

    @classmethod
    def biconvex(cls, R1, R2, **kwargs):
        return cls(R1=abs(R1), R2=-abs(R2), **kwargs)

    @classmethod
    def biconcave(cls, R1, R2, **kwargs):
        return cls(R1=-abs(R1), R2=abs(R2), **kwargs)

    @classmethod
    def plano_convex(cls, R, flat_surface="front", **kwargs):
        if flat_surface == "front":
            # front flat, back convex: R1 = inf, R2 < 0
            return cls(R1=np.inf, R2=-abs(R), **kwargs)
        else:
            # front convex, back flat: R1 > 0, R2 = inf
            return cls(R1=abs(R), R2=np.inf, **kwargs)

    @classmethod
    def plano_concave(cls, R, flat_surface="front", **kwargs):
        if flat_surface == "front":
            # front flat, back concave: R1 = inf, R2 > 0
            return cls(R1=np.inf, R2=abs(R), **kwargs)
        else:
            # front concave, back flat: R1 < 0, R2 = inf
            return cls(R1=-abs(R), R2=np.inf, **kwargs)

    @classmethod
    def meniscus(cls, R1, R2, **kwargs):
        return cls(R1=R1, R2=R2, **kwargs)