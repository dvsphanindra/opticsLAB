from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
from opticsLAB.raytracing.component import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from opticsLAB.raytracing.component import Z_AXIS_DIRECTION, Z_AXIS_DC
from opticsLAB.raytracing.component.sources import Ray
from opticsLAB.raytracing.component.materialProperties import refractiveIndex
from opticsLAB.raytracing.spotDiagram import SpotDiagramPlot
from opticsLAB.raytracing.component.primitives.OpticalSystems import OpticalSystem
from opticsLAB.raytracing.component.detectors import RectangularScreen
from opticsLAB.raytracing.component.primitives.miscellaneous import *

from vispy.color import Color
import vispy.app
import numpy as np
import sys
import matplotlib.pyplot as plt

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

def trace_ray_through_triplet(ray, triplet):
    current_ray = ray
    for lens in triplet:
        current_ray = lens.calculate_RefractedRay(current_ray)
        if current_ray is None:
            return None
    return current_ray


def compute_ray_fan_screen(triplet, wavelength, z_image, field_angle_deg=0.0,
                           fan_type="axial", n_rays=15, pupil_radius=10.0):
    pupil = np.linspace(-pupil_radius, pupil_radius, n_rays)

    if fan_type == "axial":
        direction = dc_from_points((0, 0, -20), (0, 0, 0))
        starts = [(0.0, y, -20.0) for y in pupil]
        ref_coord = pupil / pupil_radius
        coord_label = "y"

    elif fan_type == "tangential":
        target_y = np.tan(np.deg2rad(field_angle_deg)) * 100.0
        direction = dc_from_points((0, 0, -20), (0, target_y, 100.0))
        starts = [(0.0, y, -20.0) for y in pupil]
        ref_coord = pupil / pupil_radius
        coord_label = "y"

    elif fan_type == "sagittal":
        target_x = np.tan(np.deg2rad(field_angle_deg)) * 100.0
        direction = dc_from_points((0, 0, -20), (target_x, 0.0, 100.0))
        starts = [(x, 0.0, -20.0) for x in pupil]
        ref_coord = pupil / pupil_radius
        coord_label = "x"

    else:
        raise ValueError("fan_type must be axial, tangential, or sagittal")

    screen = RectangularScreen(
        Point(0.0, 0.0, z_image),
        color=Color('white', alpha=0.0),
        parent=None
    )

    chief_ray = Ray(
        Point((0.0, 0.0, -20.0)),
        rayDirection=direction,
        wavelength=wavelength,
        color="white",
        dc=True,
        parentCanvas=None
    )

    chief_out = chief_ray
    for lens in triplet:
        chief_out = lens.calculate_RefractedRay(chief_out)
        if chief_out is None:
            return np.array([]), np.array([]), coord_label

    chief_hit, _ = screen.calculate_RayIntersection(chief_out)
    if chief_hit is None:
        return np.array([]), np.array([]), coord_label

    coords = []
    aberr = []

    for s, u in zip(starts, ref_coord):
        ray = Ray(
            Point(s),
            rayDirection=direction,
            wavelength=wavelength,
            color="white",
            dc=True,
            parentCanvas=None
        )

        out_ray = ray
        failed = False
        for lens in triplet:
            out_ray = lens.calculate_RefractedRay(out_ray)
            if out_ray is None:
                failed = True
                break

        if failed:
            continue

        hit, _ = screen.calculate_RayIntersection(out_ray)
        if hit is None:
            continue

        coords.append(u)

        if fan_type in ["axial", "tangential"]:
            aberr.append(hit[1] - chief_hit[1])
        else:
            aberr.append(hit[0] - chief_hit[0])

    return np.array(coords), np.array(aberr), coord_label

def plot_aberration_fans_single_frame(triplet, z_image):
    wavelengths_plot = {
        "C": 0.6563,
        "d": 0.5876,
        "F": 0.4861
    }

    styles = {
        "C": (0, (4, 3)),
        "d": "solid",
        "F": (0, (8, 3))
    }

    panels = [
        ("axial",      "Axial",       0.0),
        ("tangential", "Tangential", 15.0),
        ("sagittal",   "Sagittal",   15.0)
    ]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), sharey=True)

    for ax, (fan_type, title, field_deg) in zip(axes, panels):
        for label, wl in wavelengths_plot.items():
            x, y, coord_label = compute_ray_fan_screen(
                triplet=triplet,
                wavelength=wl,
                z_image=z_image,
                fan_type=fan_type,
                field_angle_deg=field_deg,
                n_rays=15,
                pupil_radius=10.0
            )

            if len(x) == 0:
                continue

            ax.plot(
                x, y,
                color="black",
                linestyle=styles[label],
                linewidth=1.2,
                label=label
            )

        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_title(title, fontsize=12)
        ax.set_xlabel(f"Normalized pupil {coord_label}")
        ax.set_xlim(-1.05, 1.05)
        ax.grid(False)

    axes[0].set_ylabel("Transverse aberration (mm)")
    axes[1].legend(frameon=False, loc="lower left")

    fig.tight_layout()
    fig.canvas.manager.set_window_title("Axial + Tangential + Sagittal Fans")
    return fig

# def paraxial_cardinal_points():
#     eff_focal_length = 100.0
#     f_number = 3.5
#     aperture_diameter = eff_focal_length / f_number
#     back_focal_length = 75.98
#     field_angle_deg = 15.0
#     image_height = eff_focal_length * np.tan(np.deg2rad(field_angle_deg))
#
#     print("\nCooke triplet first-order parameters:")
#     print(f"  Aperture diameter = {aperture_diameter:.2f} mm")
#     print(f"  Effective focal length = {eff_focal_length:.2f} mm")
#     print(f"  Back focal length = {back_focal_length:.2f} mm")
#     print(f"  Object distance = infinity")
#     print(f"  Image height at {field_angle_deg:.1f}° = {image_height:.2f} mm")
#
#     return {
#         "aperture_diameter": aperture_diameter,
#         "eff_focal_length": eff_focal_length,
#         "back_focal_length": back_focal_length,
#         "field_angle_deg": field_angle_deg,
#         "image_height": image_height
#     }
#
#
# def compute_ray_fan(triplet, wavelength, z_image, field_angle_deg=0.0,
#                     fan_type="axial", n_rays=21, pupil_radius=10.0):
#     pupil = np.linspace(-pupil_radius, pupil_radius, n_rays)
#
#     if fan_type == "axial":
#         direction = Z_AXIS_DC
#         starts = [(0.0, y, -20.0) for y in pupil]
#         ref_coord = pupil / pupil_radius
#         coord_label = "y"
#     elif fan_type == "tangential":
#         direction = dc_from_field_y(field_angle_deg)
#         starts = [(0.0, y, -20.0) for y in pupil]
#         ref_coord = pupil / pupil_radius
#         coord_label = "y"
#     elif fan_type == "sagittal":
#         direction = dc_from_field_x(field_angle_deg)
#         starts = [(x, 0.0, -20.0) for x in pupil]
#         ref_coord = pupil / pupil_radius
#         coord_label = "x"
#     else:
#         raise ValueError("fan_type must be axial, tangential, or sagittal")
#
#     chief_start = (0.0, 0.0, -20.0)
#     chief_ray = Ray(
#         Point(chief_start),
#         rayDirection=direction,
#         wavelength=wavelength,
#         color="white",
#         dc=True,
#         parentCanvas=None
#     )
#     chief_out = trace_ray_through_triplet(chief_ray, triplet)
#     chief_hit = intersect_with_z_plane(chief_out, z_image) if chief_out is not None else None
#
#     coords = []
#     aberr = []
#
#     for s, u in zip(starts, ref_coord):
#         ray = Ray(
#             Point(s),
#             rayDirection=direction,
#             wavelength=wavelength,
#             color="white",
#             dc=True,
#             parentCanvas=None
#         )
#         out_ray = trace_ray_through_triplet(ray, triplet)
#         if out_ray is None:
#             continue
#
#         hit = intersect_with_z_plane(out_ray, z_image)
#         if hit is None or chief_hit is None:
#             continue
#
#         coords.append(u)
#
#         if fan_type in ["axial", "tangential"]:
#             aberr.append(hit[1] - chief_hit[1])
#         else:
#             aberr.append(hit[0] - chief_hit[0])
#
#     return np.array(coords), np.array(aberr), coord_label
#
#
# def plot_aberration_fans(triplet, z_image):
#     wavelengths_plot = {
#         "C": 0.6563,
#         "d": 0.5876,
#         "F": 0.4861
#     }
#
#     styles = {
#         "C": (0, (4, 3)),
#         "d": "solid",
#         "F": (0, (8, 3))
#     }
#
#     fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), sharey=True)
#
#     panels = [
#         ("axial", 0.0, "Axial plot"),
#         ("tangential", 15.0, "Tangential plot 15°"),
#         ("sagittal", 15.0, "Sagittal plot 15°")
#     ]
#
#     for ax, (fan_type, field_deg, title) in zip(axes, panels):
#         for label, wl in wavelengths_plot.items():
#             x, y, coord_label = compute_ray_fan(
#                 triplet=triplet,
#                 wavelength=wl,
#                 z_image=z_image,
#                 field_angle_deg=field_deg,
#                 fan_type=fan_type,
#                 n_rays=21,
#                 pupil_radius=10.0
#             )
#             ax.plot(x, y, color="black", linestyle=styles[label], linewidth=1.2, label=label)
#
#         ax.axhline(0, color="black", linewidth=0.8)
#         ax.axvline(0, color="black", linewidth=0.8)
#         ax.set_title(title, fontsize=12)
#         ax.set_xlabel(coord_label)
#         ax.set_xlim(-1.05, 1.05)
#         ax.grid(False)
#
#     axes[0].set_ylabel("Transverse aberration (mm)")
#     axes[1].legend(frameon=False, loc="lower left")
#     fig.tight_layout()
#     fig.canvas.manager.set_window_title("Aberration Fans")
#     return fig

# def compute_ray_fan_screen(triplet, wavelength, z_image, field_angle_deg=0.0,
#                            fan_type="axial", n_rays=21, pupil_radius=10.0):
#     pupil = np.linspace(-pupil_radius, pupil_radius, n_rays)
#
#     if fan_type == "axial":
#         direction = Z_AXIS_DC
#         starts = [(0.0, y, -20.0) for y in pupil]
#         ref_coord = pupil / pupil_radius
#         coord_label = "y"
#         chief_start = (0.0, 0.0, -20.0)
#     elif fan_type == "tangential":
#         direction = dc_from_field_y(field_angle_deg)
#         starts = [(0.0, y, -20.0) for y in pupil]
#         ref_coord = pupil / pupil_radius
#         coord_label = "y"
#         chief_start = (0.0, 0.0, -20.0)
#     elif fan_type == "sagittal":
#         direction = dc_from_field_x(field_angle_deg)
#         starts = [(x, 0.0, -20.0) for x in pupil]
#         ref_coord = pupil / pupil_radius
#         coord_label = "x"
#         chief_start = (0.0, 0.0, -20.0)
#     else:
#         raise ValueError("fan_type must be axial, tangential, or sagittal")
#
#     screen = RectangularScreen(
#         Point(0.0, 0.0, z_image),
#         color=Color('white', alpha=0.0),
#         parent=None
#     )
#
#     chief_ray = Ray(
#         Point(chief_start),
#         rayDirection=direction,
#         wavelength=wavelength,
#         color="white",
#         dc=True,
#         parentCanvas=None
#     )
#
#     chief_out = trace_ray_through_triplet(chief_ray, triplet)
#     if chief_out is None:
#         return np.array([]), np.array([]), coord_label
#
#     chief_hit, _ = screen.calculate_RayIntersection(chief_out)
#     if chief_hit is None:
#         return np.array([]), np.array([]), coord_label
#
#     coords = []
#     aberr = []
#
#     for s, u in zip(starts, ref_coord):
#         ray = Ray(
#             Point(s),
#             rayDirection=direction,
#             wavelength=wavelength,
#             color="white",
#             dc=True,
#             parentCanvas=None
#         )
#
#         out_ray = trace_ray_through_triplet(ray, triplet)
#         if out_ray is None:
#             continue
#
#         hit, _ = screen.calculate_RayIntersection(out_ray)
#         if hit is None:
#             continue
#
#         coords.append(u)
#
#         if fan_type in ["axial", "tangential"]:
#             aberr.append(hit[1] - chief_hit[1])
#         else:
#             aberr.append(hit[0] - chief_hit[0])
#
#     return np.array(coords), np.array(aberr), coord_label


canvas = OpticsLabCanvas()


def build_cooke_triplet(canvas, z0=0.0):
    aperture_radius = 20.0
    stop_radius = 20.7 / 2.0

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

    front = SphericalLens(
        R1=34.94,
        R2=-1164.00,
        center=(0, 0, z1_center),
        radius=aperture_radius,
        thickness=t1,
        mediumBefore="Air",
        mediumAfter="N-SK4",
        color=Color((0.3, 0.6, 1.0), alpha=0.15),
        parentCanvas=canvas
    )

    middle = SphericalLens(
        R1=-60.369,
        R2=30.68,
        center=(0, 0, z2_center),
        radius=10.35,
        thickness=t2,
        mediumBefore="Air",
        mediumAfter="N-SF2",
        color=Color((1.0, 0.5, 0.2), alpha=0.15),
        parentCanvas=canvas
    )

    rear = SphericalLens(
        R1=91.77,
        R2=-49.08,
        center=(0, 0, z3_center),
        radius=aperture_radius,
        thickness=t3,
        mediumBefore="Air",
        mediumAfter="N-SK4",
        color=Color((0.3, 1.0, 0.5), alpha=0.15),
        parentCanvas=canvas
    )

    #z_image_plane = 100



    system = OpticalSystem([front, middle, rear])

    info = {
        "front": front,
        "middle": middle,
        "rear": rear,
        "triplet": [front, middle, rear],
        "stop_radius": stop_radius,
        "image_plane_z": z3_front + t3 + 75.98
    }

    return system, info


def test_cooke_triplet():
    wavelengths = {
        "blue": 0.465,
        "green": 0.530,
        "red": 0.620
    }

    system, info = build_cooke_triplet(canvas)
    triplet = info["triplet"]

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

    #ray_heights = np.linspace(-5.0, 5.0, 5)
    nominal_focal_plane = None
    mean_z = None

    for name, wl in wavelengths.items():
        print(f"\n{name.upper()} light (λ = {wl:.3f} μm):")
        print("  Refractive indices:")
        print(f"    N-SK4: {refractiveIndex(wl, 'N-SK4'):.6f}")
        print(f"    N-SF2: {refractiveIndex(wl, 'N-SF2'):.6f}")

        focal_points = []

        my_start_points = [(0.0, 0.0, -20.0),
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


        for start in my_start_points:
            current_ray = Ray(
                Point(start),
                rayDirection=Z_AXIS_DIRECTION,
                wavelength=wl,
                color=name,
                dc=False,
                parentCanvas=canvas
            )

            ray_failed = False

            for i, lens in enumerate(triplet):
                refracted = lens.calculate_RefractedRay(current_ray)
                if refracted is None:
                    print(f"  ray start={start} -> Lens {i + 1}: No intersection")
                    ray_failed = True
                    break
                current_ray = refracted

            if ray_failed:
                continue

            start_pt = np.array(current_ray.get_StartPoint(), dtype=float)
            direction = np.array(current_ray.get_Direction(), dtype=float)

            if abs(direction[1]) > 1e-9:
                t_focus = -start_pt[1] / direction[1]
                focal_z = start_pt[2] + t_focus * direction[2]
                focal_points.append((start, focal_z))

                print(
                    f"  ray start={start} -> "
                    f"exit z={start_pt[2]:.4f}, "
                    f"dir={direction}, "
                    f"focus z={focal_z:.4f}"
                )
            else:
                print(
                    f"  ray start={start} -> "
                    f"exit z={start_pt[2]:.4f}, dir={direction}, no y-axis crossing"
                )

        if focal_points:
            zvals = [fz for _, fz in focal_points]
            mean_z = np.mean(zvals)
            print(f"  Mean focus z = {mean_z:.4f}")
            print(f"  Focus spread = {max(zvals) - min(zvals):.6f}")

            if name == "green":
                nominal_focal_plane = mean_z
        else:
            print("  No valid focused rays for this wavelength.")

    #print("\n" + "=" * 60)
    z_image_plane = nominal_focal_plane if nominal_focal_plane is not None else mean_z #79.9405#

    screen = RectangularScreen(
        Point(0.0, 0.0, z_image_plane),
        color=Color('green', alpha=0.5),
        parent=canvas
    )

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

    spot_data = {}

    for name, wl in wavelengths.items():
        pts = []

        for start in my_start_points:
            ray = Ray(
                Point(start),
                rayDirection=Z_AXIS_DIRECTION,
                wavelength=wl,
                color=name,
                dc=False,
                parentCanvas=None
            )

            current_ray = ray
            failed = False

            for lens in triplet:
                current_ray = lens.calculate_RefractedRay(current_ray)
                if current_ray is None:
                    failed = True
                    break

            if failed:
                continue

            hit, hit_color = screen.stop_ray_on_screen(current_ray)#screen.calculate_RayIntersection(current_ray)
            if hit is None:
                continue

            pts.append([hit[0], hit[1]])

        spot_data[name] = np.array(pts, dtype=float) if len(pts) > 0 else np.empty((0, 2), dtype=float)
    spot_plot = SpotDiagramPlot(
                spot_data,
                wavelengths=wavelengths,
                sizes=(600, 600)
            )

    print("\nUsing z_image_plane for aberration fans:", z_image_plane)

    #fig = plot_aberration_fans_single_frame(triplet, z_image_plane)


    canvas.show()
    # print('started_rendering')
    # img = canvas.render()
    # import imageio
    # imageio.imwrite("/Volumes/ExtremeSSD/JAYANTH-Ubuntubackup/Documents/Research/Kavalur/16inch/python_projects/opticsLAB/gallery/cooke_triplet_lens.png", img)
    # print('finished_rendering, image saved')

    spot_plot.show()

    # plt.show(block=False)
    # plt.pause(0.1)

    if sys.flags.interactive == 0:
        vispy.app.run()


if __name__ == "__main__":
    test_cooke_triplet()