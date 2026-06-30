import numpy as np
from matplotlib.pyplot import connect

from opticsLAB.raytracing.component.primitives.conicSurface import ConicSurface
from opticsLAB.raytracing.component.sources import Ray, Beam, CircularBeam
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

    primary = ConicSurface(radius=206.0,RoC=-3338.827,K=-1.157,
                           centerHoleRadius=76.0, center=x1,
                           mediumAfter='Air',mediumBefore='Air',
                           color=Color((0,0.1,0.9),alpha=0.5),
                           parentCanvas=canvas)

    x2 = Point((0, 0, -1084))

    secondary = ConicSurface(radius=80.0,RoC=-1901.093,K=-6.975, center=x2,
                           mediumAfter='Air',mediumBefore='Air',
                           color=Color((0,0.5,0.9),alpha=0.5),
                           parentCanvas=canvas)

    screen_position = Point((0, 0, 440))

    screen = RectangularScreen(screen_position,
                               width=20,
                               height=20,
                               color=Color('green', alpha=0.5),
                               parent=canvas
                               )

    return [primary, secondary], screen

def generate_aperture_rays(radius, inner_radius=80.0, z0=-1500.0, n_rays=100):
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


def generate_uniform_circular_beam(radius, z0=-1500.0, n_rays=None):
    pts = []

    # Golden ratio spacing for highly uniform spiral distribution
    golden_angle = np.pi * (3.0 - np.sqrt(5.0))

    for i in range(n_rays):
        # Evenly space out the area of the circle
        r = radius * np.sqrt(i / (n_rays - 1)) if n_rays > 1 else 0
        theta = i * golden_angle

        x = r * np.cos(theta)
        y = r * np.sin(theta)
        pts.append((x, y, z0))

    return pts


def generate_concentric_circular_beam(radius, z0=-1500.0, n_rings=5, pts_per_ring=20):
    pts = []

    # 1. Always include the exact center point (r = 0)
    pts.append((0.0, 0.0, z0))

    # 2. Generate points for each concentric ring
    # We use np.linspace to space the radii linearly up to the maximum radius
    radii = np.linspace(0, radius, n_rings + 1)[1:]  # Exclude 0 since we handled center

    for r in radii:
        for i in range(pts_per_ring):
            # Evenly space angles from 0 to 2*pi
            theta = (2 * np.pi * i) / pts_per_ring

            x = r * np.cos(theta)
            y = r * np.sin(theta)
            pts.append((x, y, z0))

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
    ray_vertices1  = []
    ray_colors1 = []
    spot_data = {}

    for name, wl in wavelengths.items():
        color_rbg = color_map.get(name, [1.0, 1.0, 1.0, 0.7])

        primary_aperture_radius = 206
        # my_start_points = generate_uniform_circular_beam(
        #     radius=primary_aperture_radius,
        #     z0=-1500.0,
        #     n_rays=1000
        # )

        my_start_points = generate_concentric_circular_beam(radius=primary_aperture_radius, n_rings=5, pts_per_ring=20)



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

        # point1 = Point((0.1,0,0))
        #
        # r1 = Ray(point1,rayDirection=Z_AXIS_DIRECTION,parentCanvas=canvas)
        # r1.rotate_aboutX(30)
        # # r1.rotate_aboutY(30)
        beam = CircularBeam(center = Point(0,0,-1500),
                            radius=180, noOfRays=100,
                             color="green", centerRay=False,
                             # Color((1.0,0.2,0.5),alpha=1.0),
                             parentCanvas=None)
        beam.rotate_aboutX(-0.125)

        # temp_beam = CircularBeam(center=Point(0, 0, -1500),
        #                      radius=180, noOfRays=100,
        #                      color="red", centerRay=False,
        #                      # Color((1.0,0.2,0.5),alpha=1.0),
        #                      parentCanvas=None)
        # temp_beam.rotate_aboutX(-0.125)
        # beam.add_Beam(temp_beam)
        #
        # temp_beam = CircularBeam(center=Point(0, 0, -1500),
        #                          radius=180, noOfRays=100,
        #                          color="blue", centerRay=False,
        #                          # Color((1.0,0.2,0.5),alpha=1.0),
        #                          parentCanvas=None)
        # temp_beam.rotate_aboutX(-0.250)
        # beam.add_Beam(temp_beam)


        # for start in my_start_points:
        #     current_ray = Ray(
        #         Point(start),
        #         rayDirection=Z_AXIS_DIRECTION,
        #         wavelength=wl,
        #         color=name,
        #         dc=False,
        #         parentCanvas=None
        #     )
        #     current_ray.rotate_aboutX(0.177)


        #current_ray.set_y_angle(60)

        #print("directon =", current_ray.direction)


        # Trace through all mirrors sequentially
        for current_ray in beam.get_Rays():
            ray_failed = False
            for i, surface in enumerate(mirrors):
                # print(current_ray.get_StartPoint())
                reflected = surface.calculate_ReflectedRay(current_ray)
                # print("reflected= ", reflected)

                # FIX 4: Check for missing the mirror immediately
                if reflected is None:
                    # print(f"Ray {current_ray.get_StartPoint()} missed mirror {i}")
                    ray_failed = True
                    break

                p1 = current_ray.get_StartPoint()
                p2 = reflected.get_StartPoint()


                ray_vertices.append(p1)
                ray_vertices.append(p2)
                ray_colors.append(Color(current_ray.get_Color()).rgba)
                ray_colors.append(Color(current_ray.get_Color()).rgba)

                current_ray = reflected
                # print("current ray = ", current_ray.get_StartPoint(), ray_failed)

                # FIX 1: Evaluate screen hit only after the ray has traversed all mirrors
                if not ray_failed:
                    hit = screen.stop_ray_on_screen(current_ray)
                    # hit_color = current_ray.get_Color()
                    if hit is not None:
                        pts.append([hit[0], hit[1]])

                        # 2. ADD THIS: Draw the final segment from the last mirror to the screen
                        last_mirror_point = current_ray.get_StartPoint()

                        # Add the start point (last mirror) and end point (screen hit)
                        ray_vertices.append(last_mirror_point)
                        ray_vertices.append(hit)  # 'hit' should contain the (x, y, z) intersection point

                        # Add the colors for this final segment
                        ray_colors.append(Color(current_ray.get_Color()).rgba)
                        ray_colors.append(Color(current_ray.get_Color()).rgba)

        # Store spot diagram data for this wavelength
        spot_data[name] = np.array(pts, dtype=float) if len(pts) > 0 else np.empty((0, 2), dtype=float) #* 48.154

# FIX 3: Initialize the plot once after all wavelengths are processed
    spot_plot = SpotDiagramPlot(
        spot_data,
        wavelengths=wavelengths,
        sizes=(600, 600)
    )
    print(ray_vertices)

    if len(ray_vertices) > 0:
        batched_rays = scene.visuals.Line(
            pos=np.array(ray_vertices, dtype=np.float32),
            color=np.array(ray_colors),
            connect='segments',
            parent=canvas.view.scene
        )

    canvas.show()
    spot_plot.show()

if __name__ == "__main__":
    test_mirror()






