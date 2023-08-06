#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import collections


from ..NotSupportedException import NotSupportedException
from ..AbstractSQLFactory import *
from ..EnumDBColType import *
from ..EnumDBIndexType import *




#
# Class to produce SQL statments. This class is providing support for the SQLite databases.
#
class SQLFactory_SQLite(AbstractSQLFactory):

	def __init__(self):
		super().__init__(
			"SQLite",
			{
				EnumDBColType.PK : "INTEGER PRIMARY KEY",
				EnumDBColType.BOOL : "INT",
				EnumDBColType.INT32 : "INT",
				EnumDBColType.INT64 : "INT",
				EnumDBColType.DOUBLE : "REAL",
				EnumDBColType.STR256 : "TEXT",
				EnumDBColType.CLOB : "TEXT",
				EnumDBColType.BLOB : "BLOB",
			},
			{
				EnumDBColType.BOOL : 0,
				EnumDBColType.INT32 : 0,
				EnumDBColType.INT64 : 0,
				EnumDBColType.DOUBLE : 0,
				EnumDBColType.STR256 : "",
				EnumDBColType.CLOB : "",
				EnumDBColType.BLOB : "",
			})
	#

	################################################################################################################################
	#### HELPER METHODS
	################################################################################################################################

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
	#### TRANSACTION SUPPORT
	################################################################################################################################

	#
	# Begin a transaction.
	#
	# @return	str							Returns an SQL string
	#
	def sqlStmt_beginTA(self):
		return "BEGIN"
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
		sqlColDefsStrList = self._sql_colDefsStrList(tableDef.columns)
		sqlStatement = "CREATE TABLE {} ({})".format(tableDef.name, ', '.join(sqlColDefsStrList))
		return sqlStatement
	#

	#
	# Destroy a database table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_dropTable(self, tableDef):
		sqlStatement = "DROP TABLE " + tableDef.name
		return sqlStatement
	#

	#
	# Create a new column in a data table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the new column.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_addTableColumn(self, tableDef, columnDef):
		return ("ALTER TABLE {} ADD COLUMN {} DEFAULT ?".format(tableDef.name, self._sql_colDefStr(columnDef)), self._defaultValue(columnDef.type))
	#

	#
	# Remove an existing table column.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column to destroy.
	#
	def sqlStmt_dropTableColumn(self, tableDef, columnDef):
		raise NotSupportedException()
	#

	#
	# Rename an existing table column.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column to modify.
	# @param	str newName					The new name for the table column.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_renameTableColumn(self, tableDef, columnDef, newName):
		raise NotSupportedException()
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
	# @return	str							Returns an SQL string
	#
	def sqlStmt_modifyTableColumnType(self, tableDef, columnDef, fieldType, bIsNullable):
		raise NotSupportedException()
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
		if columnDef.index == EnumDBIndexType.INDEX:
			s = "CREATE INDEX idx_{tname}_{cname} ON {tname} ({cname} ASC)".format(tname=tableDef.name, cname=columnDef.name)
		elif columnDef.index == EnumDBIndexType.UNIQUE_INDEX:
			s = "CREATE UNIQUE INDEX idx_{tname}_{cname} ON {tname} ({cname} ASC)".format(tname=tableDef.name, cname=columnDef.name)
		else:
			raise Exception("Unrecognized index: " + str(columnDef.index))
		return s
	#

	#
	# Destroy an existing index for a table column.
	# NOTE: Please note that such a column must have an index.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column.
	#
	def sqlStmt_dropIndex(self, tableDef, columnDef):
		return "DROP INDEX idx_{}_{}".format(tableDef.name, columnDef.name)
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
		keys = ",".join(dataKeys)
		values = ("?," * len(dataKeys))[:-1]
		return "INSERT INTO {} ({}) VALUES ({})".format(tableDef.name, keys, values)
	#

	def sqlStmt_insertFromTableIntoTable(self, fromTableDef, fromDataKeys, intoTableDef, intoDataKeys):
		sSel = "SELECT "
		bComma = False
		for key in fromDataKeys:
			if bComma:
				sSel += ","
			else:
				bComma = True
			sSel += key
		sSel += " FROM " + fromTableDef.name

		sInsert = "INSERT INTO " + intoTableDef.name + " ("
		bComma = False
		for key in intoDataKeys:
			assert isinstance(key, str)
			if bComma:
				sInsert += ","
			else:
				bComma = True
			sInsert += key
		s = sInsert + ") " + sSel

		return s
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
		s = "UPDATE " + tableDef.name + " SET "
		bComma = False
		for key in dataKeys:
			if bComma:
				s += ","
			else:
				bComma = True
			s += key + " = ?"

		ret = []
		if filter != None:
			s += " WHERE "
			bAddSep = False
			for key in filter:
				if bAddSep:
					s += " AND "
				else:
					bAddSep = True
				value = filter[key]
				if value is None:
					s += "(" + key + " is null)"
				else:
					s += "(" + key + " = ?)"
					ret.append(value)

		return s, ret
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
		s = "DELETE FROM " + tableDef.name + " WHERE "

		bAddSep = False
		ret = []
		for key in filter:
			assert isinstance(key, str)
			if bAddSep:
				s += " AND "
			else:
				bAddSep = True
			value = filter[key]
			if value is None:
				s += "(" + key + " is null)"
			else:
				s += "(" + key + " = ?)"
				ret.append(value)

		return s, ret
	#

	################################################################################################################################
	#### READ DATA
	################################################################################################################################

	def __selectRowsFromTable(self, tableDef, columnDefs, filter, bDistinct, bLimitToOne):
		keys = ",".join([col.name for col in columnDefs])
		if bDistinct:
			s = "SELECT DISTINCT {} FROM {}".format(keys, tableDef.name)
		else:
			s = "SELECT {} FROM {}".format(keys, tableDef.name)
		ret = []

		if filter != None:
			s += " WHERE "
			bAddSep = False
			for key in filter:
				if bAddSep:
					s += " AND "
				else:
					bAddSep = True
				value = filter[key]
				if value is None:
					s += "(" + key + " IS NULL)"
				else:
					s += "(" + key + " = ?)"
					ret.append(value)

		if bLimitToOne:
			s += " LIMIT 1"

		return s, ret
	#

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
		return self.__selectRowsFromTable(tableDef, tableDef.columns, filter, False, True)
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
		return self.__selectRowsFromTable(tableDef, tableDef.columns, filter, False, False)
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
		return self.__selectRowsFromTable(tableDef, columnDefs, filter, True, False)
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
		s = "SELECT COUNT(*) FROM {}".format(tableDef.name)
		ret = []

		if filter != None:
			s += " WHERE "
			bAddSep = False
			for key in filter:
				if bAddSep:
					s += " AND "
				else:
					bAddSep = True
				value = filter[key]
				if value is None:
					s += "(" + key + " IS NULL)"
				else:
					s += "(" + key + " = ?)"
					ret.append(value)

		return s, ret
	#

#



