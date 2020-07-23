import os
from datetime import datetime

from utl import utility


filepath = os.path.dirname(os.path.abspath(__file__))
json_dir = f"{filepath}/../json"

config = utility.get_json(f"{json_dir}/config.json")

current_thread_path = f"{json_dir}/current-thread.json"
current_thread = utility.get_json(current_thread_path)

data_path = f"{json_dir}/data.json"
data = utility.get_json(data_path)


def bad_interaction(comment, namecheck, reason_id, mod_note):
    if namecheck.lower() in comment.body.lower():
        comment.mod.remove(
            reason_id=reason_id,
            mod_note=mod_note
        )
        return True
    else:
        return False


def self_interact(subreddit, comment):
    self_reason = subreddit.mod.removal_reasons[0]
    return bad_interaction(
        comment, f'u/{comment.author.name}',
        self_reason.id, 'User traded with themselves'
    )


def bot_interact(subreddit, comment):
    bot_reason = subreddit.mod.removal_reasons[1]
    return bad_interaction(
        comment, f'u/{config["USERNAME"]}',
        bot_reason.id, 'User traded with bot'
    )


def append_comment_thread(parent):
    comments = list()
    comments.append(parent)
    for second_level_reply in parent.replies:
        comments.append(second_level_reply)
    return comments


def generate_comment_list(subreddit, thread):
    comments = list()
    comment_filter = current_thread['CONFIRMED_TRADES']
    comment_filter.extend(current_thread['REMOVED_COMMENTS'])

    thread.comments.replace_more(limit=None)
    for top_level in thread.comments:
        if not top_level.id in comment_filter:
            if self_interact(subreddit, top_level) or bot_interact(subreddit, top_level):
                current_thread['REMOVED_COMMENTS'].append(top_level.id)
            else:
                comments.extend(
                    append_comment_thread(top_level)
                )
    return comments


def get_parent(comment):
    parent = comment.parent()
    while not parent.is_root:
        parent = parent.parent()
    return parent


def lock_comment_thread(parent):
    queue = [parent]
    locked = list()
    while queue:
        c = queue.pop(0)
        c.mod.lock()
        locked.append(c)
        queue[0:0] = c.replies
    return locked


def is_confirmation_comment(comment):
    return not comment.is_root and 'confirmed' in comment.body.lower()


def validate_trade(comment, parent):
    reply = comment.reply('Added!')
    reply.mod.lock()
    current_thread['CONFIRMED_TRADES'].append(parent.id)


reddit, subreddit = utility.get_reddit('RHBST', config)
thread = reddit.submission(id=current_thread['CURRENT_THREAD'])
comments = generate_comment_list(subreddit, thread)


locked_comments = list()
for comment in comments:
    if is_confirmation_comment(comment):
        parent = get_parent(comment)
        if f'u/{comment.author.name}'.lower() in parent.body.lower():
            if not comment in locked_comments:
                validate_trade(comment, parent)
                locked_comments.extend(
                    lock_comment_thread(parent)
                )

utility.write_json(current_thread_path, current_thread)
