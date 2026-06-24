import numpy as np
from vispy import scene
from vispy.scene.visuals import SurfacePlot

# Import your existing base classes
from ..primitives.conicSurface import ConicSurface
from ..primitives.plane import Plane
from ..opticalPrimitives.Lens import Lens

class ConicLens(Lens):
    """
    A generalized lens composed of two conic or planar surfaces.
    By setting R and K appropriately, it can be a spherical, parabolic,
    elliptical, or hyperbolic lens.
    """

    def __init__(self,
                 R_front=100.0, K_front=0.0,
                 R_back=-100.0, K_back=0.0,
                 **kwargs):
        self.R_front = R_front
        self.K_front = K_front
        self.R_back = R_back
        self.K_back = K_back
        super().__init__(**kwargs)

    def _build_surfaces(self):
        front_center = self.center - np.array([0.0, 0.0, self.thickness / 2.0])
        back_center = self.center + np.array([0.0, 0.0, self.thickness / 2.0])

        # Front surface setup
        if np.isinf(self.R_front):
            self.front = Plane(
                radius=self.radius, width=2 * self.radius, length=2 * self.radius,
                center=front_center, name="Front", color=self.color,
                mediumBefore=self.mediumBefore, mediumAfter=self.mediumAfter,
                parentCanvas=self.parentCanvas
            )
        else:
            self.front = ConicSurface(
                radius=self.radius, RoC=self.R_front, K=self.K_front,
                center=front_center, name="Front", color=self.color,
                mediumBefore=self.mediumBefore, mediumAfter=self.mediumAfter,
                parentCanvas=self.parentCanvas
            )

        # Back surface setup
        if np.isinf(self.R_back):
            self.back = Plane(
                radius=self.radius, width=2 * self.radius, length=2 * self.radius,
                center=back_center, name="Back", color=self.color,
                mediumBefore=self.mediumAfter, mediumAfter=self.mediumBefore,
                parentCanvas=self.parentCanvas
            )
        else:
            self.back = ConicSurface(
                radius=self.radius, RoC=self.R_back, K=self.K_back,
                center=back_center, name="Back", color=self.color,
                mediumBefore=self.mediumAfter, mediumAfter=self.mediumBefore,
                parentCanvas=self.parentCanvas
            )

    def _front_local_z(self, x, y):
        if np.isinf(self.R_front): return 0.0
        r2 = x * x + y * y
        c = 1.0 / self.R_front
        inside = np.maximum(1.0 - (1.0 + self.K_front) * c * c * r2, 0.0)
        return (c * r2) / (1.0 + np.sqrt(inside))

    def _back_local_z(self, x, y):
        if np.isinf(self.R_back): return 0.0
        r2 = x * x + y * y
        c = 1.0 / self.R_back
        inside = np.maximum(1.0 - (1.0 + self.K_back) * c * c * r2, 0.0)
        return (c * r2) / (1.0 + np.sqrt(inside))

    # --- Standard optical form helpers ---

    @classmethod
    def biconvex(cls, R_front=100.0, K_front=0.0, R_back=100.0, K_back=0.0, **kwargs):
        return cls(
            R_front=abs(R_front), K_front=K_front,
            R_back=-abs(R_back), K_back=K_back,
            **kwargs
        )

    @classmethod
    def biconcave(cls, R_front=100.0, K_front=0.0, R_back=100.0, K_back=0.0, **kwargs):
        return cls(
            R_front=-abs(R_front), K_front=K_front,
            R_back=abs(R_back), K_back=K_back,
            **kwargs
        )

    @classmethod
    def plano_convex(cls, R=100.0, K=0.0, flat_surface="front", **kwargs):
        if flat_surface == "front":
            return cls(R_front=np.inf, K_front=0.0, R_back=-abs(R), K_back=K, **kwargs)
        else:
            return cls(R_front=abs(R), K_front=K, R_back=np.inf, K_back=0.0, **kwargs)

    @classmethod
    def plano_concave(cls, R=100.0, K=0.0, flat_surface="front", **kwargs):
        if flat_surface == "front":
            return cls(R_front=np.inf, K_front=0.0, R_back=abs(R), K_back=K, **kwargs)
        else:
            return cls(R_front=-abs(R), K_front=K, R_back=np.inf, K_back=0.0, **kwargs)

    @classmethod
    def meniscus(cls, R_front=100.0, K_front=0.0, R_back=150.0, K_back=0.0, **kwargs):
        return cls(
            R_front=abs(R_front), K_front=K_front,
            R_back=abs(R_back), K_back=K_back,
            **kwargs
        )