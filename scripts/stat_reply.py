import os
from datetime import datetime
from time import time
from pprint import pprint

from utl import utility

start = time()

filepath = os.path.dirname(os.path.abspath(__file__))
json_dir = f"{filepath}/../json"

config = utility.get_json(f"{json_dir}/config.json")

reply_data_path = f"{json_dir}/reply-data.json"
reply_data = utility.get_json(reply_data_path)

comment_data = utility.get_json(f"{json_dir}/comment-data.json")

reddit, subreddit = utility.get_reddit(config)

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
CUTOFF = datetime.strptime(config['CUTOFF'], '%Y-%m-%d')


def is_valid_post(post):
    if post is not None:
        creation = datetime.fromtimestamp(post.created_utc)

        if creation > CUTOFF and not post.id in reply_data['POSTS']:
            return True
    return False


def get_flair_id(post):
    flair_id = str()
    try:
        flair_id = post.link_flair_template_id
    except AttributeError:
        flair_id = None
    return flair_id


def archive_post(post_id):
    if len(reply_data['POSTS']) == 100:
        reply_data['POSTS'].pop(0)
    reply_data['POSTS'].append(post_id)


def reply_with_stats(post):
    user = post.author
    data = comment_data[user.name]
    interactions = data['sales'] + data['trades']
    creation_date = datetime.fromtimestamp(user.created_utc)

    reply = f"""Username: u/{user.name}
Join date: {creation_date.isoformat().replace('T', ' ')}
Reputation: {interactions} interaction(s)"""
    print(reply)


for post in subreddit.stream.submissions(pause_after=0):
    if time() - start >= 5 * HOUR + 55 * MINUTE:
        break

    if is_valid_post(post):
        flair_id = get_flair_id(post)

        if flair_id is not None and flair_id in config['POST_FLAIRS']:
            reply_with_stats(post)

        archive_post(post.id)

utility.write_json(reply_data_path, reply_data)
