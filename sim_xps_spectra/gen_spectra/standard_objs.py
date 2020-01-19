
import numpy as np
import gen_basis_helpers.shared.misc_utils as misc
from . import base_objs as baseObjs

""" Concrete implementations of the standard classes used in this part of the code """


class GenSpectraInputCompositeStandard( baseObjs.GenSpectraInput ):
	
	label = misc.StandardComponentDescriptor("label")

	@misc.getAssertAllLabelsUniqueUponCreationClassInitializerWrapper()
	@misc.getObjectsWithComponentsInstanceWrapper(isComposite=True)
	def __init__(self, objs):
		self.objs = list(objs)

	def calculateSpectralContribs(self,xVals):
		outVals = list()
		for obj in self.objs:
			currContribs = obj.calculateSpectralContribs(xVals)
			outVals.extend(currContribs)
		return outVals


class GenSpectraInputStandard( baseObjs.GenSpectraInput ):

	@misc.getObjectsWithComponentsInstanceWrapper(isComposite=False)	
	def __init__(self, fx, label):
		""" Initializer
		
		Args:
			fx: function with interface funct(xVals:iter)->yVals:iter. i.e. take an iterable(e.g. list) of x-values and return an iterable of y-values
			label: BaseLabel object, with components used to fully define the fragment
	 
		"""
		self._spectFunct = fx
		self._label = label


	def calculateSpectralContribs(self,xVals):
		return [self._spectFunct(xVals)]

	@property
	def label(self):
		return [self._label]

class GenSpectraOutputCompositeStandard( baseObjs.GenSpectraOutput):

	label = misc.StandardComponentDescriptor("label")
	spectralContributions = misc.StandardComponentDescriptor("spectralContributions")

	@misc.getAssertAllLabelsUniqueUponCreationClassInitializerWrapper()
	@misc.getObjectsWithComponentsInstanceWrapper(isComposite=True)
	def __init__(self, objs):
		self.objs = list(objs)


	#Possibily a good candidate for caching if speed turns out to be an issue
	@property
	def totalSpectralContributions(self):
		allContribs = [np.array(x) for x in self.spectralContributions]
		startArray = allContribs[0]
		for x in allContribs[1:]:
			startArray[:,1] += x[:,1]
		return [(a,b) for a,b in startArray]


class GenSpectraOutputStandard( baseObjs.GenSpectraOutput ):

	@misc.getObjectsWithComponentsInstanceWrapper(isComposite=False)
	def __init__(self, data, label):
		""" Initializer
		
		Args:
			data: iter(xData,yData) object. If np.array(data) is applied you get an nx2 array
			label: BaseLabel object, with components used to fully define the fragment
		"""
		self._data = data
		self._label = label

	@property
	def totalSpectralContributions(self):
		return self.spectralContributions[0]

	@property
	def spectralContributions(self):
		return [self._data]

	@property
	def label(self):
		return [self._label]





