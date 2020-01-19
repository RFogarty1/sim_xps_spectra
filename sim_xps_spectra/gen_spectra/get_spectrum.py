
import itertools as it

from . import standard_objs as standardObjs


def getSpectrumFromApplyingBroadeningFuncts(xVals, genSpectInpObj):
	""" Applies broadening function to all components and outputs an object representing final x vs y spectrum
	
	Args:
	 	xVals: (iter) of values to evalaute broadening functions at. (e.g xVals = [1,2,3,4])
		genSpectraInpObj: (GenSpectraInput object) See base_objs or standard_objs for this part of the code. Object contains information to calculate spectra contributions at each x-value
			 
	Returns
		 genSpectraOuputObj: (GenSpectraInputCompositeStandard) Object for holding results of spectrum generation, including info. to get breakdowns into various elements or fragments. totalSpectraContributions property will give x vs y data for the calculated spectrum; see standard_objs.py in this part of the code for details on how to get more info out.
 
	"""

	#Get all data and labels in the correct order
	allYVals = genSpectInpObj.calculateSpectralContribs(xVals)
	allContribs = list()
	for yVals in allYVals:
		currData = [(x,y) for x,y in it.zip_longest(xVals,yVals)]
		allContribs.append(currData)

	allLabels = genSpectInpObj.label

	#Create output objects
	allOutObjs = list()
	for data,label in it.zip_longest(allContribs, allLabels):
		currObj = standardObjs.GenSpectraOutputStandard(data, label)
		allOutObjs.append(currObj)

	compositeOutObj = standardObjs.GenSpectraOutputCompositeStandard(allOutObjs)

	return compositeOutObj

