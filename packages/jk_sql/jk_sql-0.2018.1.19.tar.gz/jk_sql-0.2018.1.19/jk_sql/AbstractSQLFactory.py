#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import collections

from .EnumDBColType import EnumDBColType





#
# Class to produce SQL statments. This class is providing support for the SQLite databases.
#
class AbstractSQLFactory(object):

	def __init__(self, dbTypeName, dataTypeMap, defaultValueMap):
		self.__dbTypeName = dbTypeName

		self.__dataTypeMap = dataTypeMap			# EnumDBColType to SQL string
		self.__intTypeMap = dict()					# int representing EnumDBColType to SQL string
		for x in dataTypeMap:
			self.__intTypeMap[int(x)] = dataTypeMap[x]

		self.__defaultValueMap = defaultValueMap	# EnumDBColType to SQL string
		self.__intDefaultValueMap = dict()			# int representing EnumDBColType to SQL string
		for x in defaultValueMap:
			self.__intDefaultValueMap[int(x)] = defaultValueMap[x]

		self.__supportedDataTypes = tuple([ x for x in self.__dataTypeMap ])
	#

	################################################################################################################################
	#### HELPER METHODS
	################################################################################################################################

	def _toSQLType(self, dataType):
		ret = self.__dataTypeMap.get(dataType, None)
		if ret is None:
			raise Exception("Type not supported: " + str(dataType))
		return ret
	#

	def _defaultValue(self, dataType):
		if dataType == EnumDBColType.PK:
			raise Exception()
		ret = self.__defaultValueMap.get(dataType, None)
		if ret is None:
			raise Exception("Type not supported: " + str(dataType))
		return ret
	#

	#
	# Returns a column definition string such as "VARCHAR NOT NULL"
	#
	# @param	DBColDef columnDef			The definition of the column.
	# @return	str							Returns an SQL string
	#
	def _sql_colDefStr(self, columnDef):
		return "{} {} {}".format(
			columnDef.name,
			self._toSQLType(columnDef.type),
			"NULL" if columnDef.nullable else "NOT NULL"
		)
	#

	#
	# Returns a list of column definition strings such as "VARCHAR NOT NULL"
	#
	# @param	DBColDef columnDef			The definition of the column.
	# @return	str[]						Returns a list of SQL strings
	#
	def _sql_colDefsStrList(self, colDefs):
		return [
			"{} {} {}".format(
				columnDef.name,
				self._toSQLType(columnDef.type),
				"NULL" if columnDef.nullable else "NOT NULL"
			)
			for columnDef in colDefs ]
	#

	################################################################################################################################
	#### PROPERTIES
	################################################################################################################################

	@property
	def dbTypeName(self):
		return self.__dbTypeName
	#

	@property
	def supportedDataTypes(self):
		return self.__supportedDataTypes
	#

	################################################################################################################################
	#### TRANSACTION SUPPORT
	################################################################################################################################

	#
	# Begin a transaction.
	#
	# @return	str							Returns an SQL string
	#
	def sqlStmt_beginTA(self):
		raise NotImplementedError()
	#

	################################################################################################################################
	#### DATA DEFINITION
	################################################################################################################################

	#
	# Create a new database table.
	# NOTE: Please note that such a table must have a primary key. These primary key columns can not be modified later.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_createTable(self, tableDef):
		raise NotImplementedError()
	#

	#
	# Destroy a database table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_dropTable(self, tableDef):
		raise NotImplementedError()
	#

	#
	# Rename a database table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	str newName					The new name of the table.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_renameTable(self, tableDef, newName):
		raise NotImplementedError()
	#

	#
	# Create a new column in a data table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the new column.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_addTableColumn(self, tableDef, columnDef):
		raise NotImplementedError()
	#

	#
	# Remove an existing table column.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column to destroy.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_dropTableColumn(self, tableDef, columnDef):
		raise NotImplementedError()
	#

	#
	# Rename an existing table column.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column to modify.
	# @param	str newName					The new name for the table column.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_renameTableColumn(self, tableDef, columnDef, newName):
		raise NotImplementedError()
	#

	#
	# Modify the type of an existing table column.
	# This method can not be used to create primary keys.
	# This method might not be supported by a database.
	# NOTE: Please note that such a column must not have an index.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The old definition of the column to modify.
	# @param	EnumDBColType fieldType		The new field type of a database column.
	# @param	bool bIsNullable			Indicates if this database field may be <c>null</c> or not.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_modifyTableColumnType(self, tableDef, columnDef, fieldType, bIsNullable):
		raise NotImplementedError()
	#

	################################################################################################################################
	#### INDEXING
	################################################################################################################################

	#
	# Create a new index for a table column.
	# @NOTE: Please note that such a column must not have an index.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column. The index type is defined in the column specification.
	#
	def sqlStmt_createIndex(self, tableDef, columnDef):
		raise NotImplementedError()
	#

	#
	# Destroy an existing index for a table column.
	# NOTE: Please note that such a column must have an index.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column.
	#
	def sqlStmt_dropIndex(self, tableDef, columnDef):
		raise NotImplementedError()
	#

	################################################################################################################################
	#### WRITE DATA
	################################################################################################################################

	#
	# Create an INSERT statement to insert a new data record into a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	str[] dataKeys				A tuple, list or iteration of column names. These are the columns to fill.
	#
	def sqlStmt_insertRowIntoTable(self, tableDef, dataKeys):
		raise NotImplementedError()
	#

	def sqlStmt_insertFromTableIntoTable(self, fromTableDef, fromDataKeys, intoTableDef, intoDataKeys):
		raise NotImplementedError()
	#

	#
	# Create an UPDATE statment to update existing data in a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	str[] dataKeys				A tuple, list or iteration of column names. These are the columns to modify.
	# @param	dict<str,mixed> filter		A dictionary of values acting as a filter: Address only those table rows that match this filter. This is the WHERE clause of the SQL statement.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the WHERE clause to pass to prepared statements.
	#
	def sqlStmt_updateRowInTable(self, tableDef, dataKeys, filter):
		raise NotImplementedError()
	#

	#
	# Create a DELETE statment to delete existing data from a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	dict<str,mixed> filter		A dictionary of values acting as a filter: Address only those table rows that match this filter. This is the WHERE clause of the SQL statement.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the WHERE clause to pass to prepared statements.
	#
	def sqlStmt_deleteRowsFromTable(self, tableDef, filter):
		raise NotImplementedError()
	#

	################################################################################################################################
	#### READ DATA
	################################################################################################################################

	#
	# Create a SELECT statment to retrieve a single data row from a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	dict<str,mixed> filter		A dictionary of values acting as a filter: Address only those table rows that match this filter. This is the WHERE clause of the SQL statement.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the WHERE clause to pass to prepared statements.
	#
	def sqlStmt_selectSingleRowFromTable(self, tableDef, filter):
		raise NotImplementedError()
	#

	#
	# Create a SELECT statment to retrieve multiple data rows from a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	dict<str,mixed> filter		A dictionary of values acting as a filter: Address only those table rows that match this filter. This is the WHERE clause of the SQL statement.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the WHERE clause to pass to prepared statements.
	#
	def sqlStmt_selectMultipleRowsFromTable(self, tableDef, filter):
		raise NotImplementedError()
	#

	#
	# Create a SELECT statment to retrieve data from a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	dict<str,mixed> filter		A dictionary of values acting as a filter: Address only those table rows that match this filter. This is the WHERE clause of the SQL statement.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the WHERE clause to pass to prepared statements.
	#
	def sqlStmt_selectDistinctValuesFromTable(self, tableDef, columnDefs, filter):
		raise NotImplementedError()
	#

	#
	# Create a SELECT statment that returns a single value which gives information about the number of data records in a table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	dict<str,mixed> filter		A dictionary of values acting as a filter: Address only those table rows that match this filter. This is the WHERE clause of the SQL statement.
	# @return	tuple<str,mixed[]>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* The list of values for the WHERE clause to pass to prepared statements.
	#
	def sqlStmt_countRowsInTable(self, tableDef, filter):
		raise NotImplementedError()
	#

#



