#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

import sqlite3

from ..AbstractDBTable import *





class MySQLTable(AbstractDBTable):



	def __init__(self, db, tableName, columnDefs):
		assert db.__class__.__name__ == "MySQLDB"
		super().__init__(db, tableName, columnDefs, True, False)
	#



	@staticmethod
	def loadFromJSON(db, jsonDef):
		colDefs = []
		for jsonColDef in jsonDef["columns"]:
			colDefs.append(DBColDef.loadFromJSON(jsonColDef))
		return MySQLTable(db, jsonDef["name"], colDefs)
	#



#











