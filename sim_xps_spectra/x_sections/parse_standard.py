
import itertools as it

""" Code to define a parser for a standard format of cross-section input files. This format does NOT HAVE to be used for a database """



def parseStandardXSectionDatabaseFile(inpPath):
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

