import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
import sqlite3
from database import Database 
from result import Result

load_dotenv()

app = Flask(__name__)

client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))

BOT_ID = client.api_call("auth.test")["user_id"]

@app.route("/weather", methods=["POST"])

# TODO: Provide arguements for targeting specific columns
@app.route("/omni", methods=["POST"])
def get_omni():
	args = request.form.get("text")
	userId = request.form.get("user_id")
	
	respondPublically = False
	caseInsensitive = False
	fuzzySearch = False

	if not bool(args.strip()):
		client.chat_postEphemeral(channel="#slack-bot", user=userId, text="Please provide a valid query")
		return Response(), 200 
	
	commands = ""
	equality = "="
	
	if "--" in args:
		args = args.split("--") 
		search = args[0].strip()
		commands = args[1]
	else: 
		search = args.strip()
		
	if commands:
		fuzzySearch =       ("f" in commands or "F" in commands)
		respondPublically = ("p" in commands or "P" in commands)
		caseInsensitive =   ("s" in commands or "S" in commands)
		
	if caseInsensitive or fuzzySearch:
		equality = "LIKE"
		
	database = Database("config.json")

	connection = sqlite3.connect(database.name)
	cursor = connection.cursor()
	
	firstName = search
	lastName = search
	
	if fuzzySearch:
		search = f"%{search}%"
		firstName = search
		lastName = search

	results = []
	for table in database.tables:
		where = []
 
		for field in table.fields:
			where.append(f"{field.name} {equality} :search")
			
		results.append(Result(
			cursor.execute(f"select * from {table.name} where " + " or ".join(where), {"search": search}).fetchall(),
			table.name
		))

	foundResult = False
	message = f"Searching for \"{search}\":\n"
	for result in results:
		count = len(result.data)
		if count:
			foundResult = True
			message += f"found {count} on the {result.tableName} table"
			if count > database.resultMax:
				message += f", showing {database.resultMax}"
					
			message += "\n```"
			for row in result.data[:database.resultMax]:
					message += str(row) + "\n"
			message += "```\n"

	if not foundResult:
		message = "No results found."
		
	if respondPublically:
		client.chat_postMessage(channel="#slack-bot", text=message )
	else:
		client.chat_postEphemeral(channel="#slack-bot", user=userId, text=message)

	connection.close()
	return Response(), 200



# starts the server in debug mode (prevents needing to restart it whenever code changes are made)
if __name__ == "__main__":
	app.run(debug=True)