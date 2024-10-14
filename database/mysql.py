import mysql.connector
import os
from config_reader import Config_Reader 
from result import Result


class MySqlDatabase(Config_Reader):
	connection = {}
	results = []
	search = ""
 
	def __init__(self, config):  
		self.name = config.name
		self.type = config.type
		self.tables = config.tables
		self.resultMax = config.resultMax
		self.channel = config.channel

 
	def openConnection(self):
		self.connection = mysql.connector.connect(
			host=os.getenv("MYSQL_HOST"),
			user=os.getenv("MYSQL_USER"),
			password=os.getenv("MYSQL_PASSWORD"),
			database=self.name
		)
  
	def closeConnection(self):
		self.connection.close()
  
	def doQuery(self, search, equality):
		self.search = search
		cursor = self.connection.cursor()
  
		for table in self.tables:
			where = []
	
			for field in table.fields:
				where.append(f"{field.name} {equality} %s")

			cursor.execute(f"select * from {table.name} where " + " or ".join(where), [search] * len(table.fields))
			self.results.append(Result(cursor.fetchall(), table.name))
  
	def omniSearch(self, search, equality):
		self.openConnection()
		self.doQuery(search, equality)
		message = self.getMessage(self.results)
		self.closeConnection()
		return message
