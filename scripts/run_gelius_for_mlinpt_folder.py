

import argparse
import itertools as it
import os
import pathlib

import sim_xps_spectra.interfaces.create_from_mlinpt_folder as mlInptInter
import sim_xps_spectra.mol_spectra.input_output as molIO
import sim_xps_spectra.mol_spectra.standard_objs as molObjs
import sim_xps_spectra.mol_spectra.mol_plotter as molPlot
import sim_xps_spectra.gen_spectra.standard_objs as genSpecObjs


def main():
	argsNamespace = parseCmdLineArgs()
	argsNamespace.folderPaths = [os.path.abspath(x) for x in argsNamespace.folderPaths]

	#Create the spectra
	allCalcSpectra, allCreators = list(), list()
	for inpPath in argsNamespace.folderPaths:
		currSpectrum, currCreator = getCalcSpectraForOneFolder( os.path.abspath(inpPath), argsNamespace.fwhm, argsNamespace.hv, argsNamespace.angle, argsNamespace.polarised )
		allCalcSpectra.append( currSpectrum )
		allCreators.append( currCreator )

	#save the outputs
	for inpPath, creator, spectrum in it.zip_longest( argsNamespace.folderPaths, allCreators, allCalcSpectra ):
		saveAllTxtFilesOneFolder(inpPath, creator, argsNamespace.fwhm, spectrum)
		saveAllPlotsOneFolder(inpPath, creator, argsNamespace.fwhm, spectrum)

def parseCmdLineArgs():
	helpMsg = "Script to simulate combined XPS spectrum of *MLinpt.txt files in given folder"
	parser = argparse.ArgumentParser(description = helpMsg)
	parser.add_argument( "folderPaths", nargs='*', help='Paths to folders you want to run the script on (relative or abs both fine)') 
	parser.add_argument( "-fwhm", help='The full-width at half maximum of the broadening function to use', required=True )
	parser.add_argument( "-hv", help='The photon energy you want the spectrum simulated at. If not provided then a density-of-states will be simulated' )
	parser.add_argument( "-angle", help='Emission angle (in degrees) you want the spectrum simulated at, if not provided then angular effects will be ignored')
	parser.add_argument( "-polarised", help='Polarisation of light. Not entering means unpolarised, "linear" means polarised in direction of the beam')
	parsedArgs = parser.parse_args()

	parsedArgs.fwhm = float(parsedArgs.fwhm)
	parsedArgs.hv = None if parsedArgs.hv is None else float(parsedArgs.hv)
	parsedArgs.angle = None if parsedArgs.angle is None else float(parsedArgs.angle)
	parsedArgs.polarised = None if parsedArgs.polarised is None else str(parsedArgs.polarised)

	return parsedArgs

def getCalcSpectraForOneFolder(inpFolder, fwhm, hv, angle, polarised):
	return mlInptInter.getSpectrumFromMlinptFolder(inpFolder, fwhm, hv, angle, polarised)

def saveAllPlotsOneFolder(inpFolder, creatorObj, fwhm, calcSpectrum):
	folderPath = os.path.join( inpFolder, getSaveFolderNameFromCreator(creatorObj, fwhm) )
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


def saveAllTxtFilesOneFolder(inpFolder, creatorObj, fwhm, calcSpectrum):
	folderPath = os.path.join( inpFolder, getSaveFolderNameFromCreator(creatorObj, fwhm) )
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

def getSaveFolderNameFromCreator(specCreator, fwhm):
	fmt = "hv_{}_angle_{}_pol_{}_fwhm_{}"
	hvVal = "None" if specCreator.photonEnergy is None else  ( "{:.2f}".format(specCreator.photonEnergy)  ).replace(".","pt")
	angle = "None" if specCreator.emissionAngle is None else ( "{:.2f}".format(specCreator.emissionAngle) ).replace(".","pt")
	pol   = "None" if specCreator.polarised    is None else str(specCreator.polarised)
	fwhmStr = ("{:.2f}".format(fwhm)).replace(".","pt")
	return fmt.format(hvVal, angle, pol, fwhmStr)

if __name__ == '__main__':
	main()

