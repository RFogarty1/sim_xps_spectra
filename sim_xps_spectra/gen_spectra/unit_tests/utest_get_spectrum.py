

import itertools as it
import unittest
import unittest.mock as mock

import sim_xps_spectra.gen_spectra.base_objs as baseObjs
import sim_xps_spectra.gen_spectra.standard_objs as stdObjs
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
		self.specFunctB = lambda x: [[a*3 for a in x]]
		self.createTestObjs()

	def createTestObjs(self):
		self.leafA = DudGenInpClass( self.specFunctA, mock.Mock() )
		self.leafB = DudGenInpClass( self.specFunctB, mock.Mock() )
		self.compA = stdObjs.GenSpectraInputCompositeStandard( [self.leafA, self.leafB] )

	def testExpTotalSpectrumOutput(self):
		testXVals = [1,2,3]
		expVals = [(x,y) for x,y in it.zip_longest(testXVals,[2,4,6])]
		outObj = tCode.getSpectrumFromApplyingBroadeningFuncts(testXVals, self.leafA)
		actVals = outObj.totalSpectralContributions
		self.assertEqual(expVals, actVals)

	def testExpTotalSpectrumOutputFromCompositeInput(self):
		testXVals = [1,2,3]
		expVals = [(x,y) for x,y in it.zip_longest(testXVals,[5,10,15])]
		outObj = tCode.getSpectrumFromApplyingBroadeningFuncts(testXVals, self.compA)
		actVals = outObj.totalSpectralContributions
		self.assertEqual(expVals,actVals)

	def testExpIndividualContribsOutputFromCompositeInput(self):
		testXVals = [1,2,3]
		expValsA = [(x,y) for x,y in it.zip_longest(testXVals,[2,4,6])]
		expValsB = [(x,y) for x,y in it.zip_longest(testXVals,[3,6,9])]
		allExpVals = [expValsA, expValsB]
		outObj = tCode.getSpectrumFromApplyingBroadeningFuncts(testXVals, self.compA)
		actVals = outObj.spectralContributions
		self.assertEqual(allExpVals,actVals)

if __name__ == '__main__':
	unittest.main()

