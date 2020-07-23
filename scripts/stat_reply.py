import os
from time import time

from utl import utility

start = time()

filepath = os.path.dirname(os.path.abspath(__file__))
json_dir = f"{filepath}/../json"

config = utility.get_json(f"{json_dir}/config.json")

reddit, subreddit = utility.get_reddit(config)

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE

for submission in subreddit.stream.submissions(
    skip_existing=True,
    pause_after=0):
    if time() - start > 1 * MINUTE:
        break
    if submission is None:
        continue
    print(submission)