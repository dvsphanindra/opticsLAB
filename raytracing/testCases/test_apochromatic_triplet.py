from opticsLAB.raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
from opticsLAB.raytracing.component import OpticsLabCanvas
from opticsLAB.raytracing.component.opticalPrimitives.Point import Point
from vispy.color import Color
from opticsLAB.raytracing.component import Z_AXIS_DIRECTION, Z_AXIS_NEG_DIRECTION
from opticsLAB.raytracing.component.sources import Ray, CircularBeam
import numpy as np
from opticsLAB.raytracing.component.materialProperties import refractiveIndex
from opticsLAB.raytracing.spotDiagram import SpotDiagramPlot
from opticsLAB.raytracing.component.primitives.OpticalSystems import OpticalSystem
import sys
import vispy.app

canvas = OpticsLabCanvas()
# canvas1 = OpticsLabCanvas()


def test_apochromatic_triplet():
    wavelengths = {
        "blue": 0.465,
        "green": 0.530,
        "red": 0.620
    }

    aperture_radius = 1
    z = 0

    front = SphericalLens(
        R1=4.4144,
        R2=-3.9524,
        center=(0, 0, z - 0.1635),
        radius=aperture_radius,
        thickness=0.33,
        mediumBefore="Air",
        mediumAfter="fused silica",
        color=Color((0.1, 0.5, 1), alpha=0.05),
        parentCanvas=canvas
    )

    middle = SphericalLens(
        R1=15.8460,
        R2=-41.8801,
        center=(0, 0, z + 0.2667),
        radius=aperture_radius,
        thickness=0.15,
        mediumBefore="Air",
        mediumAfter="sapphire",
        color=Color((0.1, 0.5, 1), alpha=0.05),
        parentCanvas=canvas
    )

    rear = SphericalLens.plano_convex(
        R=5.4845,
        flat_surface="front",
        center=(0, 0, z + 0.4267),
        radius=aperture_radius,
        thickness=0.15,
        mediumBefore="Air",
        mediumAfter="BK7",
        color=Color((0.1, 0.5, 1), alpha=0.05),
        parentCanvas=canvas
    )

    triplet = [front, middle, rear]
    system = OpticalSystem(triplet)

    print("Testing apochromatic triplet:")
    print("=" * 60)

    ray_heights = np.linspace(-0.7, 0.7, 9)

    nominal_focal_plane = None
    mean_z = None

    for name, wl in wavelengths.items():
        print(f"\n{name.upper()} light (λ = {wl:.3f} μm):")
        print("  Refractive indices:")
        print(f"    fused silica: {refractiveIndex(wl, 'fused silica'):.4f}")
        print(f"    sapphire:     {refractiveIndex(wl, 'sapphire'):.4f}")
        print(f"    BK7:          {refractiveIndex(wl, 'BK7'):.4f}")

        focal_points = []

        for ray_height in ray_heights:
            start = (0, ray_height, -2)

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
                    print(f"  ray y={ray_height:+.3f} -> Lens {i + 1}: No intersection")
                    ray_failed = True
                    break
                current_ray = refracted

            if ray_failed:
                continue

            start_pt = np.array(current_ray.get_StartPoint(), dtype=float)
            direction = np.array(current_ray.get_Direction(), dtype=float)

            if abs(direction[1]) > 1e-6:
                t_focus = -start_pt[1] / direction[1]
                focal_z = start_pt[2] + t_focus * direction[2]
                focal_points.append((ray_height, focal_z))

                print(
                    f"  ray y={ray_height:+.3f} -> "
                    f"exit z={start_pt[2]:.4f}, "
                    f"dir={direction}, "
                    f"focus z={focal_z:.4f}"
                )
            else:
                print(
                    f"  ray y={ray_height:+.3f} -> "
                    f"exit z={start_pt[2]:.4f}, dir={direction}, no axis crossing"
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

    print("\n" + "=" * 60)

    z_image_plane = nominal_focal_plane if nominal_focal_plane is not None else mean_z

    # 36 custom rays = 9 points on each of 4 pupil lines
    ray_line = np.linspace(-0.7, 0.7, 9)

    vertical_rays = [(0.0, float(t)) for t in ray_line]  # x = 0
    horizontal_rays = [(float(t), 0.0) for t in ray_line]  # y = 0
    diag45_rays = [(float(t), float(t)) for t in ray_line]  # y = x
    diag135_rays = [(float(t), -float(t)) for t in ray_line]  # y = -x

    my_custom_rays = vertical_rays + horizontal_rays + diag45_rays + diag135_rays

    print("Custom ray start points:")
    for p in my_custom_rays:
        print(p)
    print(f"Total custom rays = {len(my_custom_rays)}")

    spot_data = system.compute_spot_diagram(
        Ray=Ray,
        Point=Point,
        wavelengths=wavelengths,
        z_image=z_image_plane,
        pupil_radius=0.7,
        z_start=-2.0,
        direction=Z_AXIS_DIRECTION,
        canvas=canvas,
        dc=False,
        custom_points=my_custom_rays
    )

    for name, pts in spot_data.items():
        rms = system.rms_spot_radius(pts)
        print(f"{name}: {len(pts)} rays, RMS spot radius = {rms:.6f}")

    spot_plot = SpotDiagramPlot(
        spot_data,
        wavelengths=wavelengths,
        sizes=(600, 600)
    )

    spot_plot.show()
    canvas.show()

    if sys.flags.interactive == 0:
        vispy.app.run()


if __name__ == "__main__":
    test_apochromatic_triplet()
