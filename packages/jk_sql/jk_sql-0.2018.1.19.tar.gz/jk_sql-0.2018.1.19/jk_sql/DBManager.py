#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import codecs
import json
import sys

from .DataModelContainerFile import *
from .DataModelContainerMemory import *




class DBManager(object):

	@staticmethod
	def checkForMySQLConnector():
		for dir in ( "/usr/lib/python3/dist-packages/pymysql", "/usr/lib/python3/dist-packages/pymysql" ):
			if os.path.isdir(dir):
				return True
		return False
	#

	################################################################
	#### SQLite
	################################################################

	@staticmethod
	def createSQLiteDB(dirPath, bOverwriteIfExists = False):
		assert isinstance(dirPath, str)
		assert isinstance(bOverwriteIfExists, bool)

		import sqlite3
		from .sqlite.SQLiteDB import SQLiteDB

		if not os.path.isdir(dirPath):
			os.mkdir(dirPath)

		dataFilePath = os.path.join(dirPath, "data.db")
		modelFilePath = os.path.join(dirPath, "model.json")
		if os.path.isfile(dataFilePath) and os.path.isfile(modelFilePath):
			if not bOverwriteIfExists:
				raise Exception("Database already exists at: " + dirPath)

		if os.path.isfile(dataFilePath):
			os.unlink(dataFilePath)
		if os.path.isfile(modelFilePath):
			os.unlink(modelFilePath)

		return SQLiteDB(
			sqlite3.connect(dataFilePath),
			DataModelContainerFile(modelFilePath)
			)
	#

	@staticmethod
	def existsSQLiteDB(dirPath):
		assert isinstance(dirPath, str)

		if not os.path.isdir(dirPath):
			return False

		dataFile = os.path.join(dirPath, "data.db")
		modelFile = os.path.join(dirPath, "model.json")
		if os.path.isfile(dataFile) or os.path.isfile(modelFile):
			return True

		return False
	#

	@staticmethod
	def deleteSQLiteDB(dirPath):
		assert isinstance(dirPath, str)

		if not os.path.isdir(dirPath):
			return False

		dataFile = os.path.join(dirPath, "data.db")
		if os.path.isfile(dataFile):
			os.unlink(dataFile)
		modelFile = os.path.join(dirPath, "model.json")
		if os.path.isfile(modelFile):
			os.unlink(modelFile)

		return True
	#

	@staticmethod
	def createSQLiteMemoryDB():
		import sqlite3
		from .sqlite.SQLiteDB import SQLiteDB

		return SQLiteDB(
			sqlite3.connect(":memory:"),
			DataModelContainerMemory()
			)
	#

	@staticmethod
	def openSQLiteDB(dirPath):
		assert isinstance(dirPath, str)

		import sqlite3
		from .sqlite.SQLiteDB import SQLiteDB

		if not os.path.isdir(dirPath):
			raise Exception("Directory does not exist!")

		dataFile = os.path.join(dirPath, "data.db")
		modelFile = os.path.join(dirPath, "model.json")
		if not os.path.isfile(dataFile) or not os.path.isfile(modelFile):
			raise Exception("No database exists at specified location: " + dirPath)

		return SQLiteDB(
			sqlite3.connect(dataFile),
			DataModelContainerFile(modelFile)
			)
	#

	################################################################
	#### MySQL/MariaSQL
	################################################################

	@staticmethod
	def existsMySQLDB(dbHost, dbUser, dbPassword, dbName, modelFilePath):
		assert isinstance(dbHost, str)
		assert isinstance(dbUser, str)
		assert isinstance(dbPassword, str)
		assert isinstance(dbName, str)
		assert isinstance(modelFilePath, str)

		if not DBManager.checkForMySQLConnector():
			raise Exception("MySQL database connector not installed!")

		if os.path.isfile(modelFilePath):
			return True

		import pymysql
		import pymysql.cursors
		from .mysql.MySQLDB import MySQLDB

		connection = pymysql.connect(
			host = dbHost,
			user = dbUser,
			password = dbPassword,
			charset = 'utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)
		n = connection.cursor().execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + dbName + "'")
		return n > 0
	#

	@staticmethod
	def deleteMySQLDB(dbHost, dbUser, dbPassword, dbName, modelFilePath):
		assert isinstance(dbHost, str)
		assert isinstance(dbUser, str)
		assert isinstance(dbPassword, str)
		assert isinstance(dbName, str)
		assert isinstance(modelFilePath, str)

		if not DBManager.checkForMySQLConnector():
			raise Exception("MySQL database connector not installed!")

		if os.path.isfile(modelFilePath):
			os.unlink(modelFilePath)

		import pymysql
		import pymysql.cursors
		from .mysql.MySQLDB import MySQLDB

		connection = pymysql.connect(
			host = dbHost,
			user = dbUser,
			password = dbPassword,
			charset = 'utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)

		n = connection.cursor().execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + dbName + "'")
		if n > 0:
			connection.cursor().execute("DROP DATABASE `" + dbName + "`")

		return True
	#

	@staticmethod
	def createMySQLDB(dbHost, dbUser, dbPassword, dbName, modelFilePath, bOverwriteIfExists = False):
		assert isinstance(dbHost, str)
		assert isinstance(dbUser, str)
		assert isinstance(dbPassword, str)
		assert isinstance(dbName, str)
		assert isinstance(modelFilePath, str)
		assert isinstance(bOverwriteIfExists, bool)

		if not DBManager.checkForMySQLConnector():
			raise Exception("MySQL database connector not installed!")

		if os.path.isfile(modelFilePath):
			if not bOverwriteIfExists:
				raise Exception("Database model file already exists at: " + modelFilePath)

		import pymysql
		import pymysql.cursors
		from .mysql.MySQLDB import MySQLDB

		connection = pymysql.connect(
			host = dbHost,
			user = dbUser,
			password = dbPassword,
			charset = 'utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)
		n = connection.cursor().execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + dbName + "'")
		if n > 0:
			connection.cursor().execute("DROP DATABASE `" + dbName + "`")
		connection.cursor().execute("CREATE DATABASE `" + dbName + "` CHARACTER SET = 'utf8mb4'")
		connection.cursor().execute("USE `" + dbName + "`")

		if os.path.isfile(modelFilePath):
			os.unlink(modelFilePath)
		modelFile = DataModelContainerFile(modelFilePath)

		return MySQLDB(
			connection,
			modelFile
			)
	#

	@staticmethod
	def openMySQLDB(dbHost, dbUser, dbPassword, dbName, modelFilePath):
		assert isinstance(dbHost, str)
		assert isinstance(dbUser, str)
		assert isinstance(dbPassword, str)
		assert isinstance(dbName, str)
		assert isinstance(modelFilePath, str)

		if not os.path.isfile(modelFilePath):
			raise Exception("Model file not found: " + modelFilePath)
		modelFile = DataModelContainerFile(modelFilePath)

		if not DBManager.checkForMySQLConnector():
			raise Exception("MySQL database connector not installed!")

		import pymysql
		import pymysql.cursors
		from .mysql.MySQLDB import MySQLDB

		connection = pymysql.connect(
			host = dbHost,
			user = dbUser,
			password = dbPassword,
			db = dbName,
			charset = 'utf8mb4',
			cursorclass = pymysql.cursors.DictCursor)

		return MySQLDB(
			connection,
			modelFile
			)
	#

#











