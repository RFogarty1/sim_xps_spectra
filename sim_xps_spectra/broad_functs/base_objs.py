

class BroadenFunctionBase():
	"""Base class for the broadening function objects. This object should be called directly with a list of xValues and it will return a list of corresponding y-values (i.e. this is a callable class)
	"""
	def __call__(self, xVals):
		raise NotImplementedError("")

