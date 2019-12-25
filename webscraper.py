import praw
import datetime as dt
import pandas as pd

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
        print(submission.title, submission.selftext)
        data["titles"].append(submission.title)
        data["texts"].append(submission.selftext)
    return pd.DataFrame(data)

df = scrape_subreddit("copypasta")
df.to_csv("data.csv",index=False)