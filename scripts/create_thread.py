from datetime import datetime

from utl import utility

config = utility.get_json("config.json")

thread_path = "current-thread.json"
current = utility.get_json(thread_path)

reddit, subreddit = utility.get_reddit(config)


def create_review_thread():
    today = datetime.now()
    thread_title = f"{today.strftime('%B %Y')} Confirmed Review Thread"
    thread_text = """Post your confirmed trades below!

Begin your comments either with 'Bought from' or 'Traded with'. If you don't, your comment will be deleted!
Also include a `u/USERNAME` in your comment.

When confirming a comment, only write 'Confirmed'."""

    thread = subreddit.submit(
        thread_title,
        selftext=thread_text)

    thread.mod.distinguish(how="yes")
    thread.mod.sticky()
    thread.mod.flair(flair_template_id=config['REVIEW_FLAIR'])

    return thread


def close_thread(thread_id):
    submission = reddit.submission(id=thread_id)
    try:
        submission.mod.sticky(state=False)
        submission.mod.lock()
    except:
        print('ATTEMPTED TO DELETE NONEXISTENT THREAD')


if not current['CURRENT_THREAD'] is None:
    close_thread(current['CURRENT_THREAD'])

thread = create_review_thread()

current = {
    'CURRENT_THREAD': thread.id,
    'CONFIRMED_TRADES': list(),
    'REMOVED_COMMENTS': list()
}

utility.write_json(thread_path, current)
