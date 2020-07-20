import json
import os
from datetime import datetime

import praw

filepath = os.path.dirname(os.path.abspath(__file__))

f = open(f"{filepath}/config.json")
config = json.load(f)
f.close()

today = datetime.now()

post_title = f"{today.strftime('%B %Y')} Confimred Trade Thread"
post_text = """Post your confirmed trades below!

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

subreddit.submit(
    post_title,
    selftext=post_text)