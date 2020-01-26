
import itertools as it

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
