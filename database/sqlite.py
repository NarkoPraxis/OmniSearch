from args import Arguements
from config_reader import Config_Reader 
from database.base import Database
from result import Result
import sqlite3

class SqliteDatabase(Database):
 
	def openConnection(self):
		self.connection = sqlite3.connect(self.name)
  
	def closeConnection(self):
		self.connection.close()
  
	def doQuery(self, arguements: Arguements):
		self.search = arguements.search
		cursor = self.connection.cursor()
  
		self.results = []
		for table in self.tables:
			where = []

			for field in table.fields:
				if self.shouldInclude(arguements, field):
					where.append(f"{field.name} {arguements.equality} :search")
         
			if len(where):
				self.results.append(Result(
					cursor.execute(f"select * from {table.name} where " + " or ".join(where), (arguements.search,)).fetchall(),
					table.name
				))
    
		cursor.close()

