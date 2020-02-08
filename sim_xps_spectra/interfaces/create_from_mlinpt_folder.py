
import os
import numpy as np

import sim_xps_spectra.parsers.parse_mlinpt as parseMlinpt
import sim_xps_spectra.broad_functs.create_broaden_functs as bFunctCreator
import sim_xps_spectra.mol_spectra.spectrum_creator as specCreatorModule
import sim_xps_spectra.x_sections.yeh_lindau_db as yhDb

def getSpectrumFromMlinptFolder(inpFolder, fwhm, hv, angle, multEnergiesByMinusOne=True):
	""" Description of function
	
	Args:
		inpFolder: (str) Path to folder containing *MLinpt.txt files
		fwhm: (float) Full-Width at half maximum for the broadening function
		hv: (float) Photon energy to calculate spectrum at (None means density-of-states)
		angle: (float) Emission angle to calculate spectrum at (None means ignore angular effects)
		multEnergiesByMinusOne: (Bool) Whether to multiply parsed energies by -1, to convert from eigenvalues(more -ve means more stable) to binding energies (more positive is more stable). Default is True
 
	Returns
		outSpectrum: (GenSpectraOutput object) - contains total spectrum (totalSpectraContributions) and all contributions (spectraContributions)
		specCreator: (SpectrumCreatorStandard object) - contains all options used to create spectrum
 
	"""
	mlInptPaths = [x for x in os.listdir(inpFolder) if x.endswith('MLinpt.txt')]
	assert len(mlInptPaths) > 0, "Need at least 1 input file, but none found in folder {}".format(inpFolder)

	return getSpectrumFromMlinptFileList( mlInptPaths, fwhm, hv, angle )


def getSpectrumFromMlinptFileList( mlInptPaths, fwhm, hv, angle, multEnergiesByMinusOne=True ):
	#Get all the data
	allFrags = list()
	for x in mlInptPaths:
		allFrags.extend( parseMlinpt.getSpecFragsFromMLInptFile(x) )

	#Convert from eigenvalues to XPS binding energies
	if multEnergiesByMinusOne:
		for x in allFrags:
			x.energies = [a*-1 for a in x.energies]

	#Figure out sensible x-values to use (may allow them to be specified later)
	maxAbsMoEnergy = 50 #Arbitrary, but helps remove the core states from the calculate spectrum. WIll allow it to be set later
	allEnergies = list()
	for x in allFrags:
		allEnergies.extend( x.energies )
	filteredEnergies = [x for x in allEnergies if abs(x) < maxAbsMoEnergy]
	maxE,minE = max(filteredEnergies) + (3*fwhm), min(filteredEnergies) - (3*fwhm)

	#Ensure we pass through zero
	if (maxE < 0) and (minE < 0):
		maxE = 0.0
	elif (maxE > 0) and (minE > 0):
		minE = 0.0

	stepSize = 0.01

	xVals = list( np.arange(minE,maxE,stepSize) )

	#Define the broadening function to use (gaussian only at the moment)
	initialPosition = 0.0 #Irrelevant but we need to supply SOME kind of value
	bFunct = bFunctCreator.createNormalisedGauFunctFromCentreAndFWHM( initialPosition, fwhm )

	xSectDatabase = yhDb.YehLindauXSectionDatabase()

	#Create our input object
	specCreator = specCreatorModule.SpectrumCreatorStandard( spectraFrags=allFrags, normBFunct=bFunct, xSectionDatabase=xSectDatabase,
	                                                         photonEnergy=hv, emissionAngle=angle, xVals=xVals )

	#Create the output spectrum and return it
	outputSpectrum = specCreatorModule.createSpectrumFromStandardCreator( specCreator )

	return outputSpectrum, specCreator


