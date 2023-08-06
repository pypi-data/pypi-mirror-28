#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import json

from .AbstractDBTable import *





class AbstractDB(object):



	def __init__(self, dbConnection, dataModelContainer, sqlFactory, loadTableFromJSONDelegate):
		self._dbConnection = dbConnection
		self._sqlFactory = sqlFactory
		self._dataModelContainer = dataModelContainer
		self._loadTableFromJSONDelegate = loadTableFromJSONDelegate
		#self._bFetchAtCursor = bFetchAtCursor

		model = dataModelContainer.loadDataModel()
		if model != None:
			self._loadDataModel(model)
		else:
			self._tables = []
			self._tablesByName = {}
	#



	# ----------------------------------------------------------------



	def _loadDataModel(self, jsonRawModel):
		self._tables = []
		self._tablesByName = {}

		for jsonTableDef in jsonRawModel["tables"]:
			t = self._loadTableFromJSONDelegate(self, jsonTableDef)
			self._tables.append(t)
			self._tablesByName[t.name] = t
	#



	def _storeDataModel(self):
		self._dataModelContainer.storeDataModel(self._tables)
	#



	# ----------------------------------------------------------------



	def __str__(self):
		return self.__class__.__name__ + "()"
	#



	def __repr__(self):
		return self.__class__.__name__ + "()"
	#



	# ----------------------------------------------------------------



	def _destroyTableCallback(self, table, log = None):
		assert isinstance(table, AbstractDBTable)

		if table.name not in self._tablesByName:
			raise Exception("Table not part of this database!")

		del self._tablesByName[table.name]

		sql = self._sqlFactory.sqlStmt_dropTable(table)
		if log:
			log.debug("SQL: " + sql)
		self._dbConnection.cursor().execute(sql)

		self._storeDataModel()
	#



	# ----------------------------------------------------------------



	def getCreateTable(self, tableDef, log = None):
		assert isinstance(tableDef, DBTableDef)

		t = self._tablesByName.get(tableDef.name, None)
		if t != None:
			return t
		return self.createTable(tableDef, log)
	#



	def getTable(self, tableName):
		assert isinstance(tableName, str)

		return self._tablesByName.get(tableName, None)
	#



	def getTableE(self, tableName):
		assert isinstance(tableName, str)

		return self._tablesByName[tableName]
	#



	def tableExists(self, tableName):
		assert isinstance(tableName, str)

		return tableName in self._tablesByName
	#



	def _verifyTableDefinition(self, tableDef):
		supportedDataTypes = self._sqlFactory.supportedDataTypes
		existingNames = set()
		for colDef in tableDef.columns:
			if colDef.name in existingNames:
				raise Exception("Duplicate column name detected: " + colDef.name)
			existingNames.add(colDef.name)
			if colDef.type not in supportedDataTypes:
				raise Exception("Unsupported data type \"" + str(colDef.type) + "\" at column: " + colDef.name)
	#



	def createTable(self, tableDef, log = None):
		assert isinstance(tableDef, DBTableDef)

		self._verifyTableDefinition(tableDef)

		if tableDef.name in self._tablesByName:
			raise Exception("Table already exists!")

		sql = self._sqlFactory.sqlStmt_createTable(tableDef)
		if log:
			log.debug("SQL: " + sql)
		self._dbConnection.cursor().execute(sql)

		for colDef in tableDef.columns:
			if colDef.index != EnumDBIndexType.NONE:
				sql = self._sqlFactory.sqlStmt_createIndex(tableDef, colDef)
				self._dbConnection.cursor().execute(sql)

		t = self._instantiateTableObj(tableDef.name, tableDef.columns)
		self._tables.append(t)
		self._tablesByName[t.name] = t

		self._storeDataModel()
		return t
	#



	def _instantiateTableObj(self, tableName, tableColumns):
		raise Exception("Not implemented!")
	#



	#
	# Destroys an existing table (if the table exists).
	# An exception is thrown on error.
	#
	# @param	str tableName		The name of an existing table
	# @return	bool				Returns <c>True</c> if the table existed (and could be deleted.)
	#
	def destroyTable(self, tableName, log = None):
		assert isinstance(tableName, str)

		table = self._tablesByName.get(tableName, None)
		if table:
			self._destroyTableCallback(table, log)
			return True
		else:
			return False
	#



#











