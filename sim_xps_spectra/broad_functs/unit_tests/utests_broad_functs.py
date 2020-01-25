

import itertools as it
import types
import unittest
import sim_xps_spectra.broad_functs.create_broaden_functs as tCode

class TestSingleGauBroadenFunct(unittest.TestCase):

	def setUp(self):
		self.testCoeffA, self.testExpA, self.testCentreA = 3, 0.5, 2.3
		self.fwhmA = 2.0
		self.createTestObjs()

	def createTestObjs(self):
		self.gauFunctA = tCode.GauBroadenFunct( self.testExpA, self.testCoeffA, self.testCentreA )
		self.normGauA = tCode.createNormalisedGauFunctFromCentreAndFWHM(self.testCentreA, self.fwhmA)

	def testSimpleGauBroadenFunct(self):
		self.testXVals = [1,2,3,4]
		expVals = [1.28867207463222, 2.8679924454993, 2.3481136147256, 0.70723822966759] 
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

	def testAreasNormdGau(self):
		normAreas =self.normGauA.areas
		expNormAreas = [1.0]
		for exp,act in it.zip_longest(expNormAreas, normAreas):
			self.assertAlmostEqual(exp,act)
		
	def testAreasSetter(self):
		expAreas = [3.5]
		self.normGauA.areas = expAreas
		actAreas = self.normGauA.areas
		for exp,act in it.zip_longest(expAreas, actAreas):
			self.assertAlmostEqual(exp,act)

	def testPositionsSetter(self):
		expPositions = [10.5]
		self.gauFunctA.positions = expPositions
		actPositions = self.gauFunctA.positions
		for exp,act in it.zip_longest(expPositions,actPositions):
			self.assertAlmostEqual(exp,act)



class DudCallableWithInputFunct():
	def __init__(self, inpFunct, **kwargs):
		self.inpFunct = inpFunct
		for key in kwargs.keys():
			setattr(self, key, kwargs[key])

	@property
	def leafObjs(self):
		return [self]

	def __call__(self,xVals):
		return self.inpFunct(xVals)

class TestCompositeBroadFuncts(unittest.TestCase):

	def setUp(self):
		self.broadFunctA = lambda x: [a*2 for a in x]
		self.broadFunctB = lambda x: [a+1 for a in x]
		self.broadFunctC = lambda x: [a+5 for a in x]
		self.areaA, self.areaB, self.areaC = 2,3,4
		self.positionA, self.positionB, self.positionC = 4,5,6
		self.createTestObjs()

	def createTestObjs(self):
		self.broadObjA = DudCallableWithInputFunct( self.broadFunctA, positions=[self.positionA], areas=[self.areaA] )
		self.broadObjB = DudCallableWithInputFunct( self.broadFunctB, positions=[self.positionB], areas=[self.areaB] )
		self.broadObjC = DudCallableWithInputFunct( self.broadFunctC, positions=[self.positionC], areas=[self.areaC] )
		self.compA = tCode.BroadenFunctCompositeStandard([self.broadObjA, self.broadObjB])
		self.compB = tCode.BroadenFunctCompositeStandard([self.compA, self.broadObjC])

	def testSimpleSumOneLevelComposite(self):
		testXVals = [1,2,3]
		expYVals = [(x*2)+1+x for x in testXVals]
		actYVals = self.compA(testXVals)
		[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(expYVals, actYVals)]

	def testSimpleSumTwoLevelComposite(self):
		testXVals = [1,2,3]
		expYVals = [ (x*2) + (x+1) + (x+5) for x in testXVals]
		actYVals = self.compB(testXVals)
		for exp,act in it.zip_longest(expYVals, actYVals):
			self.assertAlmostEqual(exp,act)

	def testAreasTwoLevelComposite(self):
		""" Test both getting and setting of areas for a two-level composite broadening function """
		expAreas = [self.areaA*2, self.areaB*2, self.areaC*2]
		self.compB.areas = expAreas
		actAreas = self.compB.areas
		[self.assertAlmostEqual(exp,act) for exp,act in it.zip_longest(expAreas,actAreas)]

if __name__ == '__main__':
	unittest.main()


