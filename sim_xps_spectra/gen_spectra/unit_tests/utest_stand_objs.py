
import types
import itertools as it
import unittest
import unittest.mock as mock

import sim_xps_spectra.gen_spectra.standard_objs as tCode


class TestStandardSpectraInputClass(unittest.TestCase):

	def setUp(self):
		self.broadFunctA = lambda x: [2*a for a in x]
		self.broadFunctB = lambda x: [a for a in x]
		self.broadFunctC = lambda x: [3*a for a in x]
		self.labelA, self.labelB, self.labelC = mock.Mock(), mock.Mock(), mock.Mock()

		self.createTestObjs()

	def createTestObjs(self):
		self.nonCompTestObjA = tCode.GenSpectraInputStandard( self.broadFunctA, self.labelA )
		self.nonCompTestObjB = tCode.GenSpectraInputStandard( self.broadFunctB, self.labelB )
		self.nonCompTestObjC = tCode.GenSpectraInputStandard( self.broadFunctC, self.labelC )
		self.compTestObjA = tCode.GenSpectraInputCompositeStandard( [self.nonCompTestObjA, self.nonCompTestObjB] )
		self.compTestObjB = tCode.GenSpectraInputCompositeStandard( [self.compTestObjA, self.nonCompTestObjC] )

	def testCalcSpectraInputsActMatchesExp_nonComposite(self):
		self.createTestObjs()
		testXVals = [1,2,3]
		expYVals = [2,4,6]
		actYVals = self.nonCompTestObjA.calculateSpectralContribs(testXVals)
		self.assertTrue( len(actYVals)==1 )
		self.assertEqual(expYVals, actYVals[0])

	def testCalcSpectraInputActMatchesExp_basicComposite(self):
		self.createTestObjs()
		testXVals = [1,2,3]
		expYVals = [ [2,4,6], [1,2,3] ]
		actYVals = self.compTestObjA.calculateSpectralContribs(testXVals)
		for exp,act in it.zip_longest(expYVals, actYVals):
			self.assertEqual(exp,act)

	def testCalcSpectraInputActMatchesExp_twoLevelComposite(self):
		""" Test we get expected spectral contributions with a composite made of another composite + leaf """
		testXVals = [1,2,3]
		expYVals = [ [2,4,6], [1,2,3], [3,6,9] ]
		actYVals = self.compTestObjB.calculateSpectralContribs(testXVals)
		for exp,act in it.zip_longest(expYVals, actYVals):
			self.assertEqual(exp,act)


	def testLabelSearchCompositeExpVsActualA(self):
		""" Test we can extract a leaf from a composite object using composite-search """
		self.labelA.components = ["labA","random_comp"]
		self.labelB.components = ["labB", "another_comp"]
		self.createTestObjs()
		self.assertTrue( len(self.compTestObjA.label)==2 )

		outList = self.compTestObjA.getObjectsWithComponents(["labA"])
		self.assertTrue(len(outList)==1) #Should only find a single match
		self.assertEqual( self.labelA.components, outList[0].label[0].components ) #The label(hence object) should match labelA

class TestGenSpectraOutputObjs(unittest.TestCase):

	def setUp(self):
		self.labelA, self.labelB, self.labelC = mock.Mock(), mock.Mock(), mock.Mock()
		self.allXVals = [1,2,3]
		self.dataA = [(x,y) for x,y in it.zip_longest(self.allXVals,[2,3,4])]
		self.dataB = [(x,y) for x,y in it.zip_longest(self.allXVals,[5,6,7])]
		self.dataC = [(x,y) for x,y in it.zip_longest(self.allXVals,[8,9,5])]
		self.createTestObjs()

	def createTestObjs(self):
		self.leafA = tCode.GenSpectraOutputStandard( self.dataA, self.labelA )
		self.leafB = tCode.GenSpectraOutputStandard( self.dataB, self.labelB )
		self.leafC = tCode.GenSpectraOutputStandard( self.dataC, self.labelC )
		self.testCompA = tCode.GenSpectraOutputCompositeStandard( [self.leafA, self.leafB] )
		self.testCompB = tCode.GenSpectraOutputCompositeStandard( [self.testCompA, self.leafC] )


	def testTotalSpectraContribs_twoLevelComposite(self):
		expXVals = self.allXVals
		expYVals = [15,18,16]
		expVals = [(x,y) for x,y in it.zip_longest(expXVals, expYVals)]
		actVals = self.testCompB.totalSpectralContributions
		self.assertEqual(expVals, actVals)

if __name__ == '__main__':
	unittest.main()

