import praw
import stdiomask
import json
import re
import requests

with open('config.json') as f:
    config = json.load(f)

reddit = praw.Reddit(client_id=config['client_id'],
                     client_secret=config['client_secret'],
                     user_agent="Reddit Top Downloader")

# todo get this from args
submissions = reddit.subreddit('houseplants').top(limit=3000, time_filter="all")

count = 0
for submission in submissions:
    count += 1
    file_name = re.findall("\\w+\\.png$|\\w+\\.jpg$", submission.url)
    if len(file_name) > 0:
        print(str(count) + ': ' + submission.url)
        r = requests.get(submission.url, allow_redirects=True)
        open('downloads2/'+file_name[0], 'wb').write(r.content)
