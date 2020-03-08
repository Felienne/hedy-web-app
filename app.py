import hedy
import json
import os
import requests
from flask import request
from datetime import datetime
import jsonbin
import logging

# app.py
from flask import Flask, request, jsonify, render_template
from flask_compress import Compress

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)-8s: %(message)s')

app = Flask(__name__, static_url_path='')
Compress(app)
logger = jsonbin.JsonBinLogger.from_env_vars()

@app.route('/levels-text/', methods=['GET'])
def levels():
    level = request.args.get("level", None)

    #read levels from file
    try:
        file = open("levels.json", "r")
        contents = str(file.read())
        response = (json.loads(contents))
        file.close()
    except Exception as E:
            print(f"error opening level {level}")
            response["Error"] = str(E)
    return jsonify(response)


@app.route('/parse/', methods=['GET'])
def parse():
    # Retrieve the name from url parameter
    code = request.args.get("code", None)
    level = request.args.get("level", None)

    log_to_jsonbin(code, level)

    # For debugging
    print(f"got code {code}")

    response = {}

    # Check if user sent code
    if not code:
        response["Error"] = "no code found, please send code."
    # is so, parse
    else:
        try:
            result = hedy.transpile(code, level)
            response["Code"] = result
        except Exception as E:
            print(f"error transpiling {code}")
            response["Error"] = str(E)

    return jsonify(response)


def log_to_jsonbin(code, level):
    # log all info to jsonbin
    data = {
        'ip': request.remote_addr,
        'date': str(datetime.now()),
        'level': level,
        'code': code
    }
    logger.log(data)

# @app.route('/post/', methods=['POST'])
# for now we do not need a post but I am leaving it in for a potential future

# routing to index.html
@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    level = request.args.get("level", 1)
    level = int(level)

    try:
        file = open("static/levels.json", "r")
        contents = str(file.read())
        response = (json.loads(contents))
        file.close()
    except Exception as E:
        print(f"error opening level {level}")
        response["Error"] = str(E)

    commands = ''
    maxlevel = 0
    for json_level in response:
        int_level = int(json_level['Level'])
        if int_level > maxlevel:
            maxlevel = int_level
        if int_level == level:
            commands = json_level['Commands']
            introtext = json_level['Intro_text']
            startcode = json_level['Start_code']

    next_level_available = level != maxlevel
    nextlevel = None
    if next_level_available:
        nextlevel = level + 1

    latest = 'March 7th'

    return render_template("index.html", startcode = startcode, introtext = introtext, level=level, nextlevel = nextlevel, commands = commands, latest = latest)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
