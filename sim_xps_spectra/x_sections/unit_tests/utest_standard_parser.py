
import itertools as it

import unittest
import unittest.mock as mock

import sim_xps_spectra.x_sections.parse_standard as tCode


class TestStandardParser(unittest.TestCase):

	def setUp(self):
		self.hvVals = [20,30]
		self.xSections = [20.5, 70.3]
		self.asymFactors = [2,4]
		self.createFileAsList()


	def createFileAsList(self):
		self.fileAsListA = ["#Any comment string is fine\n"]
		for hv,xSect,asym in it.zip_longest(self.hvVals, self.xSections, self.asymFactors):
			currStr = ",".join( [str(x) for x in [hv,xSect,asym]] )
			currStr += "\n"
			self.fileAsListA.append(currStr)

	@mock.patch("sim_xps_spectra.x_sections.parse_standard._readInpFileIntoList")
	def testParsingDataFile(self,parseMock):
		parseMock.return_value = self.fileAsListA
		expParsedData = {"xSections".lower(): [(hv,val) for hv,val in it.zip_longest(self.hvVals, self.xSections)],
		                 "asymFactors".lower(): [(hv,val) for hv,val in it.zip_longest(self.hvVals, self.asymFactors)]}
		actParsedData = tCode.parseStandardXSectionDatabaseFile("fake_inp_path")
		for key in expParsedData:
			currExpData, currActData = expParsedData[key], actParsedData[key]
			for exp,act in it.zip_longest(currExpData, currActData):
				self.assertAlmostEqual(exp[0],act[0]) #photon energy
				self.assertAlmostEqual(exp[1],act[1]) #xSection or asym factor


