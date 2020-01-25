

class BroadenFunctionBase():
	"""Base class for the broadening function objects. This object should be called directly with a list of xValues and it will return a list of corresponding y-values (i.e. this is a callable class)
	"""
	def __call__(self, xVals):
		raise NotImplementedError("")


class BroadenFunctionStandard(BroadenFunctionBase):
	""" This object should be called directly with a list of xValues and it will return a list of corresponding y-values (i.e. this is a callable class). This is the "standard" broadening function interface, which means it implements gettable/settable intensity values on top of the basic interface"""

	@property
	def areas(self):
		""" (float iter) representing the area of each broadening function 
		"""
		raise NotImplementedError("")

	@areas.setter
	def areas(self,vals):
		raise NotImplementedError("")

	@property
	def positions(self):
		""" (float iter) representing where each contributing broadening function is centred
		"""
		raise NotImplementedError("")

	@positions.setter
	def positions(self, vals):
		raise NotImplementedError("")
	





