from utl import utility 

config = utility.get_json("config.json")
flair_tiers = config['USER_FLAIRS']

thread_path = "current-thread.json"
current_thread = utility.get_json(thread_path)

data_path = "comment-data.json"
data = utility.get_json(data_path)

reddit, subreddit = utility.get_reddit(config)

SALE = 'Bought'
TRADE = 'Traded'


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


def update_data_val(key, link, interaction):
    secondary_key = 'sales' if interaction == SALE else 'trades'
    if not key in data:
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

    message = 'Your review has been added' if text.startswith(SALE.lower()) \
        else f'A review has been added for u/{parent.author.name} and u/{comment.author.name}'

    reply = comment.reply(message)
    reply.mod.lock()
    current_thread['CONFIRMED_TRADES'].append(parent.id)

    update_interactions(text, parent, comment)


child = reddit.comment(id="gwxd6ch")
parent = get_parent(child)

validate_trade(child, parent)
child.mod.lock()
lock_comment_thread(parent)

utility.write_json(thread_path, current_thread)
utility.write_json(data_path, data)
