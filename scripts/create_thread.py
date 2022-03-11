from datetime import datetime
from os.path import dirname, abspath

from utl import utility

config = utility.get_json("config.json")

thread_path = "current-thread.json"
current = utility.get_json(thread_path)

reddit, subreddit = utility.get_reddit(config)


def create_review_thread():
    today = datetime.now()
    thread_title = f"Review Thread – {today.strftime('%B %Y')}"
    thread_text = open(f"{dirname(abspath(__file__))}/../thread.txt").read()

    thread = subreddit.submit(
        thread_title,
        selftext=thread_text)

    thread.mod.distinguish(how="yes")
    thread.mod.sticky()
    thread.mod.flair(flair_template_id=config["REVIEW_FLAIR"])

    return thread


def close_thread(thread_id):
    submission = reddit.submission(id=thread_id)
    try:
        submission.mod.sticky(state=False)
        submission.mod.lock()
    except Exception:
        print("ATTEMPTED TO DELETE NONEXISTENT THREAD")


if not current["CURRENT_THREAD"] is None:
    close_thread(current["CURRENT_THREAD"])

thread = create_review_thread()

current = {
    "CURRENT_THREAD": thread.id,
    "CONFIRMED_TRADES": list(),
    "REMOVED_COMMENTS": list()
}

utility.write_json(thread_path, current)
