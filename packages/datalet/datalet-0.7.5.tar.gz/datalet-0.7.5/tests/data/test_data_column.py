#!/usr/bin/env python
# -*- coding: utf-8  -*-

"""
execute the unittest file in project root directory.
"""
import sys
sys.path.insert(0, r"../datalet")

from datalet.data import *
import unittest
from tests.testing import Testing

class DataColumnTesting(Testing):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_getattr(self):
		col_name = DataColumn(name = "col_name", caption = "STUDENTNAME", dataType = type(str), nullable = True, defaultValue = 0)
		self.assertTrue(col_name.name == "col_name")
		self.assertTrue(col_name.caption == "STUDENTNAME")

	def test_setattr(self):
		col_name = DataColumn(name = "col_name", caption = "STUDENTNAME", dataType = type(str), nullable = True, defaultValue = 0)
		col_name.caption = "NAMEBIGGER"
		self.assertTrue(col_name.caption == "NAMEBIGGER")

	def test_delattr(self):
		col_name = DataColumn(name = "col_name", caption = "STUDENTNAME", dataType = type(str), nullable = True, defaultValue = 0)
		del col_name.caption
		print(col_name.caption)
		self.assertTrue(col_name.caption == None)


def suite():
	suite = unittest.TestSuite()
	suite.addTest(DataColumnTesting("test_getattr"))
	suite.addTest(DataColumnTesting("test_setattr"))
	suite.addTest(DataColumnTesting("test_delattr"))
	return suite

if __name__ == "__main__":
	unittest.main(defaultTest = "suite")
