

import itertools as it
import unittest
import unittest.mock as mock

import sim_xps_spectra.x_sections.yeh_lindau_db as tCode

class TestYehLindauDatabase(unittest.TestCase):

	def setUp(self):
		self.hvVals = [20,30]
		self.xSections = [ 50.5, 70.6]
		self.asymFactors = [12, 13]
		self.createFileAsList()

	def createFileAsList(self):
		self.fileAsListA = list()
		self.fileAsListA.append("#Here is a comment line")
		for hv, xSect, asym in it.zip_longest(self.hvVals, self.xSections, self.asymFactors):
			currStr = "\t".join( [str(x) for x in [hv, xSect, xSect, xSect, asym, asym, asym]] )
			currStr += "\n"
			self.fileAsListA.append(currStr)

	@mock.patch("sim_xps_spectra.x_sections.yeh_lindau_db._readInpFileIntoList")
	def testParseFileWorks(self,parseMock):
		parseMock.return_value = self.fileAsListA
		expParsedData = {"xSections".lower(): [(hv,val) for hv,val in it.zip_longest(self.hvVals, self.xSections)],
		                 "asymFactors".lower(): [(hv,val) for hv,val in it.zip_longest(self.hvVals, self.asymFactors)]}
		actParsedData = tCode.parseDataFile("fake_inp_path")
		for key in expParsedData:
			currExpData, currActData = expParsedData[key], actParsedData[key]
			for exp,act in it.zip_longest(currExpData, currActData):
				self.assertAlmostEqual(exp[0],act[0]) #photon energy
				self.assertAlmostEqual(exp[1],act[1]) #xSection or asym factor



#def _getTestFileStrA(inpPath):
#	return None
