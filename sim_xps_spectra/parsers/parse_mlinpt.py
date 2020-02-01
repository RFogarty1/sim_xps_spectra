
import itertools as it
import os
import re
import sim_xps_spectra.mol_spectra.standard_objs as molObjs
import sim_xps_spectra.mol_spectra.spectrum_creator as specCreate


def getSpecFragsFromMLInptFile(inpPath, fragName=None):
	""" Takes an *MLinpt.txt file and extracts a list of SpectrumFragmentStandard objects
	
	Args:
		inpPath: (str) full path to the input file
		fragName: (str, Optional) The name you want to call this fragment; If None it will be taken from the input file name
			 
	Returns
		outFrags: (iter of SpectrumFragmentStandard objects) contain energies, intensities and labels for each component 
 
	"""

	#Figure out the fragment name
	if fragName is None:
		fragName = os.path.split(inpPath)[-1].replace("_MLinpt.txt","")


	fileAsList = [x for x in _readFileIntoList(inpPath) if x.strip()!=""]
	energies, intensities, labelStrs,  = list(), list(), list()

	#Get all raw values
	mFactor = float( fileAsList[0].strip().split("=")[-1] )
	labels = [x for x in fileAsList[1].strip().split(",") if ("energy (ev)" not in x.lower()) and ("tdos" not in x.lower()) ]
	energies, intensities = list(), list()

	for line in fileAsList[2:]:
		allVals = [float(x) for x in line.strip().split(",")]
		energies.append( allVals[0] )
		intensities.append( allVals[2:] )

	#Modify intensities if needed. Note intensities in 1 per ENERGY at the moment, which is sorta anoying
	for idx,intensityList in enumerate(intensities):
		intensities[idx] = [x*mFactor for x in intensityList]

	#Get label objects from label strings
	labelObjs = list()
	for lStr in labels:
		eleKey = re.findall("^[A-Z,a-z]+", lStr.strip())
		aoKey = re.findall("[0-9][A-Z,a-z]+", lStr.strip())
		assert len(eleKey)==1 and len(aoKey)==1, "Need labels of the form EleAo, e.g C2s or Si2p, {} is invalid".format(lStr)
		labelObjs.append( molObjs.MolFragLabel(fragKey=fragName, eleKey=eleKey[0], aoKey=aoKey[0]) )

	#Create all the output objects
	allFrags = list()
	for idx, label in enumerate(labelObjs):
		currIntensities = [x[idx] for x in intensities]
		allFrags.append( specCreate.SpectrumFragmentStandard(list(energies), currIntensities, label) )	

	return allFrags

def _readFileIntoList(inpPath):
	with open(inpPath) as f:
		outList = f.readlines()
	return outList

