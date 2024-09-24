import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from slackeventsapi import SlackEventAdapter
from weather import get_current_weather
import sqlite3


load_dotenv()

app = Flask(__name__)
# slack_event_adapter = SlackEventAdapter(signing_secret=os.getenv("SIGNING_SECRET"), endpoint = "/slack/events/", server= app)

# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path = env_path)

# client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))

BOT_ID = client.api_call("auth.test")["user_id"]


# @slack_event_adapter.on("message")
# def message(payload):
# 	event = payload.get("event", {})
# 	print("event: ", event)
# 	channel_id = event.get("channel")
# 	user_id = event.get("user")
# 	text = event.get("text")

# 	if BOT_ID != user_id:
# 		client.chat_postMessage(channel="#slack-bot", text=text )

# 	return Response(), 200

@app.route("/weather", methods=["POST"])
def get_weather():
    city = request.form.get("text")

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data["cod"] == 200:
        return render_template("city-not-found.html")

    template = render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )
    
    message = f""
    
    client.chat_postMessage(channel="#slack-bot", text=template )
    return Response(), 200

    

# TODO: Implement customer table query as well as user
# TODO: Provide arguements for targeting specific columns
# TODO: Provide arguments for fuzzy search (case insensitive and/or like %search%)
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

    connection = sqlite3.connect("playground.db")
    cursor = connection.cursor()
    
    firstName = search
    lastName = search
    if fuzzySearch:
        search = f"%{search}%"
        firstName = search
        lastName = search
    
    if "@" in search:
        userWhere = f"email {equality} :search"
    elif search.isnumeric():
        if len(search) == 10:
            userWhere = f"phone {equality} :search"
        else:
            userWhere = f"id {equality} :search or zip {equality} :search"
    else:     
        userWhere = f"first_name {equality} :firstName or last_name {equality} :lastName or email {equality} :search or street_address {equality} :search or city {equality} :search or state {equality} :search"
        if search.count(" ") == 1:
            userWhere = userWhere.replace("or", "and", 1) #require first and last name to match
            names = search.split() 
            firstName = names[0]
            lastName = names[1]
            if fuzzySearch:
                firstName = f"%{firstName}%"
                lastName = f"%{lastName}%"


    companyWhere = ""
    if search.isnumeric(): 
        companyWhere = f"id {equality} :search"
    elif "@" in search:
        companyWhere = f"email {equality} :search"
    else:
        companyWhere = f"name {equality} :search"
    
    userResults  = cursor.execute(f"select * from users where {userWhere}", {"search": search, "firstName": firstName, "lastName": lastName}).fetchall()
    companyResults = cursor.execute(f"select * from company where {companyWhere}", {"search": search}).fetchall()
    maxListSize = 5 # setting small max to avoid spamming slack with walls of text

    userCount = len(userResults)
    companyCount = len(companyResults)
    
    if userCount or companyCount:
        message = f"Searching for \"{search}\":\n"
        if userCount > 0:
            message += f"found {userCount} user"
            if (userCount > 1):
                message += "s"
            if userCount > maxListSize:
                message += f", showing {maxListSize}"
                
            message += "\n```"
            for row in userResults[:maxListSize]:
                message += str(row) + "\n"
            message += "```\n"
                
        if companyCount > 0:
            message += f"found {companyCount} company"
            if companyCount > 1:
                message = message.replace("company", "companies")
            if companyCount > maxListSize:
                message += f", showing {maxListSize}"
                
            message += "\n```"
            for row in companyResults[:maxListSize]:
                message += str(row) + "\n"
            message += "```"
    else:
        message = "No results found."
        
    if respondPublically:
        client.chat_postMessage(channel="#slack-bot", text=message )
    else:
        client.chat_postEphemeral(channel="#slack-bot", user=userId, text=message)

    # cursor = connection.cursor()
    connection.close()
    return Response(), 200



if __name__ == "__main__":
	app.run(debug=True)