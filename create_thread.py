import json
import os
from datetime import datetime

import praw

filepath = os.path.dirname(os.path.abspath(__file__))


def get_json(path):
    f = open(path)
    json_dict = json.load(f)
    f.close()
    return json_dict


def get_subreddit(subreddit):
    reddit = praw.Reddit(
        client_id=config['CLIENT_ID'],
        client_secret=config['CLIENT_SECRET'],
        user_agent=config['USER_AGENT'],
        username=config['USERNAME'],
        password=config['PASSWORD']
    )

    return reddit.subreddit(subreddit)


def create_review_thread(subreddit):
    thread_title = f"{today.strftime('%B %Y')} Confimred Trade Thread"
    thread_text = """Post your confirmed trades below!

    When confirming a post, only write 'Confirmed'
    """

    thread = subreddit.submit(
        thread_title,
        selftext=thread_text)

    thread.mod.distinguish(how="yes")
    thread.mod.sticky()
    thread.mod.flair('Review Thread')

    return thread


config = get_json(f"{filepath}/config.json")
current_thread = get_json(f"{filepath}/current-thread.json")

today = datetime.now()

subreddit = get_subreddit('RHBST')

thread = create_review_thread(subreddit)

# TODO: Hook this up to a CRON job and set the current_thread
# in the database to be the thread.id

print(thread.id)
