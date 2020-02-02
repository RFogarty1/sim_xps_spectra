
import unittest
import sim_xps_spectra.gen_spectra.standard_objs as genObjs
import sim_xps_spectra.mol_spectra.standard_objs as molObjs

import sim_xps_spectra.mol_spectra.input_output as tCode

class TestWriteOutputs(unittest.TestCase):

	def setUp(self):
		self.dataA = [ (1,2), (2,4), (3,6) ]
		self.dataB = [ (1,3), (2,5), (3,5) ] 
		self.labelA = molObjs.MolFragLabel(fragKey="fragA", eleKey="Si", aoKey="2s")
		self.labelB = molObjs.MolFragLabel(fragKey="fragB", eleKey="C", aoKey="2p")
		self.createTestObjs()

	def createTestObjs(self):
		self.specOutLeafA = genObjs.GenSpectraOutputStandard(self.dataA, self.labelA)
		self.specOutLeafB = genObjs.GenSpectraOutputStandard(self.dataB, self.labelB)
		self.specOutCompositeA = genObjs.GenSpectraOutputCompositeStandard( [self.specOutLeafA, self.specOutLeafB] )

	def testTotalSpectralContribs(self):
		expTotalData = [ (1,5), (2,9), (3,11) ]
		fmtStr = "{:.9f}, {:.9f}"
		expOutStr = "\n".join( [ "#Energy, Intensities",
		                         fmtStr.format(*expTotalData[0]),
		                         fmtStr.format(*expTotalData[1]),
		                         fmtStr.format(*expTotalData[2]) ] )
		actOutStr = tCode.getTotalContribStrFromSpectraOutput( self.specOutCompositeA )
		self.assertEqual(expOutStr, actOutStr)

	def testIndividualSpectralContribs(self):
		expTotalData = [ (1,2,3), (2,4,5), (3,6,5) ]
		fmtStr = "{:.9f}, {:.9f}, {:.9f}"
		expOutStr = "\n".join( ["#labels = fragA-Si-2s, fragB-C-2p",
		                        "#Energy, Intensities",
		                        fmtStr.format( *expTotalData[0] ),
		                        fmtStr.format( *expTotalData[1] ),
		                        fmtStr.format( *expTotalData[2] ) ] )
		actOutStr = tCode.getAllContribsOutputStrFromSpectraOutput(self.specOutCompositeA)
		self.assertEqual(expOutStr, actOutStr)
