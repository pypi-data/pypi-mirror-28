#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from ..AbstractDB import *
from .SQLFactory_MySQL import *
from .MySQLTable import *




class MySQLDB(AbstractDB):



	def __init__(self, dbConnection, dataModelContainer):
		super().__init__(dbConnection, dataModelContainer, SQLFactory_MySQL(), MySQLTable.loadFromJSON)
	#



	def _instantiateTableObj(self, tableName, tableColumns):
		return MySQLTable(self, tableName, tableColumns)
	#



#











