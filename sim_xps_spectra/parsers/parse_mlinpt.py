
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


	fileAsList = [x for x in _readFileIntoList(inpPath) if x.replace(","," ").strip()!=""]
	energies, intensities, labelStrs,  = list(), list(), list()

	#Get all raw values
	mFactor = float( fileAsList[0].replace(","," ").strip().split("=")[-1] )
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


def writeMLInptFileFromPathAndSpecFrags(outPath, specFrags):
	""" Writes a *MLinpt.txt file when given an output file path and an iter of SpectrumFragmentStandard objects
	These files contains energies, intensities and labels for atomic orbitals contributing to a given fragment
	
	Args:
		outPath: (str) Full path to the output file
		specFrags: (iter of SpectrumFragmentStandard objects) These contain energies, intensities and labels for all contributions
 
	Raises:
		 ValueError: If the energies of specFrags differ between each other (The file format assumes the energy values are shared)
	"""
	_checkAllEnergiesConsistentBetweenFragments(specFrags) #Energies need to be the same on all fragments to write the MLinpt file
	outFileAsList = ["# M_FACTOR=1.0\n"]
	outFileAsList.append(_getHeaderStrFromSpecFrags(specFrags))
	outFileAsList.extend(_getDataStrFromSpecFrags(specFrags))
	outStr = "".join(outFileAsList)
	_writeStrToFile(outPath, outStr)

def _getHeaderStrFromSpecFrags(specFrags):
	baseHeader = "# Energy (eV),TDOS,"
	extraHeader = ",".join([x.label.xSectionLabel for x in specFrags])
	return baseHeader + extraHeader + "\n"


def _getDataStrFromSpecFrags(specFrags):
	formatStrs = ["{:.6g}" for x in range( len(specFrags)+2 )]
	allEnergies = specFrags[0].energies #Assume all energies are the same; this will be checked elsewhere
	outStrList = list()
	for idx, energy in enumerate(allEnergies):
		intensities = [x.intensities[idx] for x in specFrags]
		tdos = sum( intensities )
		currLineNumVals = [energy] + [tdos] + intensities
		currStr = ",".join( [fmtStr.format(x) for fmtStr,x in it.zip_longest(formatStrs,currLineNumVals)] ) + "\n"
		outStrList.append(currStr)

	return outStrList

def _checkAllEnergiesConsistentBetweenFragments( specFrags, errorTol=1e-5 ):
	allEnergies = [x.energies for x in specFrags]

	#Check number of energies values is the same
	allLens = [len(x) for x in allEnergies]
	if not all([x==allLens[0] for x in allLens]):
		raise ValueError("Cant write MLInpt.txt file since lengths of energies are different between fragments")

	#Check the values of energies are the same
	for idx in range(len(allEnergies[0])):
		currDiffs = [abs(allEnergies[x][idx] - allEnergies[0][idx]) for x in range( len(allEnergies) )]
		if not all([x<errorTol for x in currDiffs]):
			raise ValueError("Cant write MLInpt.txt file since energies are different between fragments")


#Here so i can mock it
def _writeStrToFile(outPath, outStr):
	with open(outPath,"wt") as f:
		f.write(outStr)





