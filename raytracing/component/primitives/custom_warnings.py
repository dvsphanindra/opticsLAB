import warnings

class IntersectionWarning(UserWarning):
	name="IntersectionWarning"
	
# Reformat the default warning to print only the warning message and disable printing the source line generating warning
def _warning(msg, category, filename, line_no, *args, **kwargs):
	# Change the format in which the warning is displayed
	if isinstance(category, IntersectionWarning):
		return  filename + ":" + str(line_no) + ":: " + str(category.name) + ": " + str(msg) + '\n'
	
warnings.showwarning = _warning
