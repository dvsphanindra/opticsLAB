from opticsLAB.raytracing.component import OpticsLabCanvas, Z_AXIS_DIRECTION
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from opticsLAB.raytracing.component.sources import Ray
from opticsLAB.raytracing.component.primitives.conicSurface import ConicSurface
import numpy as np
from opticsLAB.raytracing.component.primitives.hyperbolicSurface import Hyperbolic_Surface
from opticsLAB.raytracing.component.detectors import RectangularScreen
from opticsLAB.raytracing.component.primitives.LensSideWall import LensSideWall
canvas = OpticsLabCanvas()

# def build_classical_cassegrain(canvas):
#     mm = 1e-3
#
#     # From prescription:
#     # Primary:
#     #   Diameter = 2115 mm
#     #   f1 = 5670 mm
#     #   R1 = -11340 mm (concave, sign convention)
#     #   K1 = -1.0 (paraboloid)
#     #   Hole = 211.5 mm
#
#     primary_mirror = ConicSurface(
#         radius=2115.0 * mm / 2.0,
#         centerHoleRadius=211.5 * mm,
#         RoC=-11340.00 * mm,
#         K=-1.0000,
#         center=(0, 0, 0),#8000.0 * mm-2000.0*mm),
#         mediumAfter='BK7',
#         mediumBefore='Air',
#         name="Primary Mirror",
#         color=(0.5, 0.7, 1.0, 0.5),
#         parentCanvas=canvas
#     )
#
#     # Secondary:
#     #   Diameter = 530 mm
#     #   R2 = -3114.16 mm
#     #   K2 = -2.4984 (hyperboloid)
#     #   Vertex distance from primary = 4463.27 mm (in front of primary, positive z)
#
#     secondary_mirror = ConicSurface(
#         radius=530.0 * mm / 2.0,
#         centerHoleRadius=0.0,
#         RoC=-3114.16 * mm,  # try negative first; if no hit, flip to +3114.16
#         K=-2.4984,
#         center=(0, 0, -4463.27 * mm),#8000.0 * mm -4463.27 * mm -2000 * mm),  # POSITIVE: in front of primary
#         #xTilt=180.0,
#         mediumAfter='BK7',
#         mediumBefore='Air',
#         name="Secondary Mirror",
#         color=(0.7, 1.0, 0.5, 0.8),
#         parentCanvas=canvas
#     )
#
#     # secondary_mirror = Hyperbolic_Surface(
#     #     radius=530.0 * mm / 2.0,
#     #     centerHoleRadius=0.0,
#     #         R=-3114.16 * mm,  # try negative first; if no hit, flip to +3114.16
#     #         K=-2.4984,
#     #         center=(0, 0, 8000.0 * mm -4463.27 * mm -2000 * mm),  # POSITIVE: in front of primary
#     #         mediumAfter='BK7',
#     #         mediumBefore='Air',
#     #         name="Secondary Mirror",
#     #         color=(0.7, 1.0, 0.5, 0.8),
#     #         parentCanvas=canvas
#     #
#     # )
#
#
#     return primary_mirror, secondary_mirror

def build_classical_cassegrain(canvas):
    import numpy as np
    from types import SimpleNamespace
    from opticsLAB.raytracing.component.primitives.conicSurface import ConicSurface
    from opticsLAB.raytracing.component.primitives.LensSideWall import LensSideWall

    mm = 1e-3

    primary_thickness = 0.120
    secondary_thickness = 0.040

    primary_radius = 2115.0 * mm / 2.0
    primary_hole_radius = 211.5 * mm / 2.0
    secondary_radius = 530.0 * mm / 2.0

    primary_center = np.array((0.0, 0.0, 0.0), dtype=float)
    secondary_center = np.array((0.0, 0.0, -4463.27 * mm), dtype=float)

    # Back surfaces sit behind the optical front surface
    primary_back_center = primary_center + np.array((0.0, 0.0, primary_thickness), dtype=float)
    secondary_back_center = secondary_center + np.array((0.0, 0.0, secondary_thickness), dtype=float)

    # Sidewall should be centered midway between front and back
    primary_sidewall_center = 0.5 * (primary_center + primary_back_center)
    secondary_sidewall_center = 0.5 * (secondary_center + secondary_back_center)

    # -------------------------------------------------
    # PRIMARY FRONT OPTICAL SURFACE
    # -------------------------------------------------
    primary_mirror = ConicSurface(
        radius=primary_radius,
        centerHoleRadius=primary_hole_radius,
        RoC=-11340.00 * mm,
        K=-1.0000,
        center=tuple(primary_center),
        mediumAfter='BK7',
        mediumBefore='Air',
        name="Primary Mirror",
        color=(0.55, 0.75, 1.0, 0.90),
        parentCanvas=canvas
    )

    # -------------------------------------------------
    # PRIMARY BACK VISUAL SURFACE
    # -------------------------------------------------
    primary_back = ConicSurface(
        radius=primary_radius,
        centerHoleRadius=primary_hole_radius,
        RoC=-11340.00 * mm,
        K=-1.0000,
        center=tuple(primary_back_center),
        mediumAfter='BK7',
        mediumBefore='Air',
        name="Primary Mirror Back",
        color=(0.18, 0.18, 0.22, 0.35),
        parentCanvas=canvas
    )

    primary_adapter = SimpleNamespace()
    primary_adapter.radius = primary_radius
    primary_adapter.thickness = primary_thickness
    primary_adapter.center = primary_sidewall_center
    primary_adapter._frame = primary_mirror

    def primary_front_local_z(x, y):
        return primary_mirror.function(x, y)

    def primary_back_local_z(x, y):
        return primary_back.function(x, y)

    primary_adapter._front_local_z = primary_front_local_z
    primary_adapter._back_local_z = primary_back_local_z

    primary_sidewall = LensSideWall(
        lens=primary_adapter,
        name="Primary SideWall",
        color=(0.30, 0.30, 0.34, 0.65),
        parentCanvas=canvas
    )

    # -------------------------------------------------
    # SECONDARY FRONT OPTICAL SURFACE
    # -------------------------------------------------
    secondary_mirror = ConicSurface(
        radius=secondary_radius,
        centerHoleRadius=0.0,
        RoC=-3114.16 * mm,
        K=-2.4984,
        center=tuple(secondary_center),
        mediumAfter='BK7',
        mediumBefore='Air',
        name="Secondary Mirror",
        color=(0.70, 1.00, 0.55, 0.90),
        parentCanvas=canvas
    )

    # -------------------------------------------------
    # SECONDARY BACK VISUAL SURFACE
    # -------------------------------------------------
    secondary_back = ConicSurface(
        radius=secondary_radius,
        centerHoleRadius=0.0,
        RoC=-3114.16 * mm,
        K=-2.4984,
        center=tuple(secondary_back_center),
        mediumAfter='BK7',
        mediumBefore='Air',
        name="Secondary Mirror Back",
        color=(0.20, 0.20, 0.24, 0.35),
        parentCanvas=canvas
    )

    secondary_adapter = SimpleNamespace()
    secondary_adapter.radius = secondary_radius
    secondary_adapter.thickness = secondary_thickness
    secondary_adapter.center = secondary_sidewall_center
    secondary_adapter._frame = secondary_mirror

    def secondary_front_local_z(x, y):
        return secondary_mirror.function(x, y)

    def secondary_back_local_z(x, y):
        return secondary_back.function(x, y)

    secondary_adapter._front_local_z = secondary_front_local_z
    secondary_adapter._back_local_z = secondary_back_local_z

    secondary_sidewall = LensSideWall(
        lens=secondary_adapter,
        name="Secondary SideWall",
        color=(0.30, 0.32, 0.28, 0.65),
        parentCanvas=canvas
    )

    return primary_mirror, secondary_mirror


from vispy.color import Color

def trace_bundle(primary_mirror, secondary_mirror, canvas):
    start_points = [
        (0.0, 0.0, -6.0),
        (0.0, 0.5, -6.0),
        (0.0, -0.5, -6.0),
        (0.5, 0.0, -6.0),
        (-0.5, 0.0, -6.0),
        (0.0, 0.7, -6.0),
        (0.0, -0.7, -6.0),
        (0.7, 0.0, -6.0),
        (-0.7, 0.0, -6.0),
        (0.5, 0.5, -6.0),
        (-0.5, -0.5, -6.0),
    ]

    detector_z = 0.900

    screen = RectangularScreen(
        center=Point(0.0, 0.0, detector_z),
        width=1.0,
        height=1.0,
        color=Color('green', alpha=0.5),
        parent=canvas
    )

    for start in start_points:
        ray = Ray(
            Point(start),
            rayDirection=Z_AXIS_DIRECTION,
            wavelength=0.530,
            color="green",
            dc=False,
            parentCanvas=canvas
        )

        ray1 = primary_mirror.calculate_ReflectedRay(ray)
        if ray1 is None:
            print(f"Primary miss: {start}")
            continue

        print("After primary: dir =", ray1.get_Direction())

        ray2 = secondary_mirror.calculate_ReflectedRay(ray1)
        if ray2 is None:
            print(f"Secondary miss: {start}")
            continue

        print(f"{start} -> ray2 dir = {ray2.get_Direction()}")

        result = screen.calculate_RayIntersection(ray2)
        if result is None:
            print(f"{start} -> Missed the screen!")
            continue

        hit, hit_color = screen.stop_ray_on_screen(ray2)

        if hit is not None:
            print(f"{start} -> Hits Screen at [x={hit[0]:.4f}, y={hit[1]:.4f}, z={hit[2]:.4f}]")
        else:
            print(f"{start} -> Missed the screen!")

        # hit, hit_color = result
        #
        # if hit is not None:
        #     last_exit_point = np.array(ray2.get_StartPoint(), dtype=float)
        #     hit = np.array(hit, dtype=float)
        #
        #     hit_distance = np.linalg.norm(hit - last_exit_point)
        #
        #     ray2.length = hit_distance
        #
        #     if hasattr(ray2, 'update_visual'):
        #         ray2.update_visual()
        #
        #     print(f"{start} -> Hits Screen at [x={hit[0]:.4f}, y={hit[1]:.4f}, z={hit[2]:.4f}]")
        # else:
        #     print(f"{start} -> Missed the screen!")


if __name__ == "__main__":
    primary_mirror, secondary_mirror = build_classical_cassegrain(canvas)
    trace_bundle(primary_mirror, secondary_mirror, canvas)
    canvas.show()