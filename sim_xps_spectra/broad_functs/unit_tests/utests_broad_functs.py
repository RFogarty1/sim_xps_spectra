

import itertools as it
import unittest
import sim_xps_spectra.broad_functs.create_broaden_functs as tCode

class TestSingleGauBroadenFunct(unittest.TestCase):

	def setUp(self):
		self.testCoeffA, self.testExpA, self.testCentreA = 3, 0.5, 2.3
		self.createTestObjs()

	def createTestObjs(self):
		self.gauFunctA = tCode.GauBroadenFunct( self.testExpA, self.testCoeffA, self.testCentreA )

	def testSimpleGauBroadenFunct(self):
		self.testXVals = [1,2,3,4]
		expVals = [6.9839334437107, 3.13808357972615, 3.83286393961466, 12.7255564284613]
		actVals = self.gauFunctA(self.testXVals)
		for exp,act in it.zip_longest(expVals, actVals):
			self.assertAlmostEqual(exp,act)

	def testNormalisedGauBroadenFunct(self):
		testXVals = [1,2,3,4] #Value at 3 should be half the value at 4.0 (FWHM=2)
		centre = 4.0
		fwhm = 2.0
		expVals = [0.00091741921748, 0.029357414959364, 0.234859319674913, 0.469718639349826]
		outFunct = tCode.createNormalisedGauFunctFromCentreAndFWHM(centre, fwhm)
		actVals = outFunct(testXVals)
		for exp,act in it.zip_longest(expVals, actVals):
			self.assertAlmostEqual(exp,act)

if __name__ == '__main__':
	unittest.main()


