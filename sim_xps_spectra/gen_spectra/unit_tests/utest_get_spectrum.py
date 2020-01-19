

import itertools as it
import unittest
import unittest.mock as mock

import sim_xps_spectra.gen_spectra.base_objs as baseObjs
import sim_xps_spectra.gen_spectra.get_spectrum as tCode


class DudGenInpClass(baseObjs.GenSpectraInput):
	def __init__(self, calcSpecFunct, labelObj):
		self._label = labelObj
		self._calcSpecFunct = calcSpecFunct
	
	@property
	def label(self):
		return [self._label]

	def calculateSpectralContribs(self, xVals):
		return self._calcSpecFunct(xVals)

class TestGetSpectrum(unittest.TestCase):

	def setUp(self):
		self.specFunctA = lambda x: [[a*2 for a in x]]
		self.leafA = DudGenInpClass( self.specFunctA, mock.Mock() )


	def testExpTotalSpectrumOutput(self):
		testXVals = [1,2,3]
		expVals = [(x,y) for x,y in it.zip_longest(testXVals,[2,4,6])]
		outObj = tCode.getSpectrumFromApplyingBroadeningFuncts(testXVals, self.leafA)
		actVals = outObj.totalSpectralContributions
		for exp,act in it.zip_longest(expVals,actVals):
			self.assertEqual(exp,act)

	@unittest.skip("")
	def testExpTotalSpectrumOutputFromCompositeInput(self):
		self.assertTrue(False)

if __name__ == '__main__':
	unittest.main()

