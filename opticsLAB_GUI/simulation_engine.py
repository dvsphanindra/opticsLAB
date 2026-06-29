"""
Simulation Engine for OpticsLAB.
Handles optical raytracing calculations directly and updates progress without using background threads.
All background threading concepts have been removed for straightforward synchronous execution.
"""
import inspect
import numpy as np
import wx

from opticsLAB_support import (
    color_to_vispy, component_z_value, is_beam_name, is_lens_name, is_light_source_name,
    is_ray_name, is_screen_name, normalize_direction_dc, normalize_material_name
)

try:
    from opticsLAB.raytracing.component.opticalPrimitives.Point import Point as OptPoint
    from opticsLAB.raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
    from opticsLAB.raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
    from opticsLAB.raytracing.component.sources import Ray as OptRay, Beam, CircularBeam as OptCircularBeam
    from opticsLAB.raytracing.component.detectors import RectangularScreen
    from opticsLAB.raytracing.component.primitives.parabolicSurface import Parabolic_Surface
    from opticsLAB.raytracing.component.opticalPrimitives.convexParaboloid import Convex_Paraboloid
    from opticsLAB.raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
    from opticsLAB.raytracing.component.primitives.sphericalSurface import Spherical_Surface
    from opticsLAB.raytracing.component.primitives.plane import Plane
except ImportError:
    from raytracing.component.opticalPrimitives.Point import Point as OptPoint
    from raytracing.component.opticalPrimitives.ParabolicLens import ParabolicLens
    from raytracing.component.opticalPrimitives.SphericalLens import SphericalLens
    from raytracing.component.sources import Ray as OptRay, Beam, CircularBeam as OptCircularBeam
    from raytracing.component.detectors import RectangularScreen
    from raytracing.component.primitives.parabolicSurface import Parabolic_Surface
    from raytracing.component.opticalPrimitives.convexParaboloid import Convex_Paraboloid
    from raytracing.component.opticalPrimitives.concaveParaboloid import Concave_Paraboloid
    from raytracing.component.primitives.sphericalSurface import Spherical_Surface
    from raytracing.component.primitives.plane import Plane


# Main engine class responsible for creating optical parts and calculating light ray paths directly
class SimulationEngine:
    def __init__(self, frame):
        self.frame = frame

    # Safely creates Python objects even if extra parameter options are passed
    def safe_instantiate(self, cls, **kwargs):
        try:
            return cls(**kwargs)
        except TypeError as err:
            if "unexpected keyword argument" in str(err).lower():
                sig = inspect.signature(cls.__init__)
                valid_args = {k: v for k, v in kwargs.items() if k in sig.parameters or (sig.parameters.get(k) and sig.parameters[k].kind == inspect.Parameter.VAR_KEYWORD)}
                return cls(**valid_args)
            raise err

    # Builds lenses, mirrors, screens, and light sources with exact user settings
    def instantiate_component(self, comp_name, name_lower, data, opt_center, radius, vis_color, canvas):
        med_before = normalize_material_name(data.get("mediumBefore", "Air"))
        med_after = normalize_material_name(data.get("mediumAfter", "BK7"))

        # Create spherical or parabolic lenses
        if is_lens_name(comp_name):
            kwargs = {"center": opt_center, "color": vis_color, "parentCanvas": canvas, "radius": radius, "thickness": data.get("thickness", 0.5), "mediumBefore": med_before, "mediumAfter": med_after}
            if "parabolic" in name_lower:
                return self.safe_instantiate(ParabolicLens, a=data.get("a", 1.0), b=data.get("b", 1.0), c_front=data.get("c_front", -1.0), c_back=data.get("c_back", 1.0), **kwargs)
            return self.safe_instantiate(SphericalLens, R1=data.get("R1", 2.0), R2=data.get("R2", -2.0), **kwargs)

        # Create single light rays
        if is_ray_name(comp_name):
            return self.safe_instantiate(OptRay, startPoint=opt_center, rayDirection=normalize_direction_dc(data.get("direction")), wavelength=data.get("wavelength", 0.55), length=data.get("length", 5.0), dc=True, color=vis_color, parentCanvas=canvas)

        # Create light beam bundles (rectangular, circular, or random beams)
        if is_beam_name(comp_name):
            if "rect" in name_lower:
                rect_len, rect_br = float(data.get("length", 1.0)), float(data.get("breath", 1.0))
                no_of_rays = int(data.get("noOfRays", 12))
                wavelength = float(data.get("wavelength", 0.55))
                beam_direction = normalize_direction_dc(data.get("direction"))
                nx = max(1, int(np.sqrt(no_of_rays)))
                ny = max(1, int(np.ceil(no_of_rays / nx)))
                xs = np.linspace(-rect_len / 2.0, rect_len / 2.0, nx)
                ys = np.linspace(-rect_br / 2.0, rect_br / 2.0, ny)
                ray_locations = []
                center_coords = opt_center.get_coordinates()
                for x_off in xs:
                    for y_off in ys:
                        if len(ray_locations) >= no_of_rays:
                            break
                        ray_locations.append(OptPoint(center_coords + np.array([x_off, y_off, 0.0])))
                return Beam(rayLocations=ray_locations, noOfRays=len(ray_locations), wavelength=wavelength, beamDirection=beam_direction, dc=True, length=5.0, color=vis_color, parentCanvas=canvas)

            elif "random" in name_lower:
                no_of_rays = int(data.get("noOfRays", 12))
                wavelength = float(data.get("wavelength", 0.55))
                beam_direction = normalize_direction_dc(data.get("direction"))
                center_coords = opt_center.get_coordinates()
                ray_locations = [OptPoint(center_coords + (np.random.rand(3) - 0.5) * 2.0) for _ in range(no_of_rays)]
                return Beam(rayLocations=ray_locations, noOfRays=len(ray_locations), wavelength=wavelength, beamDirection=beam_direction, dc=True, length=5.0, color=vis_color, parentCanvas=canvas)

            return self.safe_instantiate(OptCircularBeam, center=opt_center, radius=data.get("radius", 0.5), noOfRays=int(data.get("noOfRays", 12)), centerRay=bool(data.get("centerRay", True)), beamDirection=normalize_direction_dc(data.get("direction")), wavelength=data.get("wavelength", 0.55), length=data.get("length", 5.0), dc=True, color=vis_color, parentCanvas=canvas)

        # Create rectangular display screens
        if is_screen_name(comp_name):
            screen = self.safe_instantiate(RectangularScreen, xTilt=data.get("xTilt", 0.0), yTilt=data.get("yTilt", 0.0), center=opt_center, color=vis_color, parent=canvas)
            if hasattr(screen, "get_Visual") and (vis := screen.get_Visual()):
                vis.parent = canvas.view.scene
            return screen

        # Create parabolic, spherical, or flat optical mirror surfaces
        kwargs = {"center": opt_center, "color": vis_color, "parentCanvas": canvas, "radius": radius, "xTilt": data.get("xTilt", 0.0), "yTilt": data.get("yTilt", 0.0), "mediumBefore": med_before, "mediumAfter": med_after}
        if "parabolic surface" in name_lower:
            return self.safe_instantiate(Parabolic_Surface, a=data.get("a", 1.0), b=data.get("b", 1.0), c=data.get("c", -1.0), centerHoleRadius=data.get("centerHoleRadius", 0.0), **kwargs)
        if "convex paraboloid" in name_lower:
            return self.safe_instantiate(Convex_Paraboloid, a=data.get("a", 1.0), b=data.get("b", 1.0), **kwargs)
        if "parabolic" in name_lower or "paraboloid" in name_lower:
            return self.safe_instantiate(Concave_Paraboloid, a=data.get("a", 1.0), b=data.get("b", 1.0), centerHoleRadius=data.get("centerHoleRadius", 0.0), **kwargs)
        if "spherical" in name_lower:
            return self.safe_instantiate(Spherical_Surface, radius_of_curvature=data.get("radius_of_curvature", 2.0), aperture_radius=radius, **kwargs)
        
        return self.safe_instantiate(Plane, width=2*radius, length=2*radius, **kwargs)

    # Makes a clean working copy of a light ray so we can trace its path through the scene
    def copy_ray_for_trace(self, comp, canvas):
        rc = OptRay(startPoint=OptPoint(*comp.lineStart_coordinates), rayDirection=comp.direction, wavelength=comp.wavelength, color=comp.color, dc=True, parentCanvas=canvas)
        self.frame.ray_visuals.append(rc.get_visual())
        return rc

    # Runs the simulation directly without background threads
    def run_simulation(self, user_initiated=True):
        self._start_simulation_gui()
        results = self._execute_raytracing_calculations(self._set_gauge_value)
        self._set_gauge_value(100)
        self._finish_simulation_gui(results, user_initiated)

    # Directly updates the progress bar on screen during ray tracing calculations
    def _set_gauge_value(self, val):
        if hasattr(self.frame, "panel_simulation") and (gauge := getattr(self.frame.panel_simulation, "gauge_Loading", None)):
            try:
                gauge.SetValue(val)
                wx.Yield() # Process pending GUI draw events directly
            except Exception:
                pass

    # Prepares the screen and loading bar when a new simulation starts
    def _start_simulation_gui(self):
        if hasattr(self.frame, "panel_simulation") and (gauge := getattr(self.frame.panel_simulation, "gauge_Loading", None)):
            try:
                gauge.SetRange(100)
                gauge.SetValue(5)
                gauge.Show(True)
                self.frame.panel_simulation.Layout()
            except Exception: pass

        # Clear old drawn light lines from 3D view
        for vis in self.frame.ray_visuals:
            if vis: vis.parent = None
        self.frame.ray_visuals.clear()
        self.frame.last_traced_rays.clear()

    # Traces each light ray through every optical component in the scene loop by loop
    def _execute_raytracing_calculations(self, progress_callback):
        if not self.frame.active_components:
            return {"status": "no_components"}
        canvas = self.frame.panel_simulation.canvas_obj
        if not canvas:
            return {"status": "no_canvas"}

        # Collect all light rays from active sources
        rays = []
        for n, c in self.frame.active_components.items():
            if is_light_source_name(n):
                if is_beam_name(n):
                    for r in c.get_Rays(): rays.append(self.copy_ray_for_trace(r, canvas))
                else:
                    rays.append(self.copy_ray_for_trace(c, canvas))

        if not rays:
            return {"status": "no_sources"}

        # Sort lenses and mirrors along the Z axis so light hits them in correct order
        sorted_comps = sorted([c for n, c in self.frame.active_components.items() if not is_light_source_name(n)], key=component_z_value)
        total_rays = len(rays)
        last_traced = []
        
        # Loop through each ray and calculate refractions directly
        for idx, ray in enumerate(rays):
            progress_callback(int(10 + ((idx + 1) / total_rays) * 80))
            current_ray = ray
            for comp in sorted_comps:
                if not current_ray: break
                current_ray = comp.calculate_RefractedRay(current_ray)
                if current_ray: 
                    self.frame.ray_visuals.append(current_ray.get_visual())
            if current_ray:
                last_traced.append(current_ray)

        progress_callback(100)
        return {"status": "success", "last_traced": last_traced, "canvas": canvas}

    # Cleans up when simulation completes and updates 2D plot diagrams and status message
    def _finish_simulation_gui(self, results, user_initiated):
        gauge = getattr(self.frame.panel_simulation, "gauge_Loading", None) if hasattr(self.frame, "panel_simulation") else None
        status = results.get("status")

        if status in ("no_components", "no_canvas", "no_sources"):
            if gauge:
                try: gauge.SetValue(0)
                except Exception: pass
            if status != "no_canvas":
                if hasattr(self.frame, "panel_plots"):
                    self.frame.panel_plots.update_plots([])
                if user_initiated:
                    msg = "No active components to simulate." if status == "no_components" else "No Light Sources in the system to trace."
                    wx.MessageBox(msg, "Info", wx.OK | wx.ICON_INFORMATION)
            return

        if status == "success":
            self.frame.last_traced_rays = results.get("last_traced", [])
            if canvas := results.get("canvas"):
                canvas.canvas.update()
            if hasattr(self.frame, "panel_plots"):
                self.frame.panel_plots.update_plots(self.frame.last_traced_rays)
            if hasattr(self.frame, "panel_components_tree"):
                self.frame.panel_components_tree.update_tree()
            if hasattr(self.frame, "GetStatusBar") and self.frame.GetStatusBar():
                self.frame.GetStatusBar().SetStatusText("Ray tracing simulation run complete.", 0)
            if gauge:
                try: gauge.SetValue(100)
                except Exception: pass
