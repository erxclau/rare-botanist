import os
from datetime import datetime

from utl import utility


def lock_comment_thread(parent):
    queue = [parent]
    locked = list()
    while queue:
        print('locking all replies')
        c = queue.pop(0)
        c.mod.lock()
        locked.append(c)
        queue[0:0] = c.replies
    return locked


filepath = os.path.dirname(os.path.abspath(__file__))

current_path = f"{filepath}/../json/current-thread.json"

config = utility.get_json(f"{filepath}/../json/config.json")
current = utility.get_json(current_path)

reddit, subreddit = utility.get_reddit('RHBST', config)

thread = reddit.submission(id=current['CURRENT_THREAD'])

thread.comments.replace_more(limit=None)

comment_filter = current['CONFIRMED_TRADES']
comment_filter.extend(current['REMOVED_COMMENTS'])

self_trade = subreddit.mod.removal_reasons[0]
bot_trade = subreddit.mod.removal_reasons[1]

def bad_trade(comment, namecheck, reason_id, mod_note):
    if namecheck.lower() in comment.body.lower():
        comment.mod.remove(
            reason_id = reason_id,
            mod_note = mod_note
        )
        return True
    else:
        return False

comments = list()
for top_level in thread.comments:
    if not top_level.id in comment_filter:
        if bad_trade(
            top_level, f'u/{top_level.author.name}',
            self_trade.id, 'User traded with themselves'
        ) or bad_trade(
            top_level, f'u/{config["USERNAME"]}',
            bot_trade.id, 'User traded with bot'
        ):
            current['REMOVED_COMMENTS'].append(top_level.id)
        else:
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
        author = comment.author.name
        if f'u/{author}'.lower() in parent.body.lower():
            if not comment in locked_comments:
                print('this is a correct reply')
                try:
                    reply = comment.reply('Added!')
                    reply.mod.lock()
                    current['CONFIRMED_TRADES'].append(parent.id)
                except:
                    print('ATTEMPTED TO REPLY TO LOCKED COMMENT')
                locked_comments.extend(
                    lock_comment_thread(parent)
                )

utility.write_json(current_path, current)
