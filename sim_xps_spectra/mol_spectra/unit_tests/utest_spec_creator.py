
import copy
import itertools as it
import math
import unittest
import unittest.mock as mock

import sim_xps_spectra.mol_spectra.spectrum_creator as tCode
import sim_xps_spectra.mol_spectra.standard_objs as molObjs
import sim_xps_spectra.broad_functs.create_broaden_functs as broadenFuncts

class TestSpecCreator(unittest.TestCase):

	def setUp(self):
		#Info needed for spectrum fragments
		self.energiesA = [3,4]
		self.energiesB = [1]
		self.intensitiesA = [5,6]
		self.intensitiesB = [2]
		self.labelA = molObjs.MolFragLabel(fragKey="fragA", eleKey="C", aoKey="2s")
		self.labelB = molObjs.MolFragLabel(fragKey="fragB", eleKey="C", aoKey="2p")

		#Mock the cross sectios and asym factors
		self.xSectionsA = [(5.0,3) , (10.0,4)] #(hv,val)
		self.xSectionsB = [(5.0,12), (10.0,15)]

		self.asymA = [(5.0,2), (10.0,1.5)]
		self.asymB = [(5.0,1), (10.0,1.2)]


		#xVals to use
		self.testXVals = [1,2,3]

		#Normalised broaden funct, we use a box function here
		self.bFunctWidth = 1.01

		#other
		self.photonEnergy = 6
		self.emissionAngle = None

		self.createTestObjs()

	def createTestObjs(self):
		xSectDict = {"C2s":self.xSectionsA, "C2p":self.xSectionsB}
		asymDict  = {"C2s":self.asymA     , "C2p":self.asymB}
		#mocked database
		self.mockDbA = mock.Mock()
		self.mockDbA.getHvAgainstAOCrossSections.side_effect = lambda x: xSectDict[x]
		self.mockDbA.getHvAgainstAOAsymFactors.side_effect = lambda x: asymDict[x]

		self.specFragsA = tCode.SpectrumFragmentStandard(self.energiesA, self.intensitiesA, self.labelA)
		self.specFragsB = tCode.SpectrumFragmentStandard(self.energiesB, self.intensitiesB, self.labelB)
		bFunctPos, bFunctHeight = 0, 1
		self.normBFunct = broadenFuncts.BoxBroadenFunct(bFunctPos, self.bFunctWidth, bFunctHeight) 
		self.testObjA = tCode.SpectrumCreatorStandard(spectraFrags=[self.specFragsA, self.specFragsB], normBFunct=self.normBFunct,
		                                              xSectionDatabase=self.mockDbA, photonEnergy=self.photonEnergy,
		                                              emissionAngle=self.emissionAngle, xVals=self.testXVals) 

	def testExpVsActAttNoAngular_setA(self):
		self.createTestObjs()
		expVals = [24,39,33]
		outSpec = tCode.createSpectrumFromStandardCreator( self.testObjA )
		actVals = [x[1] for x in outSpec.totalSpectralContributions]
		[self.assertAlmostEqual(exp,act) for (exp,act) in it.zip_longest(expVals,actVals)]

	def testExpVsActWithAngular_setA(self):
		self.emissionAngle = 60
		self.createTestObjs()
		expVals = [25.5,42.375,37.125]
		outSpec = tCode.createSpectrumFromStandardCreator( self.testObjA )
		actVals = [x[1] for x in outSpec.totalSpectralContributions]
		[self.assertAlmostEqual(exp,act) for (exp,act) in it.zip_longest(expVals,actVals)]

	def testRaisesAssertWhenHvVaries(self):
		self.xSectionsA = [(10,0.5)]
		self.createTestObjs()
		with self.assertRaises(AssertionError):
			tCode.createSpectrumFromStandardCreator( self.testObjA )


class TestSpecFrag(unittest.TestCase):

	def setUp(self):
		self.fragLabelA = molObjs.MolFragLabel(fragKey="fragA", eleKey="C", aoKey="2s")
		self.energiesA = [2,3,4]
		self.intensitiesA = [0,1,2]
		self.createTestObjs()

	def createTestObjs(self):
		self.objA = tCode.SpectrumFragmentStandard(self.energiesA, self.intensitiesA, self.fragLabelA)

	def testEqMethod_twoEqual(self):
		self.assertTrue(self.objA == self.objA)

	def testEqMethod_twoUnequalEnergies(self):
		objA = copy.deepcopy(self.objA)
		self.energiesA[0] = self.energiesA[0] + 1
		self.createTestObjs()
		self.assertTrue(objA != self.objA)

	def testEqMethod_twoUnequalIntensities(self):
		objA = copy.deepcopy(self.objA)
		self.intensitiesA[0] = self.intensitiesA[0] + 0.5	
		self.createTestObjs()
		self.assertTrue( objA != self.objA )

	def testEqMethod_twoDiffLenIntensitiesAndEnergies(self):
		objA = copy.deepcopy(self.objA)
		self.intensitiesA.append(5)
		self.energiesA.append(3)
		self.createTestObjs()
		self.assertTrue( objA != self.objA )

	def testEqMethod_twoUnequalLabels(self):
		objA = copy.deepcopy(self.objA)
		self.fragLabelA = molObjs.MolFragLabel(fragKey="fragA", eleKey="S", aoKey="2s")
		self.createTestObjs()
		self.assertTrue( objA != self.objA )




