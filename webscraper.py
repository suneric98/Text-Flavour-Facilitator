import praw
import datetime as dt
import pandas as pd
import re

RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')

client_id = "YOUR CLIENT ID"
client_secret = "SECRET"
user_agent = "APP NAME"
username = "USERNAME"
password = "PASSWORD"

reddit = praw.Reddit(client_id=client_id, \
    client_secret=client_secret, \
    user_agent=user_agent, \
    username=username, \
    password=password)

def scrape_subreddit(sub):
    subreddit = reddit.subreddit(sub)
    top = subreddit.top(limit=500)

    data = {"titles":[],"texts":[]}
    for submission in top:
        if re.search(RE_EMOJI, submission.selftext):
            print(submission.title, submission.selftext)
            data["titles"].append(submission.title)
            data["texts"].append(submission.selftext)
    return pd.DataFrame(data)

df = scrape_subreddit("copypasta")
df.to_csv("data.csv",index=False)