
""" These objects define the interfaces used in this part of the code """



class GenSpectraInput():
	"""Class acting as the input to generate XPS spectra. Composite pattern expected.

	"""
	@property
	def label(self):
		""" iter of BaseLabel objects from leaf fragments. These have a .components property listing strings
		associated with that fragment (e.g. ["anion","sulfur","3s"] might be returned from one label.components) 
		"""
		raise NotImplementedError("")

	
	def calculateSpectralContribs(self, xVals):
		""" Calculate spectral contributions on all leafs at given set of x-values
		
		Args:
			xVals: (iter) floats at which to evaluate each of the functions (i.e. calculate the spectral contribs at these x-values)
				 
		Returns
			iter of yVal iters; 1 per leaf object. For example xVals=[5.0,6.0] might give [ [1.0,2.0], [1.5,2.5] ] if two leaf fragments are present
	 
		"""
		raise NotImplementedError("")


class GenSpectraOutput():
	"""Class acting as the output from generated XPS spectra. Composite pattern expected.
	"""

	@property
	def totalSpectralContributions(self):
		""" nx2 array when np.array(x) applied; The sum of spectraContributions from all leaf objects
		"""

	@property
	def spectralContributions(self):
		""" iter, each element contains spectral contributions from one component (e.g. the anion sulfur 3s contribs). Each element should be such
		that np.array(element) produces an nx2 matrix (column 1 are usually binding energies, column 2 intensities) 
		"""
		raise NotImplementedError("")

	@property
	def label(self):
		""" iter of BaseLabel objects from leaf fragments. These have a .components property listing strings
		associated with that fragment (e.g. ["anion","sulfur","3s"] might be returned from one label.components) 
		"""
		raise NotImplementedError("")

