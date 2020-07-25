# rare-houseplants-bst-bot

This repository contains code for the bot on the RareHouseplantsBST subreddit.

On first use, `current-thread.json` should look like the following:

```json
{
    "CURRENT_THREAD": null,
    "CONFIRMED_TRADES": [],
    "REMOVED_COMMENTS": []
}
```

On first use, `comment-data.json` should look like the following:

```json
{ }
```

On first use, `reply-data.json` should look like the following:

```json
{
    "REPLIES": [],
    "CUTOFF": ""
}
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
    "SUBREDDIT": "",
}
```

Encrypt `config.json` using the following command:

```bash
gpg --symmetric --cipher-algo AES256 json/config.json
```
