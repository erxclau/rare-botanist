from utl import utility

config = utility.get_json("test-config.json")
data = utility.get_json('comment-data.json')

reddit, subreddit = utility.get_reddit(config)

content = '''This is a comprehensive list of everyone who has traded and/or sold on r/RareHouseplantsBST.
Use Ctrl + F to find `u/username`.
'''

table_header = '''|Type|Comments|
|:---:|:---|
'''

keys = sorted(list(data.keys()), key=str.lower)

for user in keys:
    content += f'## {user}\n'
    content += table_header
    for interaction in data[user]['history']:
        content += f"|{interaction['type']}|{interaction['link']}|\n"
    content += '\n'

subreddit.wiki['userdirectory'].edit(
    content,
    'Update user directory'
)
