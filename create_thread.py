import json
import os
from datetime import datetime

import praw

filepath = os.path.dirname(os.path.abspath(__file__))

f = open(f"{filepath}/config.json")
config = json.load(f)
f.close()

today = datetime.now()

thread_title = f"{today.strftime('%B %Y')} Confimred Trade Thread"
thread_text = """Post your confirmed trades below!

When confirming a post, only write 'Confirmed'
"""

reddit = praw.Reddit(
    client_id=config['CLIENT_ID'],
    client_secret=config['CLIENT_SECRET'],
    user_agent=config['USER_AGENT'],
    username=config['USERNAME'],
    password=config['PASSWORD']
)

subreddit = reddit.subreddit('RHBST')

thread = subreddit.submit(
    thread_title,
    selftext=thread_text)

# TODO: Hook this up to a CRON job and set the current_thread
# in the database to be the thread.id

print(thread.id)