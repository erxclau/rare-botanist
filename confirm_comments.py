import json
import os
from datetime import datetime

import praw

from utl import utility


filepath = os.path.dirname(os.path.abspath(__file__))

config = utility.get_json(f"{filepath}/config.json")
current = utility.get_json(f"{filepath}/current-thread.json")

today = datetime.now()

reddit, subreddit = utility.get_reddit('RHBST', config)

thread = reddit.submission(id=current['CURRENT_THREAD'])

# thread.comments.replace_more(limit=None)

# comment_queue = thread.comments[:]  # Seed with top-level
# while comment_queue:
#     comment = comment_queue.pop(0)
#     print(comment.body)
#     comment_queue[0:0] = comment.replies
