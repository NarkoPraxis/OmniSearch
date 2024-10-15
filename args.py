
class Arguements():
	fuzzySearch = False
	respondPublically = False
	caseInsensitive = False
	search = ''
	equality = '='
	email = False
	address = False
	name = False
	number = False
 
	def __init__(self, args):
		if "--" in args:
			args = args.split("--") 
			self.search = args[0].strip()
			commands = args[1]
		else: 
			self.search = args.strip()
   
		if commands:
			self.fuzzySearch 		= "f" in commands or "F" in commands
			self.respondPublically = "p" in commands or "P" in commands
			self.caseInsensitive 	= "s" in commands or "S" in commands
			self.email 		= "e" in commands or "E" in commands
			self.address 	= "a" in commands or "A" in commands
			self.name 		= "n" in commands or "N" in commands
			self.number 	= "#" in commands 
   
		if self.caseInsensitive or self.fuzzySearch:
			self.equality = "LIKE"
			
		if self.fuzzySearch:
			self.search = f"%{self.search}%"