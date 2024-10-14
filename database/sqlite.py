from config_reader import Config_Reader 
from result import Result
import sqlite3

class SqliteDatabase(Config_Reader):
	connection = {}
	results = []
	search = ""
 
	def __init__(self, database):  
		self.name = database.name
		self.type = database.type
		self.tables = database.tables
		self.resultMax = database.resultMax
		self.channel = database.channel

 
	def openConnection(self):
		self.connection = sqlite3.connect(self.name)
  
	def closeConnection(self):
		self.connection.close()
  
	def doQuery(self, search, equality):
		self.search = search
		cursor = self.connection.cursor()
  
		self.results = []
		for table in self.tables:
			where = []

			for field in table.fields:
				where.append(f"{field.name} {equality} :search")
    
			self.results.append(Result(
				cursor.execute(f"select * from {table.name} where " + " or ".join(where), (search,)).fetchall(),
				table.name
			))
  
	def omniSearch(self, search, equality):
		self.openConnection()
		self.doQuery(search, equality)
		message = self.getMessage(self.results)
		self.closeConnection()
		return message
