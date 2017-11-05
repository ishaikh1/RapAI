import logging

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

from model import *


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def freestyle():
    rap = render_template('twothousand')
    return statement(rap)

@ask.intent("UselessIntent")
def tester():
	text = "If this works I'll streak across this fucking campus."
	return statement(text)


if __name__ == '__main__':
    app.run(debug=True)