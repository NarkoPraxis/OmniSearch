import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from slackeventsapi import SlackEventAdapter
from weather import get_current_weather


load_dotenv()

app = Flask(__name__)
# slack_event_adapter = SlackEventAdapter(signing_secret=os.getenv('SIGNING_SECRET'), endpoint = '/slack/events/', server= app)

# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path = env_path)

# client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

client = slack.WebClient(token=os.getenv('SLACK_TOKEN'))

BOT_ID = client.api_call("auth.test")['user_id']


# @slack_event_adapter.on('message')
# def message(payload):
# 	event = payload.get('event', {})
# 	print('event: ', event)
# 	channel_id = event.get('channel')
# 	user_id = event.get('user')
# 	text = event.get('text')

# 	if BOT_ID != user_id:
# 		client.chat_postMessage(channel='#slack-bot', text=text )

# 	return Response(), 200

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

@app.route('/omni', methods=['POST'])
def get_omni():
	search = request.form.get('text')

	# Check for empty strings or string with only spaces
	if not bool(search.strip()):
		search = "Test"

	#do omni search
	print('Searching for: ', search)



	return Response(), 200



if __name__ == "__main__":
	app.run(debug=True)