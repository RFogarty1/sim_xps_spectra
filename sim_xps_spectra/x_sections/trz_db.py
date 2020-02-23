
""" Database for cross-sections taken from https://doi.org/10.1006/adnd.2000.0849 """
#TODO: Remove some duplication from the yeh-lindau stuff
import os
import itertools as it
from . import base_objs as baseObjs
from . import parse_standard as parser
from ..shared import config_vars as cfgVars

class TrzXSectionDatabase(baseObjs.CrossSectionDatabaseBase):

	def __init__(self, substituteLabelDict=None):
		""" Database for cross-sections taken from https://doi.org/10.1006/adnd.2000.0849 """
		self._basePath = cfgVars.TRZ_DB_PATH
		if substituteLabelDict is None:
			self._subLabelDict = createSubstituteLabelDict()
		else:
			self._subLabelDict = substituteLabelDict

	def getHvAgainstAOCrossSections(self, label):
		label = self._getConvertedLabel(label)
		parsedFile = self._parseFileForLabel(label)
		return parsedFile["xSections".lower()]

	def getHvAgainstAOAsymFactors(self, label):
		label = self._getConvertedLabel(label)
		parsedFile = self._parseFileForLabel(label)
		return parsedFile["asymFactors".lower()]

	def _getConvertedLabel(self,label):
		return self._subLabelDict.get(label, label) #returns input label if its not one that needs substituting


	def _parseFileForLabel(self, label):
		inpPath = self._getPathForLabel(label)
		return parser.parseStandardXSectionDatabaseFile(inpPath)

	def _getPathForLabel(self, label):
		inpPath = os.path.join(self._basePath, label.upper())
		return inpPath + ".txt"



#This is to make up for the fact that we use polarization functions in our basis set that we cant get an x-section for
def createSubstituteLabelDict():
	outDict = {"CL3D":"CL3P",
	           "C2D":"C2P",
	           "N2D":"N2P",
	           "S3D":"S3P",
	           "F2D":"F2P",
	           "O2D":"O2P",
	           "P3D":"P3P",
	           "B2D":"B2P"}
	return outDict	


def _parseTrzDataFile(inpPath):
	#Get the data in a sensible format
	fileAsList = [x for x in _readInpFileIntoList(inpPath) if "#" not in x]
	fileAsList = [x for x in fileAsList if x.strip()!=""] #Removing blank lines imperfectly
	xSections, asymVals, hvVals = list(), list(), list()

	for line in fileAsList:
		splitData = line.strip().split(",")
		assert len(splitData) == 3, "{} is an invalid line in cross section file {}".format(line, inpPath)
		hvVals.append( float(splitData[0]) )
		xSections.append( float(splitData[1]) )
		asymVals.append( float(splitData[2]) )
		

	outDict = {"xSections".lower():[(hv,x) for hv,x in it.zip_longest(hvVals, xSections)],
	           "asymFactors".lower():[(hv,x) for hv,x in it.zip_longest(hvVals,asymVals)]}

	return outDict


#This is here mainly so i can mock it out essentially
def _readInpFileIntoList(inpPath):
	with open(inpPath,"r") as f:
		outList = f.readlines()
	return outList

