from database.base import Database
import psycopg2
import os


class postgresSqlDatabase(Database):
 
	def openConnection(self):
		self.connection = psycopg2.connect(
			database=self.name,
			host=os.getenv("POSTGRESQL_HOST"),
			user=os.getenv("POSTGRESQL_USER"),
			password=os.getenv("POSTGRESQL_PASSWORD"),
			port=os.getenv("POSTGRESQL_PORT")
		)
  
	def closeConnection(self):
		self.connection.close()


