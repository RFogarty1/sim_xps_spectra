

import unittest
import unittest.mock as mock

import sim_xps_spectra.mol_spectra.standard_objs as molObjs
import sim_xps_spectra.mol_spectra.spectrum_creator as specCreate

import sim_xps_spectra.parsers.parse_mlinpt as tCode

class TestMlInptParser(unittest.TestCase):

	def setUp(self):
		mFactor = 2
		self.expEnergiesAll = [-4.498144, -4.498144, -4.467938, -1.090113, -1.090113]
		self.expIntensitiesC2s = [mFactor*x for x in [0.0,0.0, -0.012118, 0.0, 0.0]]
		self.expIntensitiesC2p = [mFactor*x for x in [0.479424, 0.479424, 0.118512, -0.003038, -0.003038]]
		self.expIntensitiesC2d = [mFactor*x for x in [0.001116, 0.001116, 0.000237, 0.015583, 0.015583]]
		self.expLabelC2s = molObjs.MolFragLabel(fragKey="fragA", eleKey="C", aoKey="2S")
		self.expLabelC2p = molObjs.MolFragLabel(fragKey="fragA", eleKey="C", aoKey="2P")
		self.expLabelC2d = molObjs.MolFragLabel(fragKey="fragA", eleKey="C", aoKey="2D")
		self.fakeInpPathA = "/some/fake/dir/fragA_MLinpt.txt"
		self.createTestObjs()

	def createTestObjs(self):
		self.expOutC2s = specCreate.SpectrumFragmentStandard( self.expEnergiesAll, self.expIntensitiesC2s, self.expLabelC2s )
		self.expOutC2p = specCreate.SpectrumFragmentStandard( self.expEnergiesAll, self.expIntensitiesC2p, self.expLabelC2p )
		self.expOutC2d = specCreate.SpectrumFragmentStandard( self.expEnergiesAll, self.expIntensitiesC2d, self.expLabelC2d )

	@mock.patch("sim_xps_spectra.parsers.parse_mlinpt._readFileIntoList")
	def testExpVsActMatch(self, mockedReadFileIntoList):
		mockedReadFileIntoList.side_effect = lambda x: _getTestFileAsListA()
		expVal = [self.expOutC2s, self.expOutC2p, self.expOutC2d]
		actVal = tCode.getSpecFragsFromMLInptFile( self.fakeInpPathA )
		self.assertEqual(expVal, actVal)



def _getTestFileAsListA():
	outList = [ "# M_FACTOR=2.0\n",
	            "# Energy (eV),TDOS,C2S,C2P,C2D\n",
	            "-4.498144,1.000000,0.000000,0.479424,0.001116\n",
	            "-4.498144,1.000000,0.000000,0.479424,0.001116\n",
	            "-4.467938,1.000000,-0.012118,0.118512,0.000237\n",
	            "-1.090113,1.000000,0.000000,-0.003038,0.015583\n",
	            "-1.090113,1.000000,0.000000,-0.003038,0.015583\n" ]
	return outList


class TestMlInptWriter(unittest.TestCase):

	@mock.patch("sim_xps_spectra.parsers.parse_mlinpt._readFileIntoList")
	def setUp(self, mockedReadFileIntoList):
		mockedReadFileIntoList.side_effect = lambda x: _getTestFileAsListB()
		self.fragmentsA = tCode.getSpecFragsFromMLInptFile("fakePathA")
		self.outPathA = "fake/out/path"

	@mock.patch("sim_xps_spectra.parsers.parse_mlinpt._writeStrToFile")
	def testExpMatchesActA(self, mockedWriter):
		expOutStr = "".join([x for x in _getTestFileAsListB()])
		tCode.writeMLInptFileFromPathAndSpecFrags(self.outPathA, self.fragmentsA)
		mockedWriter.assert_called_once_with(self.outPathA, expOutStr)

	@mock.patch("sim_xps_spectra.parsers.parse_mlinpt._writeStrToFile")
	def testRaisesForInconsistentEnergies(self, mockedWriter):
		self.fragmentsA[0].energies[0] += 0.2
		self.assertTrue( abs(self.fragmentsA[0].energies[0] - self.fragmentsA[1].energies[0]) >0.001 ) #Check our fragment energies are inconsistent
		with self.assertRaises(ValueError):
			tCode.writeMLInptFileFromPathAndSpecFrags(self.outPathA, self.fragmentsA)

	@mock.patch("sim_xps_spectra.parsers.parse_mlinpt._writeStrToFile")
	def testRaisesForEnergiesOfDiffLengths(self, mockedWriter):
		self.fragmentsA[1].energies.append(0.5)
		self.assertNotEqual( len(self.fragmentsA[0].energies), len(self.fragmentsA[1].energies) )
		with self.assertRaises(ValueError):
			tCode.writeMLInptFileFromPathAndSpecFrags(self.outPathA, self.fragmentsA)


#Really need M_FACTOR to equal 1 to test the writing aspect. We should only ever be writing to get the output intensities
#(which should include this factor) so this shouldnt be an issue really
#ALSO: This has the numbers formatted at .6g, rather than .6f above
def _getTestFileAsListB():
	outList = [ "# M_FACTOR=1.0\n",
	            "# Energy (eV),TDOS,C2S,C2P,C2D\n",
	            "-4.49814,0.48054,0,0.479424,0.001116\n",
	            "-4.49814,0.48054,0,0.479424,0.001116\n",
	            "-4.46794,0.106631,-0.012118,0.118512,0.000237\n",
	            "-1.09011,0.012545,0,-0.003038,0.015583\n",
	            "-1.09011,0.012545,0,-0.003038,0.015583\n" ]
	return outList







