from json import load, dump
from os.path import dirname, abspath

from praw import Reddit

JSON_DIR = f"{dirname(abspath(__file__))}/../../json"


def get_json(path: str):
    f = open(f"{JSON_DIR}/{path}")
    json_dict: dict = load(f)
    f.close()
    return json_dict


def write_json(path: str, content: dict):
    with open(f"{JSON_DIR}/{path}", "w", encoding="utf-8") as file:
        dump(content, file, ensure_ascii=False, indent=2)


def get_reddit(config: dict):
    reddit = Reddit(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        user_agent=config["USER_AGENT"],
        username=config["USERNAME"],
        password=config["PASSWORD"]
    )

    return reddit, reddit.subreddit(config["SUBREDDIT"])
