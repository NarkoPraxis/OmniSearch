# Omnisearch Slack App

An easy to use slack application that can fuzzy search an example database across multiple tables. 

See also 
Token Auth, Interactive Shell, Management Commands.

### REQUIREMENTS

- [Slack App](https://api.slack.com/apps/) You will need to create a Slack App in order to run this project
- [Remote Server](https://ngrok.com/) You will need a publically available endpoint for Slack to respond to. I use ngrok
- Python 3.8.1

**Installation Steps** 

1. Clone repo to your computer
2. Create a virtualenv and activate it
3. run `pip install -r requirements.txt` to install the project dependancies
4. run `python database_seeder.py` to create the sample database for testing
5. navigate to your [Slack App](https://api.slack.com/apps/)
	- create a slack app if you don't already have one
6. navigate to [Slash Commands](https://api.slack.com/apps/A07N8SJHNDA/slash-commands)
7. make a new slash command (I set the command as /omni with "search" as the usage hint)
8. start ngrok and use `ngrok http 5000` to start forwarding `https://localhost:5000` to a public endpoint
	- copy the port forwarding address. It should look similiar to: `https://00b2-192-184-3-35.ngrok-free.app`. 
	- paste the copied ngrok forwarding route into the url for your slash command
		- add `/omni` to the end of the ngrok route. This will send arguements from the command to the correct route on the server
	- save the slash command
9. duplicate the `.env.example` file and remove the `.example` to create a .env file
10. navigate to [Install App](https://api.slack.com/apps/A07N8SJHNDA/install-on-team?) and copy your Bot user OAuth Token
11. while on the [Install App](https://api.slack.com/apps/A07N8SJHNDA/install-on-team?) page, click the `Install to <SlackWorkspaceName>` button. (You might have to do this again later if steps are done out of order)
12. paste the Bot User OAuth Token as the value for the .env file's SLACK_TOKEN
13. navigate to [Basic Information](https://api.slack.com/apps/A07N8SJHNDA/general?) and copy your Signing Secret
14. paste it in as the value for the .env file's SIGNING_SECRET 

## Running the application

run `python config_sandbox.py` to run the server in debug mode. <br/>
   - this reads the included config.json file to connect to a sqlite or mysql database. Fill out the config correctly and the app should work with whatever schema you have. <br/>
	- add a file path as the first arguement to the config and you can now provide a config file that isn't named `config.json`

or run `python sandbox.py` to run the server in debug mode. <br/>
   - this utilizes the test database included in the repo.<br/>

If everything was done correctly, /omni search should be available as a command in your slack workspace.<br/>
It can take some time for slack to update the workspace with the installed app, so be a bit patient.<br/>

## Config file
+ `name`: The name of the sqlite .db file (or mysql database) with which to connect.<br/>
+ `type`: `mysql` or `sqlite` determines which kind of database connection should be attempted<br/>
+ `channel`: `#channel-name` of the channel where your bot should post replies and listen for commands
+ `resultMax`: the maximum number of results to return in the slack message<br/>
+ `tables`: the tables that should be searched<br/>
   + `name`: the name of the table<br/>
   + `fields`: the column names inside the table that should be searched<br/>
   	+ `field`: the column names<br/>
		+ `type`: the type of the column<br/>
			+ not currently used, may see support later<br/>

# MySql Configuration
The database `name` is still set in the configuration file.<br/>
the other connection information is filled out in the environment file</br>
`MYSQL_HOST=`</br>
`MYSQL_USER=`</br>
`MYSQL_PASSWORD=`</br>

## Usage

By default, /omni accepts any number of words or numbers as input and will use that input as a single, case-sensitive, query on an example database.

If desired, arguements can be passed in after the search parameter with the `--` sign.<br/>
+ `--f` will perform a fuzzy search by appending `%` to the front and back of a search term and using `LIKE` instead of `=` for comparison<br/>
+ `--p` will post the result into slack publically instead of keeping the result private<br/>
+ `--s` will perform the search as case insenstive by using `LIKE` instead of `=` for comparison<br/>

these arguements can be mixed and matched, so `--fps`, `--psf`, and `--pf` will also work. 

## TODO
1. move queries to background threads to accomodate large databases / queries
~~2. support multiple database connection methods, not just reading .db files~~
3. provide more usage options for when the user knows they have an email, full name, or address etc
	- should allow for more optimized fuzzy searchs
4. provide more options in config file for default behaviors.
	- right now "maxResults" is the only option, which controls how many results are returned inside slack. 
5. add postgress support
6. add ability to connect and query multiple database connections asynchronously