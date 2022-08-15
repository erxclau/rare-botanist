from utl import utility
from re import findall, match, sub

from praw.models.reddit.removal_reasons import RemovalReason, \
    SubredditRemovalReasons
from praw.reddit import Comment, Submission

config = utility.get_json("config.json")
flair_tiers: list[str] = config["USER_FLAIRS"]

thread_path = "current-thread.json"
current_thread = utility.get_json(thread_path)

data_path = "comment-data.json"
data = utility.get_json(data_path)

reddit, subreddit = utility.get_reddit(config)

SALE = "Bought"
TRADE = "Traded"

reason_ids: dict[str, str] = config["REMOVAL_REASONS"]
removal_reasons: SubredditRemovalReasons = subreddit.mod.removal_reasons

reasons = {
    key: removal_reasons[reason_ids[key]] for key in reason_ids.keys()
}


def remove_comment(c: Comment, reason: RemovalReason, type: str, note: str):
    try:
        c.mod.remove(reason_id=reason.id, mod_note=note)
        reply = c.mod.send_removal_message(
            reason.message,
            title=reason.title,
            type=type
        )
        return reply
    except Exception as e:
        print(e)
        return None


def bad_user_interact(c: Comment, name: str, reason: RemovalReason, note: str):
    cond = name.lower() in c.body.lower()
    if cond:
        remove_comment(c, reason, "private", note)
    return cond


def self_interact(c: Comment):
    return bad_user_interact(
        c, f"u/{c.author.name}", reasons["SELF_TRADE"],
        "User traded with themselves"
    )


def bot_interact(c: Comment):
    return bad_user_interact(
        c, f"u/{config['USERNAME']}", reasons["BOT_TRADE"],
        "User traded with bot"
    )


def wrong_num_interact(c: Comment):
    cond = len(findall(r"u\/\S+", c.body.lower())) != 1
    if cond:
        num_reason = reasons["ONE_USER"]
        reply: Comment = remove_comment(
            c, num_reason, "public", "User did not trade with exactly one user"
        )
        if reply is not None:
            reply.mod.lock()
    return cond


def bad_interact(c: Comment):
    return self_interact(c) or bot_interact(c) or wrong_num_interact(c)


def bad_format_check(text: str):
    text = sub(r"\s{2,}", " ", text).strip()
    sale_regex = r"^bought \w+.+ from (\/?u\/\S+|\[\/?u\/\S+\]\(\S+\))"
    trade_regex = r"^traded \w+.+ with (\/?u\/\S+|\[\/?u\/\S+\]\(\S+\))"

    sale_match = match(sale_regex, text) is not None
    trade_match = match(trade_regex, text) is not None
    return not (sale_match or trade_match)


def is_deleted(c: Comment) -> bool:
    return "[deleted]" == c.body.lower()


def bad_format(c: Comment):
    cond = bad_format_check(c.body.lower())
    if cond:
        format_reason = reasons["FORMAT"]
        reply: Comment = remove_comment(
            c, format_reason, "public", "User did not follow format"
        )
        if reply is not None:
            reply.mod.lock()
    return cond


def append_comment_thread(parent: Comment):
    comments: list[Comment] = list()
    comments.append(parent)
    for second_level_reply in parent.replies:
        comments.append(second_level_reply)
    return comments


def generate_comment_list(thread: Submission):
    comments: list[Comment] = list()
    comment_filter: list[str] = current_thread["CONFIRMED_TRADES"] + \
        current_thread["REMOVED_COMMENTS"]

    thread.comments.replace_more(limit=None)
    for c in thread.comments:
        if c.id not in comment_filter:
            if c.removed or is_deleted(c) or bad_format(c) or bad_interact(c):
                print(c.id, c.body.lower())
                current_thread["REMOVED_COMMENTS"].append(c.id)
            else:
                comments.extend(
                    append_comment_thread(c)
                )
    return comments


def get_parent(c: Comment):
    parent: Comment = c.parent()
    while not parent.is_root:
        parent = parent.parent()
    return parent


def lock_comment_thread(parent: Comment):
    queue = [parent]
    locked: list[Comment] = list()
    while queue:
        c = queue.pop(0)
        c.mod.lock()
        locked.append(c)
        queue[0:0] = c.replies
    return locked


def is_confirmation_comment(c: Comment):
    return not c.is_root and "confirmed" in c.body.lower()


def update_data_val(key: str, link: str, interaction: str):
    secondary_key = "sales" if interaction == SALE else "trades"
    if key not in data:
        data[key] = {
            "sales": 1 if interaction == SALE else 0,
            "trades": 1 if interaction == TRADE else 0,
            "history": list(),
            "update_flair": True
        }
    else:
        current = data[key]["sales"] + data[key]["trades"]
        if current == 10 or current == 20 or current == 50:
            data[key]["update_flair"] = True
        data[key][secondary_key] += 1
    data[key]["history"].append({
        "type": "Sale" if interaction == SALE else "Trade",
        "link": f"https://www.reddit.com{link}"
    })


def update_flair(name: str):
    interactions = data[name]["trades"] + data[name]["sales"]
    if data[name]["update_flair"]:
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
        data[name]["update_flair"] = False


def update_interactions(text: str, parent: Comment, comment: Comment):
    link: str = parent.permalink
    if text.startswith(TRADE.lower()):
        update_data_val(parent.author.name, link, TRADE)
        update_data_val(comment.author.name, link, TRADE)
        update_flair(parent.author.name)

    elif text.startswith(SALE.lower()):
        update_data_val(comment.author.name, link, SALE)

    update_flair(comment.author.name)


def validate_trade(comment: Comment, parent: Comment):
    text: str = parent.body.lower().strip()

    pname: str = parent.author.name
    cname: str = comment.author.name

    message = "Your review has been added" if text.startswith(SALE.lower()) \
        else f"A review has been added for u/{pname} and u/{cname}"

    reply = comment.reply(message)
    reply.mod.lock()
    current_thread["CONFIRMED_TRADES"].append(parent.id)

    update_interactions(text, parent, comment)


if __name__ == "__main__":
    comments: list[Comment] = list()
    if not current_thread["CURRENT_THREAD"] is None:
        thread = reddit.submission(id=current_thread["CURRENT_THREAD"])
        comments = generate_comment_list(thread)

    locked_comments: list[Comment] = list()
    for comment in comments:
        if is_confirmation_comment(comment):
            parent = get_parent(comment)
            if f"u/{comment.author.name}".lower() in parent.body.lower():
                if comment not in locked_comments:
                    validate_trade(comment, parent)
                    locked_comments.extend(
                        lock_comment_thread(parent)
                    )

    utility.write_json(thread_path, current_thread)
    utility.write_json(data_path, data)
