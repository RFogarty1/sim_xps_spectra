


class SearchableCollection():
	""" Groups elements, which each need a label attribute, in a way that allows simple searching to be carried out. 

	"""

	def __init__(self, elements):
		""" Initializer
		
		Args:
			elements: (iter of _SearchableElement objects) These objects simply need to implement a .label attribute which returns a SINGLE BaseLabel object. They also need to NOT implement the iter pattern. SearchableCollection objects can also be mixed in with the _SearchableElements
				 
		"""
		self.objs = list()
		for x in elements:
			try:
				iter(x)		
			except TypeError:
				self.objs.append( x ) #Executed for non-iterables
			else:
				self.objs.extend( x ) #Executed for iterables


	def getAllValsForComponent(self, compLabel):
		""" Get all values which are present for a specific component of the label objects
		
		Args:
			compLabel: The attribute name within the BaseLabel interface objects (e.g eleKey would be one for StandardLabel implementation)
				 
		Returns
			valList: (iter) The list of values that are present for this label (e.g. for eleKey we might have ["Mg","H"]
	 
		"""
		#Note we cant use sets here since we need to maintain the ordering
		allComps = [getattr(x.label,compLabel) for x in self.objs]
		uniqueComps = list()
		for x in allComps:
			if x not in uniqueComps:
				uniqueComps.append(x)

		return uniqueComps

	def getObjectsWithComponents(self,components, caseSensitive=True, partialMatch=False):
		""" Returns objects which match the components
		
		Args:
			components (str list): Strings which will be matched against BaseLabel (or inherited cls) components. Any object with 
		all of these components present will be returned 
			caseSensitive(bool): Whether we need to match the case of each component or not [Default=True]
			partialMatch(bool): Whether we need to match the full components string or just part of it. For example, if true the component="hell" will return objects with component "hello", if False they wont. Default=False
		Returns
			objList (iter): List of output objects where labels match components requested. 
	 
		"""
		inpComponents = list(components)
		allComps = [x.label.components for x in self.objs]

		#Deal with case sensitivity
		if not caseSensitive:
			for idx,x in enumerate(inpComponents):
				inpComponents[idx] = x.lower()
			for idx,x in enumerate(allComps):
				allComps[idx] = [x.lower() for x in allComps[idx] ]


		outObjs = list()
		for idx, currComps in enumerate(allComps):
			addCurrObj = True
			for inpComp in inpComponents: #Check if any components match
				if not self._inpCompMatchesObjComps(inpComp, currComps, partialMatch):
					addCurrObj = False #Could break here 
			if addCurrObj: 
				outObjs.append( self.objs[idx] )

		return outObjs

	#Duplicate from gen_basis_helpers.shared.misc_utils. Could be classmethod (self not needed really)
	def _inpCompMatchesObjComps(self, inpComp, objComps, partialMatchIsOk):
		if not partialMatchIsOk: 
			if inpComp in objComps:
				return True

		else:
			for oComp in objComponents:
				if inpComp in oComp: #test if strA part of strB
					return True

		return False

	def __iter__(self):
		yield from self.objs

class _SearchableElement():
	""" Effectively an abstract class defining the interface required for SearchableCollection element objects. No need to inherit from it

	"""

	def __init__(self, label):
		self._label = label

	@property
	def label(self):
		""" BaseLabel object which allows us to find this element in searches
		"""
		return self._label

	#
	def __iter__(self):
		raise TypeError("_SearchableElement is not iterable")

