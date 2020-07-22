import os
from datetime import datetime

from utl import utility


filepath = os.path.dirname(os.path.abspath(__file__))

config = utility.get_json(f"{filepath}/../json/config.json")
current = utility.get_json(f"{filepath}/../json/current-thread.json")

reddit, subreddit = utility.get_reddit('RHBST', config)

thread = reddit.submission(id=current['CURRENT_THREAD'])

thread.comments.replace_more(limit=None)

comment_queue = thread.comments[:]
while comment_queue:
    comment = comment_queue.pop(0)
    print(comment.body, datetime.fromtimestamp(comment.created_utc), datetime.now())
    comment_queue[0:0] = comment.replies
