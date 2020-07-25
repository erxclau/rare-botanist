# rare-houseplants-bst-bot

## Description

This repository contains code for the bot on the [/r/RareHouseplantsBST](https://www.reddit.com/r/RareHouseplantsBST/) subreddit.

The robot uses the Python Reddit API Wrapper ([PRAW](https://praw.readthedocs.io/en/latest/)) to interact with Reddit. The robot also uses GitHub Actions workflows with cron schedules to run scripts.

## Robot Roles

### Create Review Thread

The bot will create a new review thread at the start of every month. This review thread post will have a 'Review Thread' flair and will also be pinned and distinguished. The previous month's thread will be unpinned and locked.

Relevant files: `create_thread.py`, `thread.yml`, `current_thread.json`

### Validate Confirmed Trades

The bot will reply to correctly formatted interactions in the review thread at the end of every day and appropriately update a log based on the interaction. These interactions will be locked after validation. If a user reaches a certain number of interactions, their flair will be updated. Comments that do not follow the rules will be removed.

Relevant files: `confirm_comments.py`, `comment.yml`, `current_thread.json`, `comment-data.json`

### Reply to BST Posts

The bot will continually respond to posts flaired with 'Buying', 'Selling', or 'Trading' with statistical comments based on the author.

Relevant files: `stat_reply`, `reply.yml`, `comment-data.json`

## Configuration

`config.json` has been encrypted using the following command:

```bash
gpg --symmetric --cipher-algo AES256 config.json
```

`config.json` should look like the following:

```json
{
    "CLIENT_ID": "",
    "CLIENT_SECRET": "",
    "USER_AGENT": "",
    "USERNAME": "",
    "PASSWORD": "",
    "REVIEW_FLAIR": "",
    "USER_FLAIRS": [],
    "POST_FLAIRS": [],
    "SUBREDDIT": "",
    "CUTOFF": ""
}
```

`CLIENT_ID`, `CLIENT_SECRET`, `USER_AGENT`, `USERNAME`, and `PASSWORD` are needed to interact with the Reddit API via PRAW. See the quick start guide [here](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html).

`REVIEW_FLAIR` is the Flair ID associated with the flair each review thread has.

`USER_FLAIRS` contains a list of Flair IDs associated with the flairs that users receive when they reach a certain number of validated interactions.

`POST_FLAIRS` contains a list of Flair IDs associated with the flairs that users put on Buying, Selling, or Trading posts.

`SUBREDDIT` is the name of the subreddit.

`CUTOFF` is the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date such that only posts after this date will be considered for receiving a statistics comment.
