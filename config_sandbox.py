from args import Arguements
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request

from config_reader import Config_Reader
from result import Result
import sys

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
	
	if not bool(args.strip()):
		client.chat_postEphemeral(channel="#slack-bot", user=userId, text="Please provide a valid query")
		return Response(), 200 
  
	if __name__ == "__main__" and len(sys.argv) > 1:
		configPath = sys.argv[1]
	else:
		configPath = "config.json"
  
	arguements = Arguements(args)
	database = Config_Reader(configPath).databaseFactory()
	message = database.omniSearch(arguements)

	if arguements.respondPublically:
		client.chat_postMessage(channel=database.channel, text=message )
	else:
		client.chat_postEphemeral(channel=database.channel, user=userId, text=message)

	return Response(), 200



# starts the server in debug mode (prevents needing to restart it whenever code changes are made)
if __name__ == "__main__":
	app.run(debug=True)