from args import Arguements
from result import Result
from config_reader import Config_Reader

import slack
import os


#shared functionality between all databases
class Database():
	name = ""
	type = ""
	tables = []
	resultMax = 5
	channel = ""
	userId = ""
	connection = {}
	results = []
	search = ""
 
	def __init__(self, config: Config_Reader):  
		self.name = config.name
		self.type = config.type
		self.tables = config.tables
		self.resultMax = config.resultMax
		self.channel = config.channel
		self.userId = config.userId

	def openConnection(self):
		pass # implemented by child class
  
	def closeConnection(self):
		pass # implemented by child class

	def doQuery(self, arguements: Arguements):
		self.search = arguements.search
		cursor = self.connection.cursor()
  
		for table in self.tables:
			where = []
			count = 0
	
			for field in table.fields:
				if self.shouldInclude(arguements, field):
					count += 1
					if hasattr(field, 'type') and field.type == "number":
						where.append(f"CAST({field.name} AS TEXT) {arguements.equality} %s")
					else:
						where.append(f"{field.name} {arguements.equality} %s")

			if len(where):
				cursor.execute(f"select * from {table.name} where " + " or ".join(where), [arguements.search] * count)
				self.results.append(Result(cursor.fetchall(), table.name))
    
		cursor.close()
  
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

	def shouldInclude(self, arguements: Arguements, field):
		# if no arguements, return true
		include = True
		field = vars(field)
  
		# if arguements, return false unless type matches
		if arguements.email or arguements.name or arguements.address or arguements.number:
			include = False
   
		# if no type, return based on presence of arguments
		if "type" not in field:
			return include

		# include if arguement matches type
		if arguements.email and field["type"] == 'email':
			return True
		if arguements.name and field["type"] == 'name':
			return True
		if arguements.address and field["type"] == 'address':
			return True
		if arguements.number and field["type"] == 'number':
			return True

		return include
  
	def omniSearch(self, arguements: Arguements):
		self.openConnection()
		self.doQuery(arguements)
		self.sendSlackMessage(arguements.respondPublically, self.getMessage(self.results))
		self.closeConnection()
  
	def sendSlackMessage(self, respondPublically, message):
		client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))
		if respondPublically:
			client.chat_postMessage(channel=self.channel, text=message )
		else:
			client.chat_postEphemeral(channel=self.channel, user=self.userId, text=message)