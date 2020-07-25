from datetime import datetime
from time import time

from utl import utility

start = time()

config = utility.get_json("config.json")

reply_path = "reply-data.json"
reply_data = utility.get_json(reply_path)

comment_data = utility.get_json("comment-data.json")

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

    sales = trades = 0
    if user.name in comment_data:
        sales = comment_data[user.name]['sales']
        trades = comment_data[user.name]['trades']

    creation_date = datetime.fromtimestamp(user.created_utc)

    reply = f"""Username: u/{user.name}

Overall karma: {user.link_karma + user.comment_karma}

Join date: {creation_date.isoformat().replace('T', ' ')}

Reputation: {sales} sales(s) and {trades} trade(s)"""
    try:
        post.reply(reply)
    except:
        print('COULD NOT REPLY TO POST')


for post in subreddit.stream.submissions(pause_after=0):
    # if time() - start >= 5 * HOUR + 58 * MINUTE:
    if time() - start >= 28 * MINUTE:
        break

    if is_valid_post(post):
        flair_id = get_flair_id(post)

        if flair_id is not None and flair_id in config['POST_FLAIRS']:
            reply_with_stats(post)

        archive_post(post.id)

utility.write_json(reply_path, reply_data)
