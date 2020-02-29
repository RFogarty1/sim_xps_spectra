
import itertools as it

import unittest
import unittest.mock as mock

import gen_basis_helpers.shared.label_objs as baseLabels
import sim_xps_spectra.shared.searchable_collection as tCode

class TestSearchableCollection(unittest.TestCase):

	def setUp(self):
		self.eleKeys = ["Mg","Mg","Al"]
		self.methodKeys = ["methA","methB","methB"]
		self.structKeys = ["structA","structB","structC"]
		self.createTestObjects()

	def createTestObjects(self):
		labels=list()
		for eKey, mKey, sKey in it.zip_longest(self.eleKeys,self.methodKeys,self.structKeys):
			labels.append( baseLabels.StandardLabel(eleKey=eKey, methodKey=mKey, structKey=sKey) )
		self.eleA = tCode._SearchableElement(labels[0])
		self.eleB = tCode._SearchableElement(labels[1])
		self.eleC = tCode._SearchableElement(labels[2])
		self.testObjA = tCode.SearchableCollection([self.eleA, self.eleB])
		self.testObjB = tCode.SearchableCollection([self.testObjA, self.eleC])

	def testGetAllUniqueValsAllDiff(self):
		testKey = "structKey"
		expVals = self.structKeys
		actVals = self.testObjB.getAllValsForComponent(testKey)
		self.assertEqual(expVals,actVals)


	def testCompositeSearchExpMatchesAct(self):
		compSearchTerm = "methB"
		expObjs = [self.eleB, self.eleC]
		actObjs = self.testObjB.getObjectsWithComponents([compSearchTerm])
		self.assertEqual(expObjs, actObjs)

