import json
import os
from datetime import datetime

import praw

filepath = os.path.dirname(os.path.abspath(__file__))

f = open(f"{filepath}/config.json")
config = json.load(f)
f.close()

today = datetime.now()

thread_title = f"{today.strftime('%B_%Y')}_confimred_trade_thread".lower()

print(thread_title)

reddit = praw.Reddit(
    client_id=config['CLIENT_ID'],
    client_secret=config['CLIENT_SECRET'],
    user_agent=config['USER_AGENT'],
    username=config['USERNAME'],
    password=config['PASSWORD']
)

subreddit = reddit.subreddit('RHBST')

thread_id = 'hufc3o'

# TODO: Read the current_thread in the database
# Set thread_id to the current_thread

thread = reddit.submission(id=thread_id)

thread.comments.replace_more(limit=None)

for top_level_comment in thread.comments:
    print(top_level_comment.body)