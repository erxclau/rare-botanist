# rare-houseplants-bst-bot

## Description

This repository contains code for the bot on the [/r/RareHouseplantsBST](https://www.reddit.com/r/RareHouseplantsBST/) subreddit.

The robot uses the Python Reddit API Wrapper ([PRAW](https://praw.readthedocs.io/en/latest/)) to interact with Reddit. The robot also uses GitHub Actions workflows with cron schedules to continually run scripts.

## Robot Roles

- The robot creates a new pinned review thread every month using `create_thread.py` and `thread.yml`.
- The robot logs and validates confirmed trades in the review thread at the end of every day using `confirm_comments.py` and `comment.yml`.
- The robot continually responds to flaired BST posts with author stats using `stat_reply.py` and `reply.yml`.

## Configuration

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
