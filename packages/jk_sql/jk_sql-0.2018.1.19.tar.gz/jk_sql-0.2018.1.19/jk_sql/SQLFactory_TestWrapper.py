#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import collections

from .AbstractSQLFactory import *
from .DBTableDef import *
from .AbstractDBTable import *





#
# Class to produce SQL statments. This class is providing support for the SQLite databases.
#
class SQLFactory_TestWrapper(AbstractSQLFactory):

	def __init__(self, wrappedFactory):
		self.__inst = wrappedFactory
	#

	################################################################################################################################
	#### PROPERTIES
	################################################################################################################################

	@property
	def dbTypeName(self):
		ret = self.__inst.dbTypeName
		assert isinstance(ret, str)
		return ret
	#

	@property
	def supportedDataTypes(self):
		ret = self.__inst.supportedDataTypes
		assert isinstance(ret, list)
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		ret = self.__inst.sqlStmt_createTable(tableDef)
		assert isinstance(ret, str)
		return ret
	#

	#
	# Destroy a database table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_dropTable(self, tableDef):
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		ret = self.__inst.sqlStmt_dropTable(tableDef)
		assert isinstance(ret, str)
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(newName, str)
		ret = self.__inst.sqlStmt_renameTable(tableDef, newName)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert not isinstance(ret[1], (tuple, list))
		assert isinstance(ret[1], object)
		return ret
	#

	#
	# Create a new column in a data table.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the new column.
	# @return	tuple<str,mixed>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* A value for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_addTableColumn(self, tableDef, columnDef):
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDef, DBColDef)
		ret = self.__inst.sqlStmt_addTableColumn(tableDef, columnDef)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert not isinstance(ret[1], (tuple, list))
		assert isinstance(ret[1], object)
		return ret
	#

	#
	# Remove an existing table column.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column to destroy.
	# @return	str							Returns an SQL string
	#
	def sqlStmt_dropTableColumn(self, tableDef, columnDef):
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDef, DBColDef)
		ret = self.__inst.sqlStmt_dropTableColumn(tableDef, columnDef)
		assert isinstance(ret, str)
		return ret
	#

	#
	# Rename an existing table column.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column to modify.
	# @param	str newName					The new name for the table column.
	# @return	tuple<str,mixed>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* A value for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_renameTableColumn(self, tableDef, columnDef, newName):
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDef, DBColDef)
		assert isinstance(newName, str)
		ret = self.__inst.sqlStmt_renameTableColumn(tableDef, columnDef, newName)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert not isinstance(ret[1], (tuple, list))
		assert isinstance(ret[1], object)
		return ret
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
	# @return	tuple<str,mixed>			Returns a tuple consisting of two items:
	#										* The SQL string to use for the DB query.
	#										* A value for the DEFAULT clause to pass to prepared statements.
	#
	def sqlStmt_modifyTableColumnType(self, tableDef, columnDef, fieldType, bIsNullable):
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDef, DBColDef)
		assert isinstance(fieldType, EnumDBColType)
		assert isinstance(bIsNullable, bool)
		ret = self.__inst.sqlStmt_modifyTableColumnType(tableDef, columnDef, fieldType, bIsNullable)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert not isinstance(ret[1], (tuple, list))
		assert isinstance(ret[1], object)
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDef, DBColDef)
		ret = self.__inst.sqlStmt_createIndex(tableDef, columnDef)
		assert isinstance(ret, str)
		return ret
	#

	#
	# Destroy an existing index for a table column.
	# NOTE: Please note that such a column must have an index.
	#
	# @param	mixed tableDef				A table object. Either <c>DBTableDef</c> or the table class used by the corresponding database implementation.
	# @param	DBColDef columnDef			The definition of the column.
	#
	def sqlStmt_dropIndex(self, tableDef, columnDef):
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDef, DBColDef)
		ret = self.__inst.sqlStmt_dropIndex(tableDef, columnDef)
		assert isinstance(ret, str)
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(dataKeys, (tuple, list))
		for key in dataKeys:
			assert isinstance(key, str)
		ret = self.__inst.sqlStmt_insertRowIntoTable(tableDef, dataKeys)
		assert isinstance(ret, str)
		return ret
	#

	def sqlStmt_insertFromTableIntoTable(self, fromTableDef, fromDataKeys, intoTableDef, intoDataKeys):
		assert isinstance(fromTableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(fromDataKeys, (tuple, list))
		for key in fromDataKeys:
			assert isinstance(key, str)
		assert isinstance(intoTableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(intoDataKeys, (tuple, list))
		for key in intoDataKeys:
			assert isinstance(key, str)
		ret = self.__inst.sqlStmt_insertFromTableIntoTable(fromTableDef, fromDataKeys, intoTableDef, intoDataKeys)
		assert isinstance(ret, str)
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(dataKeys, (tuple, list))
		for key in dataKeys:
			assert isinstance(key, str)
		if filter != None:
			assert isinstance(filter, dict)
			for key in filter:
				assert isinstance(key, str)
		ret = self.__inst.sqlStmt_updateRowInTable(tableDef, dataKeys, filter)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert isinstance(ret[1], (tuple, list))
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		if filter != None:
			assert isinstance(filter, dict)
			for key in filter:
				assert isinstance(key, str)
		ret = self.__inst.sqlStmt_deleteRowsFromTable(tableDef, filter)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert isinstance(ret[1], (tuple, list))
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		if filter != None:
			assert isinstance(filter, dict)
			for key in filter:
				assert isinstance(key, str)
		ret = self.__inst.sqlStmt_selectSingleRowFromTable(tableDef, filter)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert isinstance(ret[1], (tuple, list))
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		if filter != None:
			assert isinstance(filter, dict)
			for key in filter:
				assert isinstance(key, str)
		ret = self.__inst.sqlStmt_selectMultipleRowsFromTable(tableDef, filter)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert isinstance(ret[1], (tuple, list))
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		assert isinstance(columnDefs, (tuple, list))
		for c in columnDefs:
			assert isinstance(c, DBColDef)
		if filter != None:
			assert isinstance(filter, dict)
			for key in filter:
				assert isinstance(key, str)
		ret = self.__inst.sqlStmt_selectDistinctValuesFromTable(tableDef, columnDefs, filter)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert isinstance(ret[1], (tuple, list))
		return ret
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
		assert isinstance(tableDef, (DBTableDef, AbstractDBTable))
		if filter != None:
			assert isinstance(filter, dict)
			for key in filter:
				assert isinstance(key, str)
		ret = self.__inst.sqlStmt_countRowsInTable(tableDef, filter)
		assert isinstance(ret, (tuple, list))
		assert len(ret) == 2
		assert isinstance(ret[0], str)
		assert isinstance(ret[1], (tuple, list))
		return ret
	#

#



