import numpy as np
from opticsLAB.raytracing.component import Z_AXIS_DIRECTION

class OpticalSystem:
    """
    Sequential optical system made of ordered refracting elements.
    Works with your existing Lens / SphericalLens / ParabolicLens classes.
    """

    def __init__(self, elements):
        self.elements = list(elements)

    def trace_ray(self, ray):
        current_ray = ray
        for element in self.elements:
            current_ray = element.calculate_RefractedRay(current_ray)
            if current_ray is None:
                return None
        return current_ray

    @staticmethod
    def intersect_ray_with_z_plane(ray, z_plane):
        p = np.array(ray.get_StartPoint(), dtype=float)
        d = np.array(ray.get_Direction(), dtype=float)

        if abs(d[2]) < 1e-12:
            return None

        t = (z_plane - p[2]) / d[2]
        if t < 0:
            return None

        return p + t * d

    @staticmethod
    def generate_pupil_points(pupil_radius, n_rings=5):
        pts = [(0.0, 0.0)]
        for k in range(1, n_rings + 1):
            r = pupil_radius * k / n_rings
            n_theta = max(6, 6 * k)
            for j in range(n_theta):
                th = 2.0 * np.pi * j / n_theta
                x = r * np.cos(th)
                y = r * np.sin(th)
                pts.append((x, y))
        return pts

    @staticmethod
    def rms_spot_radius(points):
        if len(points) == 0:
            return np.nan

        centroid = np.mean(points, axis=0)
        dr2 = np.sum((points - centroid) ** 2, axis=1)
        return np.sqrt(np.mean(dr2))

    def compute_spot_diagram(self, Ray, Point, wavelengths, z_image,
                             pupil_radius, z_start=-2.0,
                             direction=(0.0, 0.0, 1.0),
                             canvas=None, dc=False, n_rings=6, custom_points=None):
        spot_data = {}
        # pupil_points = self.generate_pupil_points(pupil_radius, n_rings=n_rings)
        # direction = np.array(direction, dtype=float)
        # direction = direction / np.linalg.norm(direction)
        # Use custom points if provided, otherwise generate the circular grid
        if custom_points is not None:
            pupil_points = custom_points
        else:
            pupil_points = self.generate_pupil_points(pupil_radius, n_rings=n_rings)

        direction = np.array(direction, dtype=float)
        direction = direction / np.linalg.norm(direction)

        for name, wl in wavelengths.items():
            hits = []

            for x0, y0 in pupil_points:
                start = np.array([x0, y0, z_start], dtype=float)

                ray = Ray(
                    Point(start),
                    rayDirection=Z_AXIS_DIRECTION,
                    wavelength=wl,
                    color=name,
                    dc=False,
                    parentCanvas=canvas
                )

                out_ray = self.trace_ray(ray)
                if out_ray is None:
                    continue

                hit = self.intersect_ray_with_z_plane(out_ray, z_image)
                if hit is not None:
                    hits.append(hit[:2])

            if hits:
                spot_data[name] = np.array(hits, dtype=float)
            else:
                spot_data[name] = np.empty((0, 2), dtype=float)

        return spot_data

    def find_best_focus(self, Ray, Point, wavelength, z_min, z_max, n_steps,
                        pupil_radius, z_start=-2.0,
                        direction=(0.0, 0.0, 1.0),
                        canvas=None, dc=False, n_rings=6):
        trial_planes = np.linspace(z_min, z_max, n_steps)
        best_z = None
        best_rms = np.inf

        for z_img in trial_planes:
            data = self.compute_spot_diagram(
                Ray=Ray,
                Point=Point,
                wavelengths={"test": wavelength},
                z_image=z_img,
                pupil_radius=pupil_radius,
                z_start=z_start,
                direction=Z_AXIS_DIRECTION,
                canvas=canvas,
                dc=False,
                n_rings=n_rings
            )
            rms = self.rms_spot_radius(data["test"])
            if np.isfinite(rms) and rms < best_rms:
                best_rms = rms
                best_z = z_img

        return best_z, best_rms

