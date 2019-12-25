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

subreddit = reddit.subreddit('emojipasta')