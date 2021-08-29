from utl import utility
import re

config = utility.get_json("config.json")
flair_tiers = config['USER_FLAIRS']

thread_path = "current-thread.json"
current_thread = utility.get_json(thread_path)

data_path = "comment-data.json"
data = utility.get_json(data_path)

reddit, subreddit = utility.get_reddit(config)

SALE = 'Bought'
TRADE = 'Traded'

reason_ids = config['REMOVAL_REASONS']
removal_reasons = subreddit.mod.removal_reasons

reasons = {
    key: removal_reasons[reason_ids[key]] for key in reason_ids.keys()
}


def bad_user_interaction(comment, namecheck, reason, mod_note):
    if namecheck.lower() in comment.body.lower():
        comment.mod.remove(
            reason_id=reason.id,
            mod_note=mod_note
        )
        comment.mod.send_removal_message(
            reason.message,
            title=reason.title,
            type='private'
        )
        return True
    else:
        return False


def self_interact(comment):
    return bad_user_interaction(
        comment, f'u/{comment.author.name}',
        reasons['SELF_TRADE'], 'User traded with themselves'
    )


def bot_interact(comment):
    return bad_user_interaction(
        comment, f'u/{config["USERNAME"]}',
        reasons['BOT_TRADE'], 'User traded with bot'
    )


def wrong_num_interact(comment):
    text = comment.body.lower()
    user_match = re.findall(r'u\/\S+', text)
    if len(user_match) != 1:
        num_reason = reasons['ONE_USER']
        comment.mod.remove(
            reason_id=num_reason.id,
            mod_note='User did not trade with exactly one user'
        )
        reply = comment.mod.send_removal_message(
            num_reason.message,
            title=num_reason.title,
            type='public'
        )
        reply.mod.lock()
        return True
    else:
        return False


def bad_interact(comment):
    return self_interact(comment) \
        or bot_interact(comment) \
        or wrong_num_interact(comment)


def bad_format_check(text):
    sale_regex = r'^bought \w+.+ from (\/?u\/\S+|\[\/?u\/\S+\]\(\S+\))'
    trade_regex = r'^traded \w+.+ with (\/?u\/\S+|\[\/?u\/\S+\]\(\S+\))'

    sale_match = re.match(sale_regex, text) is not None
    trade_match = re.match(trade_regex, text) is not None
    return not (sale_match or trade_match)


def is_deleted(comment):
    text = comment.body.lower()
    return '[deleted]' == text


def bad_format(comment):
    text = comment.body.lower()
    if bad_format_check(text):
        format_reason = reasons['FORMAT']
        comment.mod.remove(
            reason_id=format_reason.id,
            mod_note='User did not follow format'
        )
        reply = comment.mod.send_removal_message(
            format_reason.message,
            title=format_reason.title,
            type='public'
        )
        reply.mod.lock()
        return True
    else:
        return False


def append_comment_thread(parent):
    comments = list()
    comments.append(parent)
    for second_level_reply in parent.replies:
        comments.append(second_level_reply)
    return comments


def generate_comment_list(thread):
    comments = list()
    comment_filter = current_thread['CONFIRMED_TRADES'] + \
        current_thread['REMOVED_COMMENTS']

    thread.comments.replace_more(limit=None)
    for c in thread.comments:
        if c.id not in comment_filter:
            if c.removed or is_deleted(c) or bad_format(c) or bad_interact(c):
                print(c.id, c.body.lower())
                current_thread['REMOVED_COMMENTS'].append(c.id)
            else:
                comments.extend(
                    append_comment_thread(c)
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


def update_data_val(key, link, interaction):
    secondary_key = 'sales' if interaction == SALE else 'trades'
    if key not in data:
        data[key] = {
            'sales': 1 if interaction == SALE else 0,
            'trades': 1 if interaction == TRADE else 0,
            'history': list(),
            'update_flair': True
        }
    else:
        current = data[key]['sales'] + data[key]['trades']
        if current == 10 or current == 20 or current == 50:
            data[key]['update_flair'] = True
        data[key][secondary_key] += 1
    data[key]['history'].append({
        'type': 'Sale' if interaction == SALE else 'Trade',
        'link': f'https://www.reddit.com{link}'
    })


def update_flair(name):
    interactions = data[name]['trades'] + data[name]['sales']
    if data[name]['update_flair']:
        tier = 0
        if interactions > 10:
            tier = 1
        if interactions > 20:
            tier = 2
        if interactions > 50:
            tier = 3
        subreddit.flair.set(
            name, flair_template_id=flair_tiers[tier]
        )
        data[name]['update_flair'] = False


def update_interactions(text, parent, comment):
    link = parent.permalink
    if text.startswith(TRADE.lower()):
        update_data_val(parent.author.name, link, TRADE)
        update_data_val(comment.author.name, link, TRADE)
        update_flair(parent.author.name)

    elif text.startswith(SALE.lower()):
        update_data_val(comment.author.name, link, SALE)

    update_flair(comment.author.name)


def validate_trade(comment, parent):
    text = parent.body.lower().strip()

    pname = parent.author.name
    cname = comment.author.name

    message = 'Your review has been added' if text.startswith(SALE.lower()) \
        else f'A review has been added for u/{pname} and u/{cname}'

    reply = comment.reply(message)
    reply.mod.lock()
    current_thread['CONFIRMED_TRADES'].append(parent.id)

    update_interactions(text, parent, comment)


comments = list()
if not current_thread['CURRENT_THREAD'] is None:
    thread = reddit.submission(id=current_thread['CURRENT_THREAD'])
    comments = generate_comment_list(thread)

locked_comments = list()
for comment in comments:
    if is_confirmation_comment(comment):
        parent = get_parent(comment)
        if f'u/{comment.author.name}'.lower() in parent.body.lower():
            if comment not in locked_comments:
                validate_trade(comment, parent)
                locked_comments.extend(
                    lock_comment_thread(parent)
                )

utility.write_json(thread_path, current_thread)
utility.write_json(data_path, data)
