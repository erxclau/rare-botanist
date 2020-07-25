# rare-houseplants-bst-bot

## Description

This repository contains code for the bot on the [/r/RareHouseplantsBST](https://www.reddit.com/r/RareHouseplantsBST/) subreddit.

The robot uses the Python Reddit API Wrapper ([PRAW](https://praw.readthedocs.io/en/latest/)) to interact with Reddit. The robot also uses GitHub Actions workflows with cron schedules to continually run scripts.

## Robot Roles

- The robot creates a new review thread every month using `create_thread.py` and `thread.yml`.
- The robot logs and validates confirmed trades in the review at the end of every day using `confirm_comments.py` and `comment.yml`.
- The robot continually responds to flaired BST posts using `stat_reply.py` and `reply.yml`.
