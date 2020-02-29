

import argparse
import copy
import itertools as it
import os
import pathlib

#Import databases. TODO: Centralise the str to database mapping; so i can just import a database register
import sim_xps_spectra.x_sections.yeh_lindau_db as yhlDb
import sim_xps_spectra.x_sections.trz_db as trzDb

import sim_xps_spectra.interfaces.create_from_mlinpt_folder as mlInptInter
import sim_xps_spectra.mol_spectra.input_output as molIO
import sim_xps_spectra.mol_spectra.standard_objs as molObjs
import sim_xps_spectra.mol_spectra.mol_plotter as molPlot
import sim_xps_spectra.gen_spectra.standard_objs as genSpecObjs

import sim_xps_spectra.shared.searchable_collection as searchHelp
import sim_xps_spectra.parsers.parse_mlinpt as parseMlInpt
import sim_xps_spectra.mol_spectra.spectrum_creator as specCreator

def main():
	argsNamespace = parseCmdLineArgs()
	argsNamespace.folderPaths = [os.path.abspath(x) for x in argsNamespace.folderPaths]

	#Create the spectra
	database = _getDatabaseObjFromStr(argsNamespace.database)
	allCalcSpectra, allCreators = list(), list()
	for inpPath in argsNamespace.folderPaths:
		currSpectrum, currCreator = getCalcSpectraForOneFolder( os.path.abspath(inpPath), argsNamespace.fwhm, argsNamespace.hv,
		                                                        argsNamespace.angle, argsNamespace.polarised, database )
		allCalcSpectra.append( currSpectrum )
		allCreators.append( currCreator )

	#save the outputs
	for inpPath, creator, spectrum in it.zip_longest( argsNamespace.folderPaths, allCreators, allCalcSpectra ):
		saveAllTxtFilesOneFolder(inpPath, creator, argsNamespace.fwhm, argsNamespace.database, spectrum)
		saveAllPlotsOneFolder(inpPath, creator, argsNamespace.fwhm, argsNamespace.database, spectrum)
		saveAllMLInptOneFolder(inpPath, creator, argsNamespace.fwhm, argsNamespace.database)

def parseCmdLineArgs():
	helpMsg = "Script to simulate combined XPS spectrum of *MLinpt.txt files in given folder"
	parser = argparse.ArgumentParser(description = helpMsg)
	parser.add_argument( "folderPaths", nargs='*', help='Paths to folders you want to run the script on (relative or abs both fine)') 
	parser.add_argument( "-fwhm", help='The full-width at half maximum of the broadening function to use', required=True )
	parser.add_argument( "-hv", help='The photon energy you want the spectrum simulated at. If not provided then a density-of-states will be simulated' )
	parser.add_argument( "-angle", help='Emission angle (in degrees) you want the spectrum simulated at, if not provided then angular effects will be ignored')
	parser.add_argument( "-polarised", help='Polarisation of light. Not entering means unpolarised, "linear" means polarised in direction of the beam')
	parser.add_argument( "-database", help='Str(case insenstive) denoting database to use for obtaining cross-sections and asymmetry factors. Default is Yeh-Lindau cross sections. Options are "yhl" or "trz" currently') 
	parsedArgs = parser.parse_args()

	parsedArgs.fwhm = float(parsedArgs.fwhm)
	parsedArgs.hv = None if parsedArgs.hv is None else float(parsedArgs.hv)
	parsedArgs.angle = None if parsedArgs.angle is None else float(parsedArgs.angle)
	parsedArgs.polarised = None if parsedArgs.polarised is None else str(parsedArgs.polarised)
	parsedArgs.database = 'yhl' if parsedArgs.database is None else str(parsedArgs.database)

	return parsedArgs


def _getDatabaseObjFromStr(inpStr):
	strToFunct = {"yhl":yhlDb.YehLindauXSectionDatabase,
	              "trz":trzDb.TrzXSectionDatabase}
	databaseCreator = strToFunct[inpStr.lower()]
	return databaseCreator()

def getCalcSpectraForOneFolder(inpFolder, fwhm, hv, angle, polarised, database):
	return mlInptInter.getSpectrumFromMlinptFolder(inpFolder, fwhm, hv, angle, polarised, database=database)

def saveAllPlotsOneFolder(inpFolder, creatorObj, fwhm, databaseAlias, calcSpectrum):
	folderPath = os.path.join( inpFolder, getSaveFolderNameFromCreator(creatorObj, fwhm, databaseAlias) )
	pathlib.Path(folderPath).mkdir(exist_ok=True)

	#Save plot for total spectrum
	totalSpecPlot = molPlot.getTotalContribsPlotFromSpectraOutput( calcSpectrum )
	totalSpecPlot.savefig( os.path.join(folderPath,"total_spectrum.eps"), format="eps" )
	totalSpecPlot.savefig( os.path.join(folderPath,"total_spectrum.png"), format="png" )

	#Save plot for fragment contribs
	fragContribSpectrum = _getMergedFragCalcSpectraObj( calcSpectrum )
	fragSpecPlot = molPlot.getAllContribsPlotFromSpectraOutput( fragContribSpectrum )
	fragSpecPlot.savefig( os.path.join(folderPath,"frag_contribs.eps"), format="eps" )
	fragSpecPlot.savefig( os.path.join(folderPath,"frag_contribs.png"), format="png" )


def saveAllTxtFilesOneFolder(inpFolder, creatorObj, fwhm, databaseAlias, calcSpectrum):
	folderPath = os.path.join( inpFolder, getSaveFolderNameFromCreator(creatorObj, fwhm, databaseAlias) )
	pathlib.Path(folderPath).mkdir(exist_ok=True)

	#Write the total spectrum file
	totalSpecStr = molIO.getTotalContribStrFromSpectraOutput( calcSpectrum )
	with open( os.path.join(folderPath,"total_spectrum.txt"),"wt" ) as f:
		f.write(totalSpecStr)	

	#Write file with ALL contributions
	allContribsStr = molIO.getAllContribsOutputStrFromSpectraOutput( calcSpectrum )
	with open( os.path.join(folderPath,"all_contribs.txt"),"wt" ) as f:
		f.write(allContribsStr)

	#Write the fragment contribs
	fragContribSpectrum = _getMergedFragCalcSpectraObj( calcSpectrum )
	fragContribStr = molIO.getAllContribsOutputStrFromSpectraOutput( fragContribSpectrum )
	with open( os.path.join(folderPath, "frag_contribs.txt"), "wt" ) as f:
		f.write(fragContribStr)


def saveAllMLInptOneFolder(inpFolder, creatorObj, fwhm, databaseAlias):
	searchCol = searchHelp.SearchableCollection(creatorObj.spectraFrags)
	allFragNames = searchCol.getAllValsForComponent("fragKey")
	outSaveFolder = getSaveFolderNameFromCreator(creatorObj, fwhm, databaseAlias)

	for fName in allFragNames:
		outFilePath = os.path.join(outSaveFolder, fName + "_output_MLinpt.txt")
		currFragments = copy.deepcopy(searchCol.getObjectsWithComponents([fName]))
		for frag in currFragments:
			frag.energies = [-1*x for x in frag.energies]
			specCreator.applyCrossSectionsToFragmentObjectAndReturnHvUsed(frag, creatorObj)
		parseMlInpt.writeMLInptFileFromPathAndSpecFrags(outFilePath,currFragments)

def _getMergedFragCalcSpectraObj( calcSpecOutput ):
	""" For a calcSpectrum with fragA and fragB, all atomic contribs will be merged within fragA and fragB (NOT in place), 
	    and the object will look like one with atomic orbital contributions just from fragA and fragB. Useful for getting
	    fragment contributions
	"""
	allFrags = set([x.fragKey for x in calcSpecOutput.label])
	allCalcSpecObjs = list()
	for fragKey in sorted(allFrags):
		currCalcSpectra = genSpecObjs.GenSpectraOutputCompositeStandard( calcSpecOutput.getObjectsWithComponents([fragKey], caseSensitive=True, partialMatch=False) )
		currData = currCalcSpectra.totalSpectralContributions
		currLabel = molObjs.MolFragLabel( fragKey=fragKey,eleKey="None",aoKey="None" )
		allCalcSpecObjs.append( genSpecObjs.GenSpectraOutputStandard( currData, currLabel) )

	return genSpecObjs.GenSpectraOutputCompositeStandard( allCalcSpecObjs )

def getSaveFolderNameFromCreator(specCreator, fwhm, databaseAlias):
	fmt = "hv_{}_angle_{}_pol_{}_fwhm_{}_db_{}"
	hvVal = "None" if specCreator.photonEnergy is None else  ( "{:.2f}".format(specCreator.photonEnergy)  ).replace(".","pt")
	angle = "None" if specCreator.emissionAngle is None else ( "{:.2f}".format(specCreator.emissionAngle) ).replace(".","pt")
	pol   = "None" if specCreator.polarised    is None else str(specCreator.polarised)
	db = databaseAlias
	fwhmStr = ("{:.2f}".format(fwhm)).replace(".","pt")
	return fmt.format(hvVal, angle, pol, fwhmStr, db)

if __name__ == '__main__':
	main()

