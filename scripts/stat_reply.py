from datetime import datetime
from time import time

from utl import utility

start = time()

config = utility.get_json("config.json")
bot_name = config["USERNAME"].lower()

reply_path = "reply-data.json"
reply_data = utility.get_json(reply_path)

comment_data = utility.get_json("comment-data.json")

reddit, subreddit = utility.get_reddit(config)

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
CUTOFF = datetime.strptime(config["CUTOFF"], "%Y-%m-%d")


def already_replied(comments):
    replied = False
    for comment in comments:
        author = comment.author
        if author is not None and author.name.lower() == bot_name:
            replied = True
            break
    return replied


def is_valid_post(post):
    if post is not None:
        creation = datetime.fromtimestamp(post.created_utc)

        if creation > CUTOFF and post.id not in reply_data["POSTS"]:
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
    if len(reply_data["POSTS"]) == 100:
        reply_data["POSTS"].pop(0)
    reply_data["POSTS"].append(post_id)


def reply_with_stats(post):
    user = post.author

    sales = trades = 0
    if user.name in comment_data:
        sales = comment_data[user.name]["sales"]
        trades = comment_data[user.name]["trades"]

    creation_date = datetime.fromtimestamp(user.created_utc)

    reply = f"""Username: u/{user.name}

Overall karma: {user.link_karma + user.comment_karma}

Join date: {creation_date.isoformat().replace('T', ' ')}

Reputation: {sales} sale(s) and {trades} trade(s)"""
    try:
        post.reply(reply)
    except Exception:
        print("COULD NOT REPLY TO POST")


try:
    for post in subreddit.stream.submissions(pause_after=5):
        if time() - start >= 5 * HOUR + 45 * MINUTE:
            break

        if is_valid_post(post):
            fid = get_flair_id(post)

            if fid is not None and fid in config["POST_FLAIRS"]:
                if not already_replied(post.comments):
                    reply_with_stats(post)

            archive_post(post.id)
except Exception:
    print("STREAM ERROR")

utility.write_json(reply_path, reply_data)
