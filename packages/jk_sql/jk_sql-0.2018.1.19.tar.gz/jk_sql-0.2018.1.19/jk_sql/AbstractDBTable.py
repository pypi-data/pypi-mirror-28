#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

import sqlite3

from .DBColDef import *
from .DBTableDef import *





class AbstractDBTable(object):



	_EMPTY_TUPLE = tuple(list())



	def __init__(self, db, tableName, columnDefs, bFetchAtCursor, bConvertResultFromListToDict):
		assert isinstance(db, object)
		assert isinstance(tableName, str)
		if isinstance(columnDefs, tuple):
			columnDefs = list(columnDefs)
		else:
			assert isinstance(columnDefs, list)
		assert isinstance(bFetchAtCursor, bool)
		assert isinstance(bConvertResultFromListToDict, bool)

		self._db = db
		self.__bFetchAtCursor = bFetchAtCursor
		self.__bConvertResultFromListToDict = bConvertResultFromListToDict
		#self._db.isolation_level = None
		self._name = tableName
		self._columnDefs = columnDefs
		self._columnDefsByName = None
		self._columnDefsNameToIndex = None
		self.__cachedColumnNames = None

		self._reconstructInternalData()
	#



	def _reconstructInternalData(self):
		self._columnDefsByName = {}
		self._columnDefsNameToIndex = {}

		count = 0
		for colDef in self._columnDefs:
			assert isinstance(colDef, DBColDef)
			self._columnDefsByName[colDef.name] = colDef
			self._columnDefsNameToIndex[colDef.name] = count
			count += 1

		self.__cachedColumnNames = None
	#



	def toJSON(self):
		columns = []
		for colDef in self._columnDefs:
			columns.append(colDef.toJSON())

		return {
			"name" : self._name,
			"columns" : columns
		}
	#



	# ----------------------------------------------------------------



	@property
	def name(self):
		return self._name
	#



	#
	# Returns the list of columns in this table. This list includes the primary key column.
	#
	# @return	DBColDef[]		Returns a list of column definition objects.
	#
	@property
	def columns(self):
		return tuple(self._columnDefs)
	#



	#
	# Get a specific column.
	#
	def getColumn(self, nameOrIndex):
		if isinstance(nameOrIndex, str):
			return self._columnDefsByName.get(nameOrIndex, None)
		elif isinstance(nameOrIndex, int):
			if (nameOrIndex < 0) or (nameOrIndex >= len(self._columnDefs)):
				return None
			else:
				return self._columnDefs[nameOrIndex]
		else:
			raise Exception("Unexpected type: " + str(type(nameOrIndex)))
	#



	#
	# Get a specific column.
	#
	def getColumnE(self, nameOrIndex):
		if isinstance(nameOrIndex, str):
			columnDef = self._columnDefsByName.get(nameOrIndex, None)
		elif isinstance(nameOrIndex, int):
			if (nameOrIndex < 0) or (nameOrIndex > len(self._columnDefs)):
				columnDef = None
			else:
				columnDef = self._columnDefs[nameOrIndex]
		else:
			raise Exception("Unexpected type: " + str(type(nameOrIndex)))
		if columnDef is None:
			raise Exception("No such column: " + nameOrIndex)
		else:
			return columnDef
	#



	#
	# Returns the list of column names in this table. Please be aware that the data returned here does not have a clearly defined order.
	#
	# @return	str[]		Returns a string list containing all column names.
	#
	@property
	def columnNames(self):
		if self.__cachedColumnNames is None:
			self.__cachedColumnNames = []
			for colDef in self._columnDefs:
				self.__cachedColumnNames.append(colDef.name)
		return self.__cachedColumnNames
	#



	@property
	def pkColumn(self):
		for c in self._columnDefs:
			if c.type == EnumDBColType.PK:
				return c
		return None
	#



	# ----------------------------------------------------------------



	def _beginTA(self):
		if self.__bFetchAtCursor:
			c = self._db._dbConnection.cursor()
			# c.execute(sql)			## not needed: TAs are started automatically
			return c
		else:
			sql = self._db._sqlFactory.sqlStmt_beginTA()
			self._db._dbConnection.execute(sql)
			return None
	#



	def modifyColumn(self, columnName, newColDef, log = None):
		assert isinstance(columnName, str)
		assert isinstance(newColDef, DBColDef)

		curColDef = self.getColumnE(columnName)

		# determine if we need to drop and recreate the index
		# we need to do this if there is a type change or even if the name of the column has changed
		bDropIndex = False
		bCreateIndex = False
		if curColDef.index == newColDef.index:
			if (curColDef.type != newColDef.type) or (curColDef.name != newColDef.name):
				bDropIndex = True
				bCreateIndex = True
		else:
			if curColDef.index != EnumDBIndexType.NONE:
				bDropIndex = True
			if newColDef.index != EnumDBIndexType.NONE:
				bCreateIndex = True
		bRenameColumn = curColDef.name != newColDef.name
		bRenameByCopy = False
		if bRenameColumn:
			if newColDef.name in self._columnDefsByName:
				raise Exception("Can't rename column because another column of that name already exists: " + newColDef.name + "!")
			if not self._db._sqlFactory.supportsRenameColumn:
				if self._db._sqlFactory.supportsCopyColumn:
					if self._db._sqlFactory.supportsDropColumn:
						bRenameByCopy = True
					else:
						raise Exception("Renaming columns is not supported by databases of type " + self._db._sqlFactory.dbTypeName + "!")
				else:
					raise Exception("Renaming columns is not supported by databases of type " + self._db._sqlFactory.dbTypeName + "!")
		bModifyColumn = (curColDef.type != newColDef.type) or (curColDef.nullable != newColDef.nullable)
		if bModifyColumn:
			if not self._db._sqlFactory.supportsModifyColumn:
				raise Exception("Modifying columns is not supported by databases of type " + self._db._sqlFactory.dbTypeName + "!")
			if (curColDef.type == EnumDBColType.PK) and (newColDef.type != EnumDBColType.PK):
				raise Exception("Primary keys can not be changed!")
			if (newColDef.type == EnumDBColType.PK) and (newColDef.type != EnumDBColType.PK):
				raise Exception("Can't modify column to be primary key!")

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				if bDropIndex:
					# drop index
					sql = self._db._sqlFactory.sqlStmt_dropIndex(self, curColDef)
					c.execute(sql)
					curColDef = DBColDef(curColDef.name, curColDef.type, curColDef.nullable, EnumDBIndexType.NONE)

				if bRenameColumn:
					if bRenameByCopy:
						# create new column
						sql = self._db._sqlFactory.sqlStmt_addTableColumn(self, newColDef)
						if log:
							log.debug("SQL: " + sql)
						c.execute(sql)
						# copy column
						sql = self._db._sqlFactory.sqlStmt_copyTableColumn(self, curColDef, newColDef)
						if log:
							log.debug("SQL: " + sql)
						c.execute(sql)
						# drop old column
						sql = self._db._sqlFactory.sqlStmt_dropTableColumn(self, curColDef)
						if log:
							log.debug("SQL: " + sql)
						c.execute(sql)
					else:
						# rename column
						sql = self._db._sqlFactory.sqlStmt_renameTableColumn(self, curColDef, newColDef.name)
						if log:
							log.debug("SQL: " + sql)
						c.execute(sql)
					curColDef = DBColDef(newColDef.name, curColDef.type, curColDef.nullable, curColDef.index)

				if bModifyColumn:
					# modify column
					sql = self._db._sqlFactory.sqlStmt_modifyTableColumn(self, curColDef, newColDef)
					if log:
						log.debug("SQL: " + sql)
					c.execute(sql)
					curColDef = DBColDef(newColDef.name, newColDef.type, newColDef.nullable, curColDef.index)

				if bCreateIndex:
					# create index
					sql = self._db._sqlFactory.sqlStmt_createIndex(self, curColDef)
					if log:
						log.debug("SQL: " + sql)
					c.execute(sql)
					curColDef = DBColDef(curColDef.name, curColDef.type, curColDef.nullable, newColDef.index)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()

				if bDropIndex:
					# drop index
					sql = self._db._sqlFactory.sqlStmt_dropIndex(self, curColDef)
					self._db._dbConnection.execute(sql)
					curColDef = DBColDef(curColDef.name, curColDef.type, curColDef.nullable, EnumDBIndexType.NONE)

				if bRenameColumn:
					if bRenameByCopy:
						# create new column
						sql = self._db._sqlFactory.sqlStmt_addTableColumn(self, newColDef)
						if log:
							log.debug("SQL: " + sql)
						self._db._dbConnection.execute(sql)
						# copy column
						sql = self._db._sqlFactory.sqlStmt_copyTableColumn(self, curColDef, newColDef)
						if log:
							log.debug("SQL: " + sql)
						self._db._dbConnection.execute(sql)
						# drop old column
						sql = self._db._sqlFactory.sqlStmt_dropTableColumn(self, curColDef)
						if log:
							log.debug("SQL: " + sql)
						self._db._dbConnection.execute(sql)
					else:
						# rename column
						sql = self._db._sqlFactory.sqlStmt_renameTableColumn(self, curColDef, newColDef.name)
						if log:
							log.debug("SQL: " + sql)
						self._db._dbConnection.execute(sql)
					curColDef = DBColDef(newColDef.name, curColDef.type, curColDef.nullable, curColDef.index)

				if bModifyColumn:
					# modify column
					sql = self._db._sqlFactory.sqlStmt_modifyTableColumn(self, curColDef, newColDef)
					if log:
						log.debug("SQL: " + sql)
					self._db._dbConnection.execute(sql)
					curColDef = DBColDef(newColDef.name, newColDef.type, newColDef.nullable, curColDef.index)

				if bCreateIndex:
					# create index
					sql = self._db._sqlFactory.sqlStmt_createIndex(self, curColDef)
					if log:
						log.debug("SQL: " + sql)
					self._db._dbConnection.execute(sql)
					curColDef = DBColDef(curColDef.name, curColDef.type, curColDef.nullable, newColDef.index)

		self._columnDefsByName[columnName] = curColDef
		n = self._columnDefsNameToIndex[columnName]
		self._columnDefs[n] = curColDef
		self._db._storeDataModel()
	#



	#
	# Remove a column.
	#
	# @TODO: Not implemented yet!
	#
	def removeColumn(self, columnName, log = None):
		assert isinstance(columnName, str)
		if columnName not in self._columnDefsByName:
			raise Exception("Column already defined: " + str(columnName))
		colDef = self._columnDefsByName[columnName]
		if colDef.type == EnumDBColType.PK:
			raise Exception("Can't delete a primary key column!")

		# delete index if necessary

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				if colDef.index != EnumDBIndexType.NONE:
					sql = self._db._sqlFactory.sqlStmt_dropIndex(self, colDef)
					if log:
						log.debug("SQL: " + sql)
					c.execute(sql)

				self._beginTA()
				sql = self._db._sqlFactory.sqlStmt_dropTableColumn(self, colDef)
				if log:
					log.debug("SQL: " + sql)
				c.execute(sql)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				if colDef.index != EnumDBIndexType.NONE:
					sql = self._db._sqlFactory.sqlStmt_dropIndex(self, colDef)
					if log:
						log.debug("SQL: " + sql)
					self._db._dbConnection.execute(sql)

				self._beginTA()
				sql = self._db._sqlFactory.sqlStmt_dropTableColumn(self, colDef)
				if log:
					log.debug("SQL: " + sql)
				self._db._dbConnection.execute(sql)

		del self._columnDefsByName[colDef.name]
		del self._columnDefsNameToIndex[colDef.name]
		self.__cachedColumnNames = None

		self._db._storeDataModel()
	#



	#
	# Be aware that an index might be created here. SQLite might fail during index creation. This is NOT wrapped in a transaction.
	#
	def addColumn(self, colDef, log = None):
		assert isinstance(colDef, DBColDef)
		if colDef.name in self._columnDefsByName:
			raise Exception("Column already defined: " + colDef.name)
		if (colDef.type == EnumDBColType.PK) and (self.pkColumn != None):
			raise Exception("Can't create a second primary key column!")
		if (colDef.type != EnumDBColType.PK) and not colDef.nullable and colDef.unique:
			n = self.countRows()
			if n > 1:
				raise Exception("Can't create unique index on table if no distinct values have been stored in the new column! The values wouldn't be unique!")

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				sql = self._db._sqlFactory.sqlStmt_addTableColumn(self, colDef)
				if log:
					log.debug("SQL: " + sql)
				c.execute(sql)

				if colDef.index != EnumDBIndexType.NONE:
					sql = self._db._sqlFactory.sqlStmt_createIndex(self, colDef)
					if log:
						log.debug("SQL: " + sql)
					c.execute(sql)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()
				sql = self._db._sqlFactory.sqlStmt_addTableColumn(self, colDef)
				if log:
					log.debug("SQL: " + sql)
				self._db._dbConnection.execute(sql)

				if colDef.index != EnumDBIndexType.NONE:
					sql = self._db._sqlFactory.sqlStmt_createIndex(self, colDef)
					if log:
						log.debug("SQL: " + sql)
					self._db._dbConnection.execute(sql)

		i = len(self._columnDefs)

		self._columnDefs.append(colDef)
		self._columnDefsByName[colDef.name] = colDef
		self._columnDefsNameToIndex[colDef.name] = i

		if self.__cachedColumnNames != None:
			self.__cachedColumnNames.append(colDef.name)

		self._db._storeDataModel()
	#



	#
	# Add a single row to the table.
	#
	# @param	dict fieldData				A hash map containing the data
	# @param	str[] limitToColumnNames	If not <c>None</c> ignores other keys in the maps in <c>fieldDataList</c> than the ones specified here.
	#
	def addRow(self, fieldData, limitToColumnNames = None, log = None):
		assert isinstance(fieldData, dict)

		if limitToColumnNames != None:
			assert isinstance(limitToColumnNames, (tuple, list))
		else:
			limitToColumnNames = fieldData.keys()
		for columnName in limitToColumnNames:
			assert isinstance(columnName, str)
		existingColumnNames = set(self.columnNames)
		columnNames = []
		for columnName in limitToColumnNames:
			if columnName in existingColumnNames:
				columnNames.append(columnName)
			else:
				raise Exception("Invalid column names: " + str(limitToColumnNames))

		dataValueList = []
		for key in columnNames:
			dataValueList.append(fieldData.get(key, None))

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				sql = self._db._sqlFactory.sqlStmt_insertRowIntoTable(self, columnNames)
				if log:
					log.debug("SQL: " + sql)
				c.execute(sql, dataValueList)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()

				sql = self._db._sqlFactory.sqlStmt_insertRowIntoTable(self, columnNames)
				if log:
					log.debug("SQL: " + sql)
				self._db._dbConnection.execute(sql, dataValueList)

		#self._commitTA(c)
	#



	#
	# Add a varieties of rows to the table.
	#
	# @param	list<dict> fieldDataList		A list of hash maps containing the data
	# @param	str[] limitToColumnNames	If not <c>None</c> ignores other keys in the maps in <c>fieldDataList</c> than the ones specified here.
	#
	def addRows(self, fieldDataList, limitToColumnNames = None, log = None):
		assert isinstance(fieldDataList, list)
		for fieldData in fieldDataList:
			assert isinstance(fieldData, dict)

		if limitToColumnNames != None:
			assert isinstance(limitToColumnNames, (tuple, list))
		else:
			limitToColumnNames = set()
			for fieldData in fieldDataList:
				limitToColumnNames.update(fieldData.keys())
		for columnName in limitToColumnNames:
			assert isinstance(columnName, str)
		existingColumnNames = set(self.columnNames)
		columnNames = []
		for columnName in limitToColumnNames:
			if columnName in existingColumnNames:
				columnNames.append(columnName)
			else:
				raise Exception("Invalid column names: " + str(limitToColumnNames))

		sql = self._db._sqlFactory.sqlStmt_insertRowIntoTable(self, columnNames)
		if log:
			log.debug("SQL: " + sql)

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				for fieldData in fieldDataList:
					dataValueList = []
					for key in columnNames:
						dataValueList.append(fieldData.get(key, None))
					c.execute(sql, dataValueList)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()

				for fieldData in fieldDataList:
					dataValueList = []
					for key in columnNames:
						dataValueList.append(fieldData.get(key, None))
					self._db._dbConnection.execute(sql, dataValueList)
	#



	def updateRows(self, fieldData, filter, limitToColumnNames = None, log = None):
		assert isinstance(fieldData, dict)

		if limitToColumnNames != None:
			assert isinstance(limitToColumnNames, (tuple, list))
		else:
			limitToColumnNames = fieldData.keys()
		for columnName in limitToColumnNames:
			assert isinstance(columnName, str)
		existingColumnNames = set(self.columnNames)
		columnNames = []
		for columnName in limitToColumnNames:
			if columnName in existingColumnNames:
				columnNames.append(columnName)
			else:
				raise Exception("Invalid column names: " + str(limitToColumnNames))

		sql, filterValues = self._db._sqlFactory.sqlStmt_updateRowInTable(self, columnNames, filter)
		if log:
			log.debug("SQL: " + sql)

		dataValueList = []
		for key in columnNames:
			dataValueList.append(fieldData.get(key, None))
		dataValueList.extend(filterValues)

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:

				c.execute(sql, dataValueList)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()

				self._db._dbConnection.execute(sql, dataValueList)
	#



	def deleteRows(self, filter, log = None):
		sql, filterValues = self._db._sqlFactory.sqlStmt_deleteRowsFromTable(self, filter)
		if log:
			log.debug("SQL: " + sql)

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				c.execute(sql, filterValues)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()
				self._db._dbConnection.execute(sql, filterValues)
	#



	def countRows(self, filter = None, log = None):
		if filter != None:
			assert isinstance(filter, dict)

		sql, filterValues = self._db._sqlFactory.sqlStmt_countRowsInTable(self, filter)
		if log:
			log.debug("SQL: " + sql)

		c = self._db._dbConnection.cursor()
		if self.__bFetchAtCursor:
			n = c.execute(sql, filterValues)
			if n > 0:
				ret = c.fetchone()
			else:
				raise Exception()
		else:
			ret = c.execute(sql, filterValues).fetchone()[0]

		c.close()

		if not self.__bConvertResultFromListToDict and (ret != None):
			for key in ret:
				ret = ret[key]
				break

		return ret
	#



	#
	# Retrieve a data row.
	#
	# @return	dict			Returns a dictionary containing all data of this row.
	#
	def getRow(self, filter = None, log = None):
		if filter != None:
			assert isinstance(filter, dict)

		sql, filterValues = self._db._sqlFactory.sqlStmt_selectSingleRowFromTable(self, filter)
		if log:
			log.debug("SQL: " + sql)

		c = self._db._dbConnection.cursor()
		if self.__bFetchAtCursor:
			n = c.execute(sql, filterValues)
			if n > 0:
				ret = c.fetchone()
			else:
				ret = None
		else:
			ret = c.fetchone()

		if self.__bConvertResultFromListToDict and (ret != None):
			ret2 = dict()
			for i in range(0, len(ret)):
				ret2[self._columnDefs[i]] = ret[i]
			ret = ret2

		c.close()
		return ret
	#



	#
	# Retrieve a set of data rows.
	#
	# @return	dict[]			Returns a list of dictionaries containing all data of the rows retrieved.
	#
	def getRows(self, filter = None, log = None):
		if filter != None:
			assert isinstance(filter, dict)

		sql, filterValues = self._db._sqlFactory.sqlStmt_selectMultipleRowsFromTable(self, filter)
		if log:
			log.debug("SQL: " + sql)

		c = self._db._dbConnection.cursor()
		if self.__bFetchAtCursor:
			n = c.execute(sql, filterValues)
			if n > 0:
				ret = c.fetchall()
			else:
				ret = AbstractDBTable._EMPTY_TUPLE
		else:
			ret = c.execute(sql, filterValues).fetchall()
			if self.__bConvertResultFromListToDict and (ret != None):
				ret3 = []
				maxi = len(self._columnDefs)
				for row in ret:
					ret2 = dict()
					for i in range(0, maxi):
						ret2[self._columnDefs[i].name] = row[i]
					ret3.append(ret2)
				ret = ret3

		c.close()
		return ret
	#



	#
	# Retrieve a set of data rows.
	#
	# @return	dict[]			Returns a list of dictionaries containing all data of the rows retrieved.
	#
	def getDistinct(self, columnNames, filter = None, log = None):
		if filter != None:
			assert isinstance(filter, dict)

		columnDefs = []
		assert isinstance(columnNames, list)
		for columnName in columnNames:
			assert isinstance(columnName, str)
			columnDefs.append(self.getColumnE(columnName))

		sql, filterValues = self._db._sqlFactory.sqlStmt_selectDistinctValuesFromTable(self, columnDefs, filter)
		if log:
			log.debug("SQL: " + sql)

		c = self._db._dbConnection.cursor()
		if self.__bFetchAtCursor:
			n = c.execute(sql, filterValues)
			if n > 0:
				ret = c.fetchall()
			else:
				ret = AbstractDBTable._EMPTY_TUPLE
		else:
			ret = c.execute(sql, filterValues).fetchall()

		c.close()
		return ret
	#



	def getRowIterator(self, filter = None, log = None):
		if filter != None:
			assert isinstance(filter, dict)

		sql, filterValues = self._db._sqlFactory.sqlStmt_selectMultipleRowsFromTable(self, filter)
		if log:
			log.debug("SQL: " + sql)

		c = self._db._dbConnection.cursor()
		if self.__bFetchAtCursor:
			n = c.execute(sql, filterValues)
			if n > 0:
				for row in c:
					yield row
		else:
			for row in c.execute(sql, filterValues):
				yield row

		c.close()
	#



	def copyToOtherTable(self, otherTable, columnMapping, log = None):
		assert isinstance(otherTable, AbstractDBTable)
		if otherTable._db != self._db:
			raise Exception("Can't copy table to other data base!")
		assert isinstance(columnMapping, (tuple, list, dict))

		existingFromColumns = set(self.columnNames)
		existingToColumns = set(otherTable.columnNames)

		fromColumns = []
		toColumns = []
		if isinstance(columnMapping, (tuple, list)):
			for fromColumn, toColumn in columnMapping:
				if (fromColumn != None) and (toColumn != None):
					if fromColumn not in existingFromColumns:
						raise Exception("No such source column: " + fromColumn)
					if toColumn not in existingToColumns:
						raise Exception("No such destination column: " + toColumn)
					fromColumns.append(fromColumn)
					toColumns.append(toColumn)
		else:
			for fromColumn in columnMapping:
				toColumn = columnMapping[fromColumn]
				if toColumn != None:
					if fromColumn not in existingFromColumns:
						raise Exception("No such source column: " + fromColumn)
					if toColumn not in existingToColumns:
						raise Exception("No such destination column: " + toColumn)
					fromColumns.append(fromColumn)
					toColumns.append(toColumn)

		sql = self._db._sqlFactory.sqlStmt_insertFromTableIntoTable(self, fromColumns, otherTable, toColumns)
		if log:
			log.debug("SQL: " + sql)

		if self.__bFetchAtCursor:
			c = self._beginTA()
			try:
				c.execute(sql)

				self._db._dbConnection.commit()
			except Exception as e:
				self._db._dbConnection.rollback()
				raise e

		else:
			with self._db._dbConnection:
				self._beginTA()

				self._db._dbConnection.execute(sql)
	#



	def destroyTable(self, log = None):
		self._db._destroyTableCallback(self, log)
		self._db = None
		self._name = None
		self._columnDefs = None
		self._columnDefsNameToIndex = None
		self.__cachedColumnNames = None
	#



	# ----------------------------------------------------------------



	def __str__(self):
		s = "sqlite-table: " + self._name + " [ "
		bRequiresComma = False
		for col in self._columnDefs:
			if bRequiresComma:
				s += ", "
			s += col.name + ":" + str(col.type)
			bRequiresComma = True
		s += " ]"
		return s
	#



	def __repr__(self):
		return self.__str__()
	#



#











