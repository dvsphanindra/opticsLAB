import numpy as np
from matplotlib.pyplot import connect

from opticsLAB.raytracing.component.primitives.conicSurface import ConicSurface
from opticsLAB.raytracing.component.sources import Ray
from opticsLAB.raytracing.component.OpticsLabCanvas import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from opticsLAB.raytracing.component import Z_AXIS_DIRECTION, Z_AXIS_DC
from opticsLAB.raytracing.spotDiagram import SpotDiagramPlot
from opticsLAB.raytracing.component.detectors import RectangularScreen
from vispy.color import Color
from vispy import scene

canvas = OpticsLabCanvas()

def build_mirror():
    x1 = Point((0, 0, 0))

    primary = ConicSurface(radius=410.0,RoC=-3338.8,K=-1.1,
                           centerHoleRadius=50.0, center=x1,
                           mediumAfter='BK7',mediumBefore='Air',
                           color=Color((0,0.1,0.9),alpha=0.5),
                           parentCanvas=canvas)

    x2 = Point((0, 0, -1084))

    secondary = ConicSurface(radius=200.0,RoC=-1901.0,K=-6.9, center=x2,
                           mediumAfter='BK7',mediumBefore='Air',
                           color=Color((0,0.5,0.9),alpha=0.5),
                           parentCanvas=canvas)

    screen_position = Point((0, 0, 450))

    screen = RectangularScreen(screen_position,
                               width=20,
                               height=20,
                               color=Color('green', alpha=0.5),
                               parent=canvas
                               )

    return [primary, secondary], screen

def generate_aperture_rays(radius, inner_radius=200.0, z0=-1500.0, n_rays=100):
    pts = []

    n_side = int(np.ceil(np.sqrt(n_rays * 1.5)))
    xs = np.linspace(-radius, radius, n_side)
    ys = np.linspace(-radius, radius, n_side)

    for x in xs:
        for y in ys:
            r2 = x*x + y*y
            if inner_radius*inner_radius <= r2 <= radius*radius:
                pts.append((x, y, z0))

    if len(pts) > n_rays:
        idx = np.linspace(0, len(pts) - 1, n_rays, dtype=int)
        pts = [pts[i] for i in idx]

    return pts

def test_mirror():
    mirrors, screen = build_mirror()

    wavelengths = {
        "blue": 0.465,
        "green": 0.530,
        "red": 0.620
    }

    color_map = {
        "blue": [0.0, 0.0, 1.0, 1.0],
        "green": [0.0, 1.0, 0.0, 1.0],
        "red": [1.0, 0.0, 0.0, 1.0]
    }

    ray_vertices = []
    ray_colors = []
    spot_data = {}

    for name, wl in wavelengths.items():
        color_rbg = color_map.get(name, [1.0, 1.0, 1.0, 0.7])

        primary_aperture_radius = 410.0
        my_start_points = generate_aperture_rays(
            radius=primary_aperture_radius,
            z0=-1500.0,
            n_rays=100
        )

        # my_start_points = [
        #     #(0.0, 0.0, -20.0),
        #     (-5.0, 0.0, -20.0),
        #     (0.0, 5.0, -20.0), (0.0, 7.0, -20.0),
        #     (0.0, -5.0, -20.0), (0.0, -7.0, -20.0),
        #     (5.0, 0.0, -20.0), (7.0, 0.0, -20.0),
        #     (-5.0, 7.0, -20.0), (-5.0, -7.0, -20.0),
        #     (5.0, -7.0, -20.0), (5.0, 7.0, -20.0),
        #     (7.0, -5.0, -20.0), (7.0, 5.0, -20.0),
        #     (-7.0, 5.0, -20.0), (-7.0, -5.0, -20.0),
        # ]

        # FIX 2: Initialize pts outside the start_points loop to collect all hits
        pts = []

        for start in my_start_points:
            current_ray = Ray(
                Point(start),
                rayDirection=Z_AXIS_DIRECTION,
                wavelength=wl,
                color=name,
                dc=False,
                parentCanvas=None
            )

            ray_failed = False

            # Trace through all mirrors sequentially
            for i, surface in enumerate(mirrors):
                reflected = surface.calculate_ReflectedRay(current_ray)

                # FIX 4: Check for missing the mirror immediately
                if reflected is None:
                    print(f"Ray {start} missed mirror {i}")
                    ray_failed = True
                    break

                p1 = current_ray.get_StartPoint()
                p2 = reflected.get_StartPoint()

                ray_vertices.append(p1)
                ray_vertices.append(p2)
                ray_colors.extend([color_rbg, color_rbg])

                current_ray = reflected

            # FIX 1: Evaluate screen hit only after the ray has traversed all mirrors
            if not ray_failed:
                hit, hit_color = screen.stop_ray_on_screen(current_ray)
                if hit is not None:
                    pts.append([hit[0], hit[1]])

                    # 2. ADD THIS: Draw the final segment from the last mirror to the screen
                    last_mirror_point = current_ray.get_StartPoint()

                    # Add the start point (last mirror) and end point (screen hit)
                    ray_vertices.append(last_mirror_point)
                    ray_vertices.append(hit)  # 'hit' should contain the (x, y, z) intersection point

                    # Add the colors for this final segment
                    ray_colors.extend([color_rbg, color_rbg])

        # Store spot diagram data for this wavelength
        spot_data[name] = np.array(pts, dtype=float) if len(pts) > 0 else np.empty((0, 2), dtype=float)

    # FIX 3: Initialize the plot once after all wavelengths are processed
    spot_plot = SpotDiagramPlot(
        spot_data,
        wavelengths=wavelengths,
        sizes=(600, 600)
    )

    if len(ray_vertices) > 0:
        batched_rays = scene.visuals.Line(
            pos=np.array(ray_vertices, dtype=np.float32),
            color=np.array(ray_colors, dtype=np.float32),
            connect='segments',
            parent=canvas.view.scene
        )

    canvas.show()
    spot_plot.show()

if __name__ == "__main__":
    test_mirror()






