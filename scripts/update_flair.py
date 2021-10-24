from utl import utility 

config = utility.get_json("config.json")
flair_tiers = config['USER_FLAIRS']

reddit, subreddit = utility.get_reddit(config)

subreddit.flair.set(
    'USERNAME', flair_template_id=flair_tiers[0]
)
