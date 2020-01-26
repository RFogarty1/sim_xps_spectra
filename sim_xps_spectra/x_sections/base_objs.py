

class CrossSectionDatabaseBase():
	"""Base class for representing a database of cross-sections (including assymetry factors)
	"""

	def getHvAgainstAOCrossSections(self,label):
		""" Returns list of photon energies (hv) against atomic-orbital cross section for atomic orbital reperesented by label
		
		Args:
			label: (str), Key to obtain atomic orbital cross sections. This is the base-class docstring so cant give DEFINITE example, but something like "S3s" should probably work
				 
		Returns
			crossSections: (2-element iter) List of photon energies with cross sections IN ORDER of increasing photon energy. e.g. [(5,20),(10,15)] might be returned
	 
		"""
		raise NotImplementedError("")


	def getHvAgainstAOAsymFactors(self,label):
		""" Returns list of photon energies (hv) against atomic-orbital asymetry factors for atomic orbital reperesented by label
		
		Args:
			label: (str), Key to obtain atomic orbital asymetry factors. This is the base-class docstring so cant give DEFINITE example, but something like "S3s" should probably work
				 
		Returns
			asymFactors: (2-element iter) List of photon energies with asym factors IN ORDER of increasing photon energy. e.g. [(5,20),(10,15)] might be returned
	 
		"""
		raise NotImplementedError("")


class CrossSectionCalculatorBase():
	"""Class Used to calculate total cross-sections (which can include angular effects) for an atomic orbital at a certain photon energy/angle

	"""

	def getHvUsedToCalculateCrossSection(label, hv, angle=None, ao=True):
		""" Return the hv actually used to calculate the cross-section. Useful if not using any kind of interpolation, and making sure all cross-sections are really calculated at the same hv
		
		Args:
			label: (str) Key to obtain cross-sections (e.g. might be S3s for sulfur 3s case)
			hv: (float) - Photon energy to use to calculate cross-section
			angle: (Float,Optional, in DEGREES) - If None then dont take angular dependence into account
			ao: (Boolean, Optional) - If False then return 1 for the angular-independent part of the atomic orbital cross section
				 
		Returns
			hv: The photon energy that would be used to calculate the cross-section defined by input args
		"""
		raise NotImplementedError("")


	def calculateTotalCrossSection(label, hv, angle=None, ao=True):
		""" Return the total cross-section (combination of angular-dependent and independent parts)

		Args:
			label: (str) Key to obtain cross-sections (e.g. might be S3s for sulfur 3s case)
			hv: (float) - Photon energy to use to calculate cross-section
			angle: (Float,Optional, in DEGREES) - If None then dont take angular dependence into account
			ao: (Boolean, Optional) - If False then return 1 for the angular-independent part of the atomic orbital cross section
				 
		Returns
			crossSection: The cross section for this atomic orbital at the given hv and angle
		"""
		raise NotImplementedError("")

