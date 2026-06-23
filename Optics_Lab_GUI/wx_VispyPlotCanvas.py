import numpy as np
from vispy import scene


class wx_VispyPlotCanvas(scene.SceneCanvas):
	def __init__(self, *args, **kwargs):
		size = kwargs.pop("size", (300, 300))  # Default value is (300, 300)
		axes_color = kwargs.pop("axes_color", "teal")
		x_axis_label = kwargs.pop("x_axis_label", '')
		y_axis_label = kwargs.pop("y_axis_label", '')
		plot_title = kwargs.pop("plot_title", '')
		x_lim = kwargs.pop("x_lim", (0.0, 10.0))
		y_lim = kwargs.pop("y_lim", (0.0, 10.0))
		bgcolor = kwargs.pop("bgcolor", "#eef3fb")
		
		scene.SceneCanvas.__init__(self, *args, bgcolor=bgcolor, **kwargs)
		
		self.unfreeze()
		# Add all properties after unfreezing
		self.size = size
		self.axes_color = axes_color
		self.line = None
		self.lineVisual = None

		# Callback invoked when the camera range changes (e.g. pan/zoom by user).
		# Signature: on_range_changed(x_lim, y_lim)
		self.on_range_changed = None

		# Add a grid to place the widgets aligned to the grid
		self.grid = self.central_widget.add_grid(margin=10, spacing=0)
		
		# Add title to the plot
		title = scene.Label(plot_title, color=self.axes_color)
		title.height_max = 40
		self.grid.add_widget(title, row=0, col=0, col_span=2)
		
		self.xaxis = scene.AxisWidget(orientation='bottom', axis_label=x_axis_label, axis_font_size=10,
		                              axis_label_margin=25, tick_label_margin=15, axis_color=self.axes_color,
		                              tick_color=self.axes_color, text_color=self.axes_color)
		# Set only height and not width of x-axis to allow for expansion during resizing event of the parent
		self.xaxis.height_max = 50
		self.grid.add_widget(self.xaxis, row=2, col=1)
		
		self.yaxis = scene.AxisWidget(orientation='left', axis_label=y_axis_label, axis_font_size=10,
		                              axis_label_margin=25, tick_label_margin=5, axis_color=self.axes_color,
		                              tick_color=self.axes_color, text_color=self.axes_color)
		# Set only width and not height of y-axis to allow for expansion during resizing event of the parent
		self.yaxis.width_max = 50
		self.grid.add_widget(self.yaxis, row=1, col=0)
		
		# Add a view inside the grid. NOTE: Add the view only after adding the axes
		self.view = self.grid.add_view(row=1, col=1, border_color=self.axes_color, camera='panzoom')
		self.plotArea = self.view.scene
		
		self._x_lim = x_lim
		self._y_lim = y_lim
		# Link to the axes so that the axes can move along with the view when panned
		self.xaxis.link_view(self.view)
		self.yaxis.link_view(self.view)
		
		self.auto_set_viewBox_range()
		
		right_padding = self.grid.add_widget(row=1, col=2, row_span=1)
		right_padding.width_max = 50
		
		self.x_data = None
		self.y_data = None
		self.line_transform = None

		# Connect camera transform_change to detect user pan/zoom
		self.view.camera.transform.changed.connect(self._on_camera_changed)

		self.freeze()
		
		self.show()

	def _on_camera_changed(self, event=None):
		"""Fired when the user pans or zooms. Notify any linked canvases."""
		if self.on_range_changed is None:
			return
		try:
			rect = self.view.camera.rect
			x_lim = (rect.left, rect.right)
			y_lim = (rect.bottom, rect.top)
			self.on_range_changed(x_lim, y_lim)
		except Exception:
			pass

	@property
	def x_lim(self):
		return self._x_lim
	
	@x_lim.setter
	def x_lim(self, x_lim):
		self._x_lim = x_lim
		self.auto_set_viewBox_range()
	
	@property
	def y_lim(self):
		return self._y_lim
	
	@y_lim.setter
	def y_lim(self, y_lim):
		self._y_lim = y_lim
		self.auto_set_viewBox_range()

	def set_range(self, x_lim, y_lim):
		"""
		Set both axis ranges at once without triggering the range-changed
		callback (used by the sync logic to avoid recursive loops).
		"""
		self._x_lim = x_lim
		self._y_lim = y_lim
		self.auto_set_viewBox_range()

	def plot_xy(self, xdata, ydata, color='teal'):
		self.x_data = xdata
		self.y_data = ydata
		data = np.column_stack((xdata, ydata))
		return self.plot_data(data, color=color)
	
	def plot_data(self, data, line=None, color='teal'):
		assert data.ndim in [1, 2], "Plotting FAILED. Plot Data should be of the format (n,) or (n,2)"
		if data.ndim == 1:
			self.y_data = data
			self.x_data = np.linspace(0, len(self.y_data), len(self.y_data))
			data = np.column_stack((self.x_data, self.y_data))
		
		if self.lineVisual:
			self.lineVisual.parent = None
			
		self.lineVisual = scene.Line(data, color=color, parent=self.plotArea)
		self.line_transform = self.lineVisual.transforms.get_transform(map_to="canvas")
		
		# NOTE: Do NOT auto-override x_lim / y_lim here.
		# The caller (Load_Test._apply_telemetry_plots) explicitly sets the
		# limits after calling plot_xy so that all canvases share the same
		# x-axis window.  Overriding them here broke that synchronisation.
		# Simply refresh the view with whatever limits are currently stored.
		self.auto_set_viewBox_range()
		return line
	
	def auto_set_viewBox_range(self):
		# auto-scale to see the whole line.
		self.view.camera.set_range(x=self._x_lim, y=self._y_lim)

	def clear_plot(self):
		if self.lineVisual:
			self.lineVisual.parent = None
			self.lineVisual = None
