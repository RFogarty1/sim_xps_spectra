
import math
import types
import unittest
import sim_xps_spectra.x_sections.standard_objs as tCode

class TestStandardCrossSectionCalculator(unittest.TestCase):

	def setUp(self):
		self.testXSectionsA = [(10,20), (20,25), (30,35)]
		self.testAsymA = [(10,2), (20,4), (30,6)]
		self.xSectionPreFactor = 1 
		self.createTestObjs()

	def createTestObjs(self):
		self.databaseA = types.SimpleNamespace( getHvAgainstAOCrossSections=lambda x: self.testXSectionsA,
		                                        getHvAgainstAOAsymFactors=lambda x: self.testAsymA )
		self.tCalcA = tCode.CrossSectionCalculatorStandard(self.databaseA)

	def testExpectedHvReturned(self):
		testHvVals = [5,16,26]
		expHvVals = [10,20,30]
		actHvVals = [self.tCalcA.getHvUsedToCalculateCrossSection("fakeLabel", hv) for hv in testHvVals]
		self.assertEqual(expHvVals,actHvVals)


	def testAngularIndependentCrossSection(self):
		fakeLabel = "S3s"
		testHvVals = [5, 16, 26]
		expCrossSections = [self.xSectionPreFactor*x for x in [20,25,35]]
		actCrossSections = [self.tCalcA.calculateTotalCrossSection(fakeLabel,hv) for hv in testHvVals]
		self.assertEqual(expCrossSections,actCrossSections)

	def testAngularDependentCrossSection(self):
		testHv = 22
		testAngle = 50
		expOutput = 19.0118066625099
		actOutput = self.tCalcA.calculateTotalCrossSection( "fakeLabel", testHv, angle=testAngle )
		self.assertAlmostEqual( expOutput, actOutput )

	def testAngularDependentLinearPolarisedCrossSection(self):
		testHv = 22
		testAngle = 50
		expOutput = 36.9763866749802
		actOutput = self.tCalcA.calculateTotalCrossSection( "fakeLabel", testHv, angle=testAngle, pol="linear" )
		self.assertAlmostEqual( expOutput, actOutput )


	def testErrorRaisedIfAsymAndXSectionHvDifferent(self):
		testHv, testAngle = 20, 20
		self.testAsymA = [(1,20)]
		self.createTestObjs()
		with self.assertRaises(AssertionError):
			self.tCalcA.calculateTotalCrossSection("fakelabel",  testHv, angle=testAngle)
		with self.assertRaises(AssertionError):
			self.tCalcA.getHvUsedToCalculateCrossSection("fakelabel", testHv, angle=testAngle)

