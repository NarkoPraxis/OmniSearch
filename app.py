#!/bin/project

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index(): 
	return "Hello World, from Flask"


app.run(host="192.184.3.35", port=8000)