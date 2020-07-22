import os
from datetime import datetime

from utl import utility


filepath = os.path.dirname(os.path.abspath(__file__))

config = utility.get_json(f"{filepath}/../json/config.json")
current = utility.get_json(f"{filepath}/../json/current-thread.json")

reddit, subreddit = utility.get_reddit('RHBST', config)

thread = reddit.submission(id=current['CURRENT_THREAD'])

thread.comments.replace_more(limit=None)

comments = list()
comment_queue = thread.comments[:]
while comment_queue:
    comment = comment_queue.pop(0)
    # TODO: if the comment is in the list of added trades, do not do the next two lines
    comments.append(comment)
    comment_queue[0:0] = comment.replies

for comment in comments:
    if not comment.is_root and comment.body == 'Confirmed':
        parent = comment.parent()
        while not parent.is_root:
            parent = comment.parent()
        if f'u/{comment.author.name}' in parent.body:
            try:
                reply = comment.reply('Added!')
                reply.mod.lock()
            except:
                print('COULD NOT REPLY TO LOCKED COMMENT')
            queue = [parent]
            while queue:
                c = queue.pop(0)
                c.mod.lock()
                queue[0:0] = c.replies