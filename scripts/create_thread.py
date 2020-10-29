from datetime import datetime

from utl import utility

config = utility.get_json("config.json")

thread_path = "current-thread.json"
current = utility.get_json(thread_path)

reddit, subreddit = utility.get_reddit(config)


def create_review_thread():
    today = datetime.now()
    thread_title = f"Review Thread – {today.strftime('%B %Y')}"
    thread_text = """**Please read the required formatting carefully before posting your review comment.**

To review a trade or purchase, format your comment as follows:

- Bought anthurium crystallinum, hoya chelsea from `u/username`
- Traded philodendron pink princess with `u/username`

Limit your review comment to one `u/username` only. If your comment does not start with this specific format, it will be deleted.

If you would like to include images in your review, add it AFTER the required format:

- Bought philodendron atabapoense from `u/username` https://imgur.com/gallery/0rlZIq3

**To confirm a trade or purchase, only reply with "Confirmed"**

Things to note

- **Only one trade review is needed to document that a trade has occurred between two users. Both users will get a +1 trade in the user directory.**
- Please keep in mind that this is essentially a good/positive experience review thread. In the event there is a negative interaction, please view “[Trades Gone Wrong](https://www.reddit.com/r/RareHouseplantsBST/wiki/exchangegonewrong)” for possible conflict resolutions and DM the moderators with your concerns.
"""

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
