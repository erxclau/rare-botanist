import os
from datetime import datetime
from time import time
from pprint import pprint

from utl import utility

start = time()

filepath = os.path.dirname(os.path.abspath(__file__))
json_dir = f"{filepath}/../json"

config = utility.get_json(f"{json_dir}/config.json")

data_path = f"{json_dir}/reply-data.json"
data = utility.get_json(data_path)

reddit, subreddit = utility.get_reddit(config)

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
CUTOFF = datetime.strptime(config['CUTOFF'], '%Y-%m-%d')


def get_flair_id(post):
    flair_id = str()
    try:
        flair_id = post.link_flair_template_id
    except AttributeError:
        flair_id = None
    return flair_id


def archive_post(post_id):
    if len(data['POSTS']) == 100:
        data['POSTS'].pop(0)
    data['POSTS'].append(post_id)


def reply_with_stats(post):
    return


for post in subreddit.stream.submissions(pause_after=0):
    if time() - start >= 5 * HOUR + 55 * MINUTE:
        break

    if post is not None:
        creation = datetime.fromtimestamp(post.created_utc)

        if creation > CUTOFF and not post.id in data['POSTS']:
            flair_id = get_flair_id(post)

            if flair_id is not None and flair_id in config['POST_FLAIRS']:
                reply_with_stats(post)

            archive_post(post.id)

utility.write_json(data_path, data)
