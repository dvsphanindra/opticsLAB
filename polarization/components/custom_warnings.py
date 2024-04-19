import warnings

class IntersectionWarning(UserWarning):
	name="IntersectionWarning"
	
class RetarderNote(UserWarning):
	name="RetarderNote"
	
# Reformat the default warning to print only the warning message and disable printing the source line generating warning
def _warning(msg, category, filename, line_no, *args, **kwargs):
	# Change the format in which the warning is displayed
	if isinstance(category, IntersectionWarning):
		return  filename + ":" + str(line_no) + ":: " + str(category.name) + ": " + str(msg) + '\n'
	if isinstance(category, RetarderNote):
		print("Here")
		return "Hello"
	
warnings.showwarning = _warning
