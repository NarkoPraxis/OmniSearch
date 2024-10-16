import json
from types import SimpleNamespace



class Config_Reader:
	name = ""
	resultMax = 0
	type = ""
	tables = []
	channel = ""
	userId = ""
	
	def __init__(self, configPath, userId):
		with open(configPath, "r") as f:
			database = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
  
		self.name = database.name
		self.type = database.type
		self.tables = database.tables
		self.resultMax = database.resultMax
		self.channel = database.channel
		self.userId = userId
  
	def databaseFactory(self):
		if self.type == "sqlite":
			from database.sqlite import SqliteDatabase
			return SqliteDatabase(self)
		elif self.type == "mysql":
			from database.mysql import MySqlDatabase
			return MySqlDatabase(self)
  