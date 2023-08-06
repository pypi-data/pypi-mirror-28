#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from ..AbstractDB import *
from .SQLFactory_SQLite import *
from .SQLiteTable import *




class SQLiteDB(AbstractDB):



	def __init__(self, dbConnection, dataModelContainer):
		super().__init__(dbConnection, dataModelContainer, SQLFactory_SQLite(), SQLiteTable.loadFromJSON)
	#



	def _instantiateTableObj(self, tableName, tableColumns):
		return SQLiteTable(self, tableName, tableColumns)
	#



#











