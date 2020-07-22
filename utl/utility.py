import json

import praw


def get_json(path):
    f = open(path)
    json_dict = json.load(f)
    f.close()
    return json_dict


def get_reddit(subreddit, config):
    reddit = praw.Reddit(
        client_id=config['CLIENT_ID'],
        client_secret=config['CLIENT_SECRET'],
        user_agent=config['USER_AGENT'],
        username=config['USERNAME'],
        password=config['PASSWORD']
    )

    return reddit, reddit.subreddit(subreddit)
