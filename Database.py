import json
from types import SimpleNamespace

class Database:
	name = ""
	tables = []
	
	def __init__(self, name):
		with open(name, "r") as f:
			database = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
  
		self.name = database.name
		self.tables = database.tables
  
  
