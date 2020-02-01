
import itertools as it
import math
from . import base_objs
import gen_basis_helpers.shared.misc_utils as misc

class BroadenFunctCompositeStandard(base_objs.BroadenFunctionStandard):


	leafObjs = misc.StandardComponentDescriptor("leafObjs")
	def __init__(self, objs:iter):
		""" Initializer for composite broadening function. When called, this objectsums all individual values from objs (i.e. used to get the sum of a list of broadening functions)
		
		Args:
			objs: (iter of BroadenFunctionBase). 
				 
		"""
		self.objs = list(objs)
		assert len(self.objs)>0, "Len of iter needs to be greater than zero"

	def __call__(self, xVals):
		allVals = list()

		#Calculate individual broadening functions
		for x in self.objs:
			allVals.append( x(xVals) )

		#Sum them all
		outVals = [0 for x in range(len(allVals[0]))]
		for currVals in allVals: #gets list of y-vals
			for idx,yVal in enumerate(currVals):
				outVals[idx] += yVal

		return outVals

	@property
	def areas(self):
		outList = list()
		for x in self.objs:
			outList.extend( x.areas )
		return outList

	@areas.setter
	def areas(self,vals):
		allObjs = self.leafObjs
		assert len(allObjs)==len(vals), "Exacltly one area must be given for each leaf; you gave {} areas for {} leafs".format( len(allObjs),len(vals) )
		for area,obj in it.zip_longest(vals,allObjs):
			obj.areas = [area]

		

class GauBroadenFunct(base_objs.BroadenFunctionStandard):

	def __init__(self,exp, coeff, centre):
		""" Initializer for a Gaussian function (f(x) = c exp(-a (x-x')^{2} )
		
		Args:
			exp: (float) Exponent prefactor, the value "a" above. MUST BE POSITIVE
			coeff: (float) Gaussian prefactor, the value "c" above
			centre: (float) The position of the centre of the Gaussian function, the value "x'" above

		"""
		self.exp = exp
		assert self.exp > 0, "Positive exponent required for Gaussian broadening function"
		self.coeff = coeff
		self.centre = centre

	def _calcFunctValSingleX(self, xVal):
		outVal = self.coeff* math.exp( -1*self.exp*((xVal - self.centre)**2) )
		return outVal

	def __call__(self, xVals):
		outVals = [self._calcFunctValSingleX(x) for x in xVals]
		return outVals

	@property
	def areas(self):
		gauIntegral =  math.sqrt( math.pi / self.exp )
		return [gauIntegral*self.coeff]

	@areas.setter
	def areas(self,val):
		assert len(val)==1, "Intensities needs an iter with ONE value, not {}".format(len(val))
		gauIntegral =  math.sqrt( math.pi / self.exp )
		self.coeff = val[0] / gauIntegral 

	@property
	def positions(self):
		return [self.centre]

	@positions.setter
	def positions(self,val):
		assert len(val)==1, "Positions needs an iter with ONE value, not {}".format(len(val))
		self.centre = val[0]

	@property
	def leafObjs(self):
		""" Property used on composite classes to find all leaf-objects. Just returns [self] for a leaf (this class) """
		return [self]


class BoxBroadenFunct(base_objs.BroadenFunctionStandard):


	def __init__(self, pos, width, height):
		""" Initializer for box function f(x) = area if pos-width<=x<=pos+width, else 0.0
		
		Args:
			pos: (float) x-value at which the function is centred
			width: (float) Width of the box function
			height: (float) Intensity of the box function when its non-zero
		"""

		self._pos = pos
		self._width = width
		self._height = height

	def __call__(self, xVals):
		outVals = list()
		minX, maxX = self._pos-self._width, self._pos+self._width
		for x in xVals:
			if ( x >= minX ) and (x <= maxX):
				outVals.append(self._height)
			else:
				outVals.append(0.0)
		return outVals

	@property
	def areas(self):
		""" For box broadening function this actually returns height rather than area """
		return [self._height]

	@areas.setter
	def areas(self, vals):
		assert len(vals) == 1, "areas needs an iter with ONE value, not {}".format(len(vals)) 
		self._height = vals[0]

	@property
	def positions(self):
		return [self._pos]

	@positions.setter
	def positions(self, vals):
		assert len(vals) == 1, "positions needs an iter with ONE value, not {}".format(len(vals)) 
		self._pos = vals[0]

	@property
	def leafObjs(self):
		""" Property used on composite classes to find all leaf-objects. Just returns [self] for a leaf (this class) """
		return [self]


def createNormalisedGauFunctFromCentreAndFWHM(centre, fwhm, area=1.0):
	""" Creates a Gaussian broadening function with total area of 1.0
	
	Args:
		Centre: (Float) Position where Gaussian is centred (i.e. where the maximum is located)
		fwhm: Full-Width at half maximum.
		area: (Optional, float) The area of the output Gaussian function. Default is an area of 1.0 

	Returns
		gauFunct: (BroadenFunctionBase obj) Callable class, takes iter of x values as input and return iter of y values
 
	"""
	sigma = fwhm / ( 2* math.sqrt(math.log(2)*2) )
	outCoeff = 1 / (sigma * math.sqrt(math.pi*2) )
	outExp = 1 / (2*sigma*sigma)
	return GauBroadenFunct(outExp, outCoeff*area, centre)
