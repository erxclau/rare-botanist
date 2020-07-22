import os
from datetime import datetime

from utl import utility


filepath = os.path.dirname(os.path.abspath(__file__))

current_path = f"{filepath}/../json/confirmed-trades.json"

config = utility.get_json(f"{filepath}/../json/config.json")
current = utility.get_json(current_path)

reddit, subreddit = utility.get_reddit('RHBST', config)

thread = reddit.submission(id=current['CURRENT_THREAD'])

thread.comments.replace_more(limit=None)

comments = list()
for top_level in thread.comments:
    if not top_level.id in current['CONFIRMED_TRADES']:
        comments.append(top_level)
        for second_level in top_level.replies:
            comments.append(second_level)

locked_comments = list()

for comment in comments:
    if not comment.is_root and 'confirmed' in comment.body.lower():
        print('comment is not root')
        parent = comment.parent()
        while not parent.is_root:
            parent = parent.parent()
        if f'u/{comment.author.name}' in parent.body:
            # TODO: Prevent people from trading with themselves
            # Remove message and add removal reason as
            # 'You cannot trade with yourself'
            if not comment in locked_comments:
                print('this is a correct reply')
                try:
                    reply = comment.reply('Added!')
                    reply.mod.lock()
                    current['CONFIRMED_TRADES'].append(parent.id)
                except:
                    print('ATTEMPTED TO REPLY TO LOCKED COMMENT')
                queue = [parent]
                while queue:
                    print('locking all replies')
                    c = queue.pop(0)
                    c.mod.lock()
                    locked_comments.append(c)
                    queue[0:0] = c.replies

utility.write_json(current_path, current)