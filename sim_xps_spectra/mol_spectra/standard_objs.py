
import gen_basis_helpers.shared.label_objs as baseLabels



class MolFragLabel(baseLabels.BaseLabel):
	"""Label class used to differentiate contributions to atomic spectra, and also (in some cases) to figure out the cross-sections to use.

	Attributes:
		fragKey: (str, Optional) The molecular fragment this is part of. Default is "fragA"
		eleKey: (str) Elemental symbol for this atomic orbital. E.g. for a sulfur 3s orbital it woul be "S"; for Germanium 3p it would be "Ge"
		aoKey: (str) Represents the atomic orbital type. Recommended to be of a format like 3s, i.e. the quantum number followed by a symbol for angular momentum
	"""
	

	def __init__(self, fragKey=None, eleKey=None, aoKey=None):
		if fragKey is None:
			self.fragKey = "fragA"

		self.fragKey = fragKey
		self.eleKey = eleKey
		self.aoKey = aoKey

		self.reqArgs = ["fragKey", "eleKey", "aoKey"]
		for x in self.reqArgs:
			if getattr(self,x) is None:
				raise ValueError("{} is a required argument for MolFragLabel".format(x))

	@property
	def labelNames(self):
		return self.reqArgs

	@property
	def components(self):
		return [getattr(self,x) for x in self.reqArgs]

	@property
	def xSectionLabel(self):
		""" Str reperesenting the required cross-section (e.g. S3s) for this fragment """
		return self.eleKey + self.aoKey



