
import math
from . import base_objs as baseObjs


class CrossSectionCalculatorStandard(baseObjs.CrossSectionCalculatorBase):

	def __init__(self, database):
		""" Initialiser
		
		Args:
			database: (CrossSectionDatabaseBase interface) Used to get photon energies ve cross-sections/asym factors
		"""
		self.database = database


	#Formula from http://dx.doi.org/10.1016/j.molliq.2014.01.007
	def calculateTotalCrossSection(self,label, hv, angle=None, ao=True, pol=None):

		if ao is True:
			aoData = self.database.getHvAgainstAOCrossSections(label)
			aoHv, aoIdx = self._getHvUsedAndIndex(hv, aoData)
			angularIndependent = aoData[aoIdx][1]
		else:
			angularIndependent = 1

		if angle is not None:
			asymData = self.database.getHvAgainstAOAsymFactors(label)
			asymHv, asymIdx = self._getHvUsedAndIndex(hv, asymData)
			angleFactor = self._calcAngularDependentTermFromAsymAndAngle( asymData[asymIdx][1], angle, pol )
			angularDependent = angleFactor*angularIndependent
		else:
			angularDependent = 0 

		#Need to check we used the same hv value for both
		if (angle is not None) and (ao is True):
			assert abs(aoHv-asymHv)<0.01, "Photon energy must be the same for asymetry factor and ao cross section, aoHv={}, asymHv = {}".format(aoHv, asymHv)


		return angularIndependent + angularDependent

	def getHvUsedToCalculateCrossSection(self,label, hv, angle=None, ao=True):
		if (angle is None) and (ao is False):
			return None #Should never be called this way but... 

		if ao is True:
			aoData = self.database.getHvAgainstAOCrossSections(label)
			aoHv,Index = self._getHvUsedAndIndex(hv,aoData)
			hvUsed = aoHv


		if angle is not None:
			asymData = self.database.getHvAgainstAOAsymFactors(label)
			asymHv, unused = self._getHvUsedAndIndex(hv, asymData)
			hvUsed = asymHv

		#Need to make sure we're consistent if looking up both asym param AND ao param
		if (angle is not None) and (ao is True):
			assert abs(aoHv-asymHv)<0.01, "Photon energy must be the same for asymetry factor and ao cross section, aoHv={}, asymHv = {}".format(aoHv, asymHv)

		return hvUsed

	def _getHvUsedAndIndex(self, hv, xSectionData):
		photonEnergies = [x[0] for x in xSectionData]
		absDiffs = [abs(x-hv) for x in photonEnergies]
		idx, unused = min( enumerate(absDiffs), key=lambda x:x[1] )
		hv = photonEnergies[idx]
		return (hv,idx)

	def _calcAngularDependentTermFromAsymAndAngle(self, asymParam, angle, polarisation):
		if polarisation is None:
			return self._calcAngularDepNonPolarisedTerm(asymParam, angle)
		elif polarisation.lower() == "linear":
			return self._calcAngularDepLinearPolarisedTerm(asymParam, angle)
		else:
			raise ValueError("{} is an invalid value for polarisation".format(polarisation))


	def _calcAngularDepNonPolarisedTerm(self, asymParam, angle):
		""" Non-polarised light expression from https://doi.org/10.1006/adnd.2000.0849   [-\Beta/2 P_2(cos(\Theta))]"""
		prefactor = -1 * (asymParam / 2)
		p2Term = self._calcP2Term(asymParam,angle)
		total = prefactor * p2Term #DegreesTerm - 1 is P2(cos Theta), where P2 means 2nd Legendre polynomial
		return total
	
	def _calcAngularDepLinearPolarisedTerm(self, asymParam, angle):
		""" Linearly polarised light expression from https://doi.org/10.1006/adnd.2000.0849 """
		p2Term = self._calcP2Term(asymParam,angle)
		return asymParam*p2Term

	def _calcP2Term(self, asymParam, angle):
		return 0.5 * ( ( 3* ( math.cos( math.radians(angle) )**2 )) - 1 ) #0.5(3x^2 - 1)
