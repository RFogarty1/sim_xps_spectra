
import math
from . import base_objs

class GauBroadenFunct(base_objs.BroadenFunctionBase):

	def __init__(self,exp, coeff, centre):
		""" Initializer for a Gaussian function (f(x) = c exp(a (x-x')^{2} )
		
		Args:
			exp: (float) Exponent prefactor, the value "a" above
			coeff: (float) Gaussian prefactor, the value "c" above
			centre: (float) The position of the centre of the Gaussian function, the value "x'" above

		"""
		self.exp = exp
		self.coeff = coeff
		self.centre = centre

	def _calcFunctValSingleX(self, xVal):
		outVal = self.coeff* math.exp( self.exp*((xVal - self.centre)**2) )
		return outVal

	def __call__(self, xVals):
		outVals = [self._calcFunctValSingleX(x) for x in xVals]
		return outVals
		

def createNormalisedGauFunctFromCentreAndFWHM(centre, fwhm):
	""" Creates a Gaussian broadening function with total area of 1.0
	
	Args:
		Centre: (Float) Position where Gaussian is centred (i.e. where the maximum is located)
		fwhm: Full-Width at half maximum. 

	Returns
		gauFunct: (BroadenFunctionBase obj) Callable class, takes iter of x values as input and return iter of y values
 
	"""
	sigma = fwhm / ( 2* math.sqrt(math.log(2)*2) )
	outCoeff = 1 / (sigma * math.sqrt(math.pi*2) )
	outExp = -1*(1 / (2*sigma*sigma))
	return GauBroadenFunct(outExp, outCoeff, centre)
