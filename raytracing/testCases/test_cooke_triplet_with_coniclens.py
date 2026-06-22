from opticsLAB.raytracing.component.opticalPrimitives.conicLens import ConicLens
from opticsLAB.raytracing.component import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from opticsLAB.raytracing.component import Z_AXIS_DIRECTION, Z_AXIS_DC
from opticsLAB.raytracing.component.sources import Ray
from opticsLAB.raytracing.component.materialProperties import refractiveIndex
from opticsLAB.raytracing.component.detectors import RectangularScreen

from vispy.color import Color
import vispy.app
import numpy as np
import sys

def calculate_first_order_properties(triplet, entrance_radius=10.0, field_angle_deg=15.0,
                                     wavelength=0.5876, z_start=-20.0):
    import numpy as np

    def trace(ray):
        current = ray
        for lens in triplet:
            current = lens.calculate_RefractedRay(current)
            if current is None:
                return None
        return current

    # Paraxial marginal ray from object at infinity
    marginal_ray = Ray(
        Point((0.0, entrance_radius, z_start)),
        rayDirection=Z_AXIS_DC,
        wavelength=wavelength,
        color="white",
        dc=True,
        parentCanvas=None
    )

    marginal_out = trace(marginal_ray)
    if marginal_out is None:
        raise RuntimeError("Marginal ray failed during trace.")

    p_m = np.array(marginal_out.get_StartPoint(), dtype=float)
    d_m = np.array(marginal_out.get_Direction(), dtype=float)

    if abs(d_m[1]) < 1e-12:
        raise RuntimeError("Marginal ray has zero image-space slope.")

    y1 = entrance_radius
    y_last = p_m[1]
    u_img = d_m[1] / d_m[2]

    effective_focal_length = -y1 / u_img
    back_focal_length = -y_last / u_img

    aperture_diameter = 2.0 * entrance_radius
    f_number = effective_focal_length / aperture_diameter

    # Chief ray for field angle
    th = np.deg2rad(field_angle_deg)
    chief_dir = np.array((0.0, np.sin(th), np.cos(th)), dtype=float)
    chief_dir /= np.linalg.norm(chief_dir)

    chief_ray = Ray(
        Point((0.0, 0.0, z_start)),
        rayDirection=chief_dir,
        wavelength=wavelength,
        color="white",
        dc=True,
        parentCanvas=None
    )

    chief_out = trace(chief_ray)
    if chief_out is None:
        raise RuntimeError("Chief ray failed during trace.")

    p_c = np.array(chief_out.get_StartPoint(), dtype=float)
    d_c = np.array(chief_out.get_Direction(), dtype=float)

    if abs(d_c[2]) < 1e-12:
        raise RuntimeError("Chief ray has invalid z-direction.")

    # Use paraxial image plane estimated from back focal length
    z_last_surface = p_m[2]
    z_image = z_last_surface + back_focal_length

    t = (z_image - p_c[2]) / d_c[2]
    chief_hit = p_c + t * d_c
    image_height = chief_hit[1]

    return {
        "aperture_diameter": aperture_diameter,
        "effective_focal_length": effective_focal_length,
        "back_focal_length": back_focal_length,
        "f_number": f_number,
        "field_angle_deg": field_angle_deg,
        "image_height": image_height,
        "z_image": z_image
    }


def build_cooke_triplet(canvas, z0=0.0):
    aperture_radius = 20.0

    t1 = 9.0
    air1 = 10.0
    t2 = 3.0
    air2 = 13.0
    t3 = 10.0

    z1_center = z0 + t1 / 2.0
    z2_front = z0 + t1 + air1
    z2_center = z2_front + t2 / 2.0
    z3_front = z2_front + t2 + air2
    z3_center = z3_front + t3 / 2.0

    # Front Lens
    front = ConicLens(
        R_front=34.94, K_front=0.0,
        R_back=-1164.00, K_back=0.0,
        center=(0, 0, z1_center),
        radius=aperture_radius,
        thickness=t1,
        mediumBefore="Air",
        mediumAfter="N-SK4",
        color=Color((0.3, 0.6, 1.0), alpha=0.15),
        parentCanvas=canvas
    )

    # Middle Lens
    middle = ConicLens(
        R_front=-60.369, K_front=0.0,
        R_back=30.68, K_back=0.0,
        center=(0, 0, z2_center),
        radius=10.35,
        thickness=t2,
        mediumBefore="Air",
        mediumAfter="N-SF2",
        color=Color((1.0, 0.5, 0.2), alpha=0.15),
        parentCanvas=canvas
    )

    # Rear Lens
    rear = ConicLens(
        R_front=91.77, K_front=0.0,
        R_back=-49.08, K_back=0.0,
        center=(0, 0, z3_center),
        radius=aperture_radius,
        thickness=t3,
        mediumBefore="Air",
        mediumAfter="N-SK4",
        color=Color((0.3, 1.0, 0.5), alpha=0.15),
        parentCanvas=canvas
    )

    return [front, middle, rear]


def test_cooke_triplet():
    canvas = OpticsLabCanvas()
    triplet = build_cooke_triplet(canvas)

    wavelengths = {
        "blue": 0.465,
        "green": 0.530,
        "red": 0.620
    }

    my_start_points = [
        (0.0, 0.0, -20.0),
        (0.0, 5.0, -20.0),
        (0.0, -5.0, -20.0),
        (5.0, 0.0, -20.0),
        (-5.0, 0.0, -20.0),
        (0.0, 7.0, -20.0),
        (0.0, -7.0, -20.0),
        (7.0, 0.0, -20.0),
        (-7.0, 0.0, -20.0),
        (-5.0, 7.0, -20.0),
        (5.0, -7.0, -20.0),
        (7.0, -5.0, -20.0),
        (-7.0, 5.0, -20.0),
        (-5.0, -7.0, -20.0),
        (5.0, 7.0, -20.0),
        (7.0, 5.0, -20.0),
        (-7.0, -5.0, -20.0),
    ]

    print("Testing Cooke Triplet Raytracing (Using ConicLens):")
    print("==================================================")
    first_order = calculate_first_order_properties(
        triplet,
        entrance_radius=10.0,
        field_angle_deg=15.0,
        wavelength=0.5876,
        z_start=-20.0
    )

    print("\nCalculated first-order properties:")
    print(f"  Aperture diameter = {first_order['aperture_diameter']:.4f} mm")
    print(f"  Effective focal length = {first_order['effective_focal_length']:.4f} mm")
    print(f"  Back focal length = {first_order['back_focal_length']:.4f} mm")
    print(f"  F-number = {first_order['f_number']:.4f}")
    print(f"  Image height at {first_order['field_angle_deg']:.1f}° = {first_order['image_height']:.4f} mm")
    print(f"  Estimated paraxial image plane z = {first_order['z_image']:.4f} mm")

    print("Testing Cooke triplet:")
    print("=" * 60)
    # -------------------------------------------------------------
    # 1. CALCULATE FOCAL PLANE Z-COORDINATE FIRST
    # -------------------------------------------------------------
    # We trace a single invisible green test ray to mathematically find the focus
    test_ray = Ray(Point((0.0, 5.0, -20.0)), rayDirection=Z_AXIS_DIRECTION,
                   wavelength=0.530, color="green", dc=False, parentCanvas=None)
    for lens in triplet:
        test_ray = lens.calculate_RefractedRay(test_ray)

    start_pt = np.array(test_ray.get_StartPoint(), dtype=float)
    direction = np.array(test_ray.get_Direction(), dtype=float)
    t_focus = -start_pt[1] / direction[1]
    z_image_plane = start_pt[2] + t_focus * direction[2]

    print(f"Placing RectangularScreen exactly at focal plane z = {z_image_plane:.4f}\n")

    # -------------------------------------------------------------
    # 2. PLACE THE SCREEN IN THE CANVAS
    # -------------------------------------------------------------
    screen = RectangularScreen(
        center=Point(0.0, 0.0, z_image_plane),

        color=Color('green', alpha=1),
        parent=canvas
    )

    # -------------------------------------------------------------
    # 3. TRACE ALL RAYS AND MAKE THEM HIT THE SCREEN
    # -------------------------------------------------------------
    for name, wl in wavelengths.items():
        print(f"{name.upper()} light (λ = {wl:.3f} μm):")

        for start in my_start_points:
            # Create the visual ray
            current_ray = Ray(
                Point(start),
                rayDirection=Z_AXIS_DIRECTION,
                wavelength=wl,
                color=name,
                dc=False,
                parentCanvas=canvas
            )

            # Trace through the triplet
            ray_failed = False
            for i, lens in enumerate(triplet):
                refracted = lens.calculate_RefractedRay(current_ray)
                if refracted is None:
                    ray_failed = True
                    break
                current_ray = refracted

            if ray_failed:
                continue

            # -------------------------------------------------------------
            # STOP THE RAY AT THE SCREEN
            # -------------------------------------------------------------
            # Calculate where the final ray intersects the detector screen
            hit, hit_color = screen.calculate_RayIntersection(current_ray)

            if hit is not None:
                # Calculate the exact distance from the last lens exit to the screen
                last_exit_point = np.array(current_ray.get_StartPoint(), dtype=float)
                hit_distance = np.linalg.norm(np.array(hit) - last_exit_point)

                # Truncate the ray's visual length so it physically stops at the screen!
                current_ray.length = hit_distance

                # Update visual if required by opticsLAB architecture
                if hasattr(current_ray, 'update_visual'):
                    current_ray.update_visual()

                print(f"  ray start={start} -> Hits Screen at [x={hit[0]:.4f}, y={hit[1]:.4f}]")
            else:
                print(f"  ray start={start} -> Missed the screen!")

    canvas.show()
    if sys.flags.interactive == 0:
        vispy.app.run()


if __name__ == "__main__":
    test_cooke_triplet()