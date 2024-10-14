import json
from types import SimpleNamespace


class Config_Reader:
	name = ""
	resultMax = 0
	type = ""
	tables = []
	channel = ""
	
	def __init__(self, name):
		with open(name, "r") as f:
			database = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
  
		self.name = database.name
		self.type = database.type
		self.tables = database.tables
		self.resultMax = database.resultMax
		self.channel = database.channel
  
	def getMessage(self, results):
		foundResult = False
		message = f"Searching for \"{self.search}\":\n"
		for result in results:
			count = len(result.data)
			if count:
				foundResult = True
				message += f"found {count} on the {result.tableName} table"
				if count > self.resultMax:
					message += f", showing {self.resultMax}"
						
				message += "\n```"
				for row in result.data[:self.resultMax]:
						message += str(row) + "\n"
				message += "```\n"

		if not foundResult:
			message = "No results found."
		
		return message
  
	def databaseFactory(self):
		if self.type == "sqlite":
			from database.sqlite import SqliteDatabase
			return SqliteDatabase(self)
		elif self.type == "mysql":
			from database.mysql import MySqlDatabase
			return MySqlDatabase(self)
  
