
import os
import itertools as it

from . import base_objs as baseObjs
from ..shared import config_vars as cfgVars

class YehLindauXSectionDatabase(baseObjs.CrossSectionDatabaseBase):

	def __init__(self, substituteLabelDict=None):
		""" Database class with Yeh and Lindau cross sections taken "from https://vuo.elettra.eu/services/elements/WebElements.html" who in turn list these references:
		
		J.J. Yeh, Atomic Calculation of Photoionization Cross-Sections and Asymmetry Parameters, Gordon and Breach Science Publishers, Langhorne, PE (USA), 1993
		J.J. Yeh and I.Lindau, Atomic Data and Nuclear Data Tables, 32, 1-155 (1985)
		"""
		self._basePath = cfgVars.YEH_LINDAU_DB_PATH
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
		return parseDataFile(inpPath)

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


#TODO: Figure out why we have 3 values for x-sections and asym factors. For C2p the asym factor values differ a bit
def parseDataFile(inpPath):
	fileAsList = _readInpFileIntoList(inpPath)
	xSections, asymVals, hvVals = list(), list(), list()
	for line in fileAsList:
		currData = line.strip().split("\t")
		hvVals.append( float(currData[0]) )
		currXSection = sum([float(x) for x in currData[1:4]])/3
		currAsym = sum([float(x) for x in currData[4:7]])/3
		xSections.append(currXSection)
		asymVals.append(currAsym)
	outDict = {"xSections".lower():[(hv,x) for hv,x in it.zip_longest(hvVals, xSections)],
	           "asymFactors".lower():[(hv,x) for hv,x in it.zip_longest(hvVals,asymVals)]}
	return outDict

#This is here mainly so i can mock it out essentially
def _readInpFileIntoList(inpPath):
	with open(inpPath,"r") as f:
		outList = f.readlines()
	return outList
