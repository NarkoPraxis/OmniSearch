import mysql.connector
import os
from args import Arguements

from database.base import Database
from result import Result


class MySqlDatabase(Database):
 
	def openConnection(self):
		self.connection = mysql.connector.connect(
			host=os.getenv("MYSQL_HOST"),
			user=os.getenv("MYSQL_USER"),
			password=os.getenv("MYSQL_PASSWORD"),
			database=self.name
		)
  
	def closeConnection(self):
		self.connection.close()
  
	def doQuery(self, arguements: Arguements):
		self.search = arguements.search
		cursor = self.connection.cursor()
  
		for table in self.tables:
			where = []
			count = 0
	
			for field in table.fields:
				if self.shouldInclude(arguements, field):
					count += 1
					where.append(f"{field.name} {arguements.equality} %s")

			if len(where):
				cursor.execute(f"select * from {table.name} where " + " or ".join(where), [arguements.search] * count)
				self.results.append(Result(cursor.fetchall(), table.name))
    
		cursor.close()
  
