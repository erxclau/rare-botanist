import json
import os

import praw

filepath = os.path.dirname(os.path.abspath(__file__))
json_dir = f"{filepath}/../../json"


def get_json(path):
    f = open(f"{json_dir}/{path}")
    json_dict = json.load(f)
    f.close()
    return json_dict


def write_json(path, content):
    with open(f"{json_dir}/{path}", 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=2)


def get_reddit(config):
    reddit = praw.Reddit(
        client_id=config['CLIENT_ID'],
        client_secret=config['CLIENT_SECRET'],
        user_agent=config['USER_AGENT'],
        username=config['USERNAME'],
        password=config['PASSWORD']
    )

    return reddit, reddit.subreddit(config['SUBREDDIT'])
