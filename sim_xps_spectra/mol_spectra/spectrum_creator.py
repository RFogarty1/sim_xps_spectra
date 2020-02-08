
import copy
import itertools as it
import sim_xps_spectra.gen_spectra.standard_objs as specObjs
import sim_xps_spectra.gen_spectra.get_spectrum as spectrumMaker
import sim_xps_spectra.broad_functs.create_broaden_functs as broadFunctLib
import sim_xps_spectra.x_sections.standard_objs as xSectObjs

class SpectrumCreatorStandard():
	"""Object used to store options for simulating an XPS spectrum

	Attributes:
		spectraFrags : (iter of SpectrumFragmentStandard object) 
		normBFunct: (BroadenFunctionStandard object). This is the broaden function which will be placed around each energy value
		xSectionDatabase: (CrossSectionDatabaseBase object). Can set this to None if not using any cross-sections
		photonEnergy: (float) The photon energy to use; affects which cross-sections are applied. None means no cross-sections applied at all
		emissionAngle: (float) Emission angle of photoelectrons; leave as None if you dont want angular effects included when calculating cross-sections
		xVals: (float iter) List of x-values to evaluate the broadening functions at (i.e. binding energies included in plot)

	"""
	def __init__(self, spectraFrags=None, normBFunct=None,
	             xSectionDatabase=None, photonEnergy=None, emissionAngle=None, xVals=None):

		self.spectraFrags = spectraFrags
		self.normBFunct = normBFunct
		self.xSectionDatabase = xSectionDatabase
		self.photonEnergy = photonEnergy
		self.emissionAngle = emissionAngle
		self.xVals = xVals

		#Check all the required arguments are set
		reqArgs = ["spectraFrags", "normBFunct","xVals"]
		for reqArg in reqArgs:
			if getattr(self,reqArg) is None:
				raise AttributeError("None is an invalid value for reqArg")

		#Check our broadening function has an area of one
		assert len(self.normBFunct.positions)==1, "self.normBFunct should have 1 position, not {}".format( len(self.normBFunct.positions) )
		assert abs(self.normBFunct.areas[0] - 1.0)<1e-5, "self.normBFunct should have an area of 1.0, not {}".format(self.normBFunct)


class SpectrumFragmentStandard():
	"""Object represents contribution of one atomic orbital on one fragment (e.g. the Anionic C2s contribution)

	Attributes:
		energies: (float iter) Energy of each transition
		intensities: (float iter) Areas applied to broadening functions around each energy (these are intensities BEFORE the relevant cross-section has been applied)
		label: (MolFragLabel object) Contains strs used to identify this fragment (i.e. the name of the fragment its part of and the atomic orbital it is)

	"""

	def __init__(self,energies, intensities, label):
		self._eqTol = 1e-5
		self.energies = energies
		self.intensities = intensities
		assert len(energies)==len(intensities), "Need an intensity for each energy; have {} energies and {} intensities".format(len(energies),len(intensities))
		self.label = label

	def __eq__(self, other):
		eqTol = max(self._eqTol, other._eqTol)

		#Compare energies
		if len(self.energies) != len(other.energies):
			return False
		eDiffs = [abs(x-y) for x,y in zip(self.energies,other.energies)]
		if not all([x < eqTol for x in eDiffs]):
			return False

		#compare intensities
		if len(self.intensities) != len(other.intensities):
			return False
		iDiffs = [abs(x-y) for x,y in zip(self.intensities,other.intensities)]
		if not all([x < eqTol for x in iDiffs]):
			return False

		#compare labels
		if self.label != other.label:
			return False

		return True


def createSpectrumFromStandardCreator( specCreator ):
	#Step 1 is to create a list of broadening functions
	allBroadFuncts = list()
	for x in specCreator.spectraFrags:
		currBFunct = _getBroadenFunctFromSpecFragAndNormBroadFunct(x, specCreator.normBFunct)
		allBroadFuncts.append(currBFunct)

	#Step 2 is to multiply the intensities on each fragment by their cross-section. And make sure we use the same hv for each
	allHvUsed = _getAllHvUsedForSpecCreator( specCreator )
	allXSections = _getAllXSectionsForSpecCreator( specCreator )

	#We need to check we used the same hv in all cases
	hvDiffs = [abs(x-allHvUsed[0]) for x in allHvUsed]
	assert all([x<0.01 for x in hvDiffs]), "All hv values need to be the same, which was not possible for input photon energy {}".format(specCreator.photonEnergy)
	if specCreator.photonEnergy is not None:
		specCreator.photonEnergy = allHvUsed[0] #So we have some way of knowing what photon energy was ACTUALLY used	

	#Now we modify the newly created broadening functions
	for bFunct,xSect in it.zip_longest(allBroadFuncts,allXSections):
		startIntensities = bFunct.areas
		bFunct.areas = [x*xSect for x in startIntensities] 

	#Step 3 is simply to create the spectrum
	inpObjs = list()
	for specFrag,bFunct in it.zip_longest(specCreator.spectraFrags, allBroadFuncts):
		currObj = specObjs.GenSpectraInputStandard(  bFunct, specFrag.label )
		inpObjs.append(currObj)
 
	specInp = specObjs.GenSpectraInputCompositeStandard(inpObjs)
	outSpectraObj = spectrumMaker.getSpectrumFromApplyingBroadeningFuncts(specCreator.xVals, specInp)

	return outSpectraObj	


def _getBroadenFunctFromSpecFragAndNormBroadFunct(specFrag, normBFunct):
	allBFuncts = list()
	for energy,intensity in it.zip_longest(specFrag.energies, specFrag.intensities):
		bFunct = copy.deepcopy(normBFunct)
		bFunct.positions = [energy]
		bFunct.areas = [intensity]
		allBFuncts.append(bFunct)

	return broadFunctLib.BroadenFunctCompositeStandard( allBFuncts )


def _getAllHvUsedForSpecCreator( specCreator ):
	xSectCalculator = xSectObjs.CrossSectionCalculatorStandard( specCreator.xSectionDatabase )

	if specCreator.photonEnergy is None:
		allHvUsed = [-1.0 for x in specCreator.spectraFrags]
	else:
		allHvUsed = list()
		for x in specCreator.spectraFrags:
			currHv = xSectCalculator.getHvUsedToCalculateCrossSection(x.label.xSectionLabel, specCreator.photonEnergy, angle=specCreator.emissionAngle, ao=True )
			allHvUsed.append(currHv)

	return allHvUsed


def _getAllXSectionsForSpecCreator( specCreator ):
	xSectCalculator = xSectObjs.CrossSectionCalculatorStandard( specCreator.xSectionDatabase )

	if specCreator.photonEnergy is None:
		allXSections = [1.0 for x in specCreator.spectraFrags]
	else:
		allXSections = list()
		for x in specCreator.spectraFrags:
			currXSection = xSectCalculator.calculateTotalCrossSection(x.label.xSectionLabel, specCreator.photonEnergy, angle=specCreator.emissionAngle, ao=True )
			allXSections.append(currXSection)

	return allXSections

