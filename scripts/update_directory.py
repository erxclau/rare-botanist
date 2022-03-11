from utl import utility
from os.path import dirname, abspath

config = utility.get_json("config.json")
data = utility.get_json('comment-data.json')

reddit, subreddit = utility.get_reddit(config)

content = open(f"{dirname(abspath(__file__))}/../userdir.txt").read()

table_header = """|Type|Comments|
|:---:|:---|
"""

keys = sorted(list(data.keys()), key=str.lower)

for user in keys:
    content += f"## {user}\n"
    content += table_header
    for interaction in data[user]["history"]:
        content += f"|{interaction['type']}|{interaction['link']}|\n"
    content += "\n"

subreddit.wiki["userdirectory"].edit(
    content,
    "Update user directory"
)
