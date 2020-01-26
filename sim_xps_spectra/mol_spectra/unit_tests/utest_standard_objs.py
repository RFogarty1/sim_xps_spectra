
import sim_xps_spectra.mol_spectra.standard_objs as tCode
import unittest


class TestMolFragLabel(unittest.TestCase):

	def setUp(self):
		self.fragKeyA, self.eleKeyA, self.aoKeyA = "tfragA", "Si", "3s"
		self.createTestObjs()

	def createTestObjs(self):
		self.testLabelA = tCode.MolFragLabel( fragKey=self.fragKeyA, eleKey=self.eleKeyA, aoKey=self.aoKeyA )

	def testExpectedComponents(self):
		expComponents = [self.fragKeyA, self.eleKeyA, self.aoKeyA]
		actComponents = self.testLabelA.components
		self.assertEqual(expComponents, actComponents)

