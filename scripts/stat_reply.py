import os
from time import time

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

for submission in subreddit.stream.submissions(
    skip_existing=True,
    pause_after=0):
    if time() - start >= HOUR:
        break
    if submission is None:
        continue
    print(submission)

utility.write_json(data_path, data)
