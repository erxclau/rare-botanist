import json
import os
from datetime import datetime

import praw


def get_json(path):
    f = open(path)
    json_dict = json.load(f)
    f.close()
    return json_dict


def get_reddit(subreddit):
    reddit = praw.Reddit(
        client_id=config['CLIENT_ID'],
        client_secret=config['CLIENT_SECRET'],
        user_agent=config['USER_AGENT'],
        username=config['USERNAME'],
        password=config['PASSWORD']
    )

    return reddit, reddit.subreddit(subreddit)


def create_review_thread(subreddit):
    today = datetime.now()
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


def close_thread(reddit, thread_id):
    submission = reddit.submission(id=thread_id)
    submission.mod.sticky(state=False)
    submission.mod.lock()


filepath = os.path.dirname(os.path.abspath(__file__))

thread_path = f"{filepath}/current-thread.json"

config = get_json(f"{filepath}/config.json")
current = get_json(thread_path)

reddit, subreddit = get_reddit('RHBST')

if not current['CURRENT_THREAD'] is None:
    close_thread(reddit, current['CURRENT_THREAD'])

thread = create_review_thread(subreddit)

current['CURRENT_THREAD'] = thread.id

with open(thread_path, 'w', encoding='utf-8') as file:
    json.dump(current, file, ensure_ascii=False, indent=2)

# TODO: Hook this up to a CRON job
