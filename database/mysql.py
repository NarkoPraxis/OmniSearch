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


  
