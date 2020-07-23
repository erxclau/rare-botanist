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

SALE = 'Bought from'
TRADE = 'Traded with'


def is_bad_interaction(comment, namecheck, reason_id, mod_note):
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
    return is_bad_interaction(
        comment, f'u/{comment.author.name}',
        self_reason.id, 'User traded with themselves'
    )


def bot_interact(subreddit, comment):
    bot_reason = subreddit.mod.removal_reasons[1]
    return is_bad_interaction(
        comment, f'u/{config["USERNAME"]}',
        bot_reason.id, 'User traded with bot'
    )


def bad_interaction(subreddit, comment):
    return self_interact(subreddit, comment) or bot_interact(subreddit, comment)


def bad_start(text):
    return not (text.startswith(SALE.lower()) or text.startswith(TRADE.lower()))


def bad_format(subreddit, comment):
    text = comment.body.lower()
    if bad_start(text) or 'u/' not in text:
        format_reason = subreddit.mod.removal_reasons[2]
        comment.mod.remove(
            reason_id=format_reason.id,
            mod_note='User did not follow format'
        )
        return True
    else:
        return False


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
            if bad_interaction(subreddit, top_level) or bad_format(subreddit, top_level):
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


def add_data_val(key, interaction):
    secondary_key = 'sales' if interaction == SALE else 'trades'
    if not key in data:
        data[key] = {
            'sales': 1 if interaction == SALE else 0,
            'trades': 1 if interaction == TRADE else 0
        }
    else:
        data[key][secondary_key] += 1


def update_data(text, parent_name, comment_name):
    if text.startswith(TRADE.lower):
        add_data_val(parent_name, TRADE)
        add_data_val(comment_name, TRADE)
    elif text.startswith(SALE.lower):
        add_data_val(comment_name, SALE)


def validate_trade(comment, parent):
    reply = comment.reply('Added!')
    reply.mod.lock()
    current_thread['CONFIRMED_TRADES'].append(parent.id)

    text = parent.body.lower()
    parent_name = parent.author.name
    comment_name = comment.author.name

    update_data(text, parent_name, comment_name)


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
