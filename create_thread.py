import json
import os
from datetime import datetime

from utl import utility


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
    try:
        submission.mod.sticky(state=False)
        submission.mod.lock()
    except:
        print('ATTEMPTED TO DELETE NONEXISTENT THREAD')


filepath = os.path.dirname(os.path.abspath(__file__))

config = utility.get_json(f"{filepath}/config.json")

thread_path = f"{filepath}/current-thread.json"
current = utility.get_json(thread_path)

reddit, subreddit = utility.get_reddit('RHBST', config)

if not current['CURRENT_THREAD'] is None:
    close_thread(reddit, current['CURRENT_THREAD'])

thread = create_review_thread(subreddit)

current['CURRENT_THREAD'] = thread.id

with open(thread_path, 'w', encoding='utf-8') as file:
    json.dump(current, file, ensure_ascii=False, indent=2)

# TODO: Hook this up to a CRON job
