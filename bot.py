import json
import os

import praw

filepath = os.path.dirname(os.path.abspath(__file__))

f = open(f"{filepath}/config.json")
config = json.load(f)
f.close()

reddit = praw.Reddit(
    client_id=config['CLIENT_ID'],
    client_secret=config['CLIENT_SECRET'],
    user_agent=config['USER_AGENT'],
    username=config['USERNAME'],
    password=config['PASSWORD']
)
