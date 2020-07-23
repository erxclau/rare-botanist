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
    "SUBREDDIT": ""
}
```

Encrypt `config.json` using the following command:

```bash
gpg --symmetric --cipher-algo AES256 json/config.json
```

On first use, `data.json` should look like the following:

```json
{

}
```
