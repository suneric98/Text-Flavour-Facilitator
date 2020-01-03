import praw
import datetime as dt
import pandas as pd
import re
import requests
import json
import time

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
    count = 0
    for submission in top:
        if re.search(RE_EMOJI, submission.selftext):
            data["titles"].append(submission.title)
            data["texts"].append(submission.selftext)
            count += 1
    print("Amount of data gathered:{}".format(count))
    return pd.DataFrame(data)

def scrape_subreddit_pushshift(sub, day = 10, size = "100"):
    data = {"titles":[], "texts":[]}
    hashedTitles = set()
    while day > 0:
        time.sleep(5)
        url = "https://api.pushshift.io/reddit/search/submission/?subreddit=" + sub + "&after=" + str(day) + "d&size=" + size
        resp = requests.get(url)
        jsonData = resp.json()["data"]
        count = 0
        for submission in jsonData:
            if "selftext" not in submission:
                continue
            if re.search(RE_EMOJI, submission["selftext"]) and submission["selftext"] not in hashedTitles:
                data["titles"].append(submission["title"])
                data["texts"].append(submission["selftext"])
                hashedTitles.add(submission["title"])
                count += 1
        day -= 1
        print("Day:{}, Amount of data gathered:{}".format(day, count))
    print("Total data size:{}".format(len(data["titles"])))
    return pd.DataFrame(data)

# df = scrape_subreddit("copypasta")
df = scrape_subreddit_pushshift("copypasta", 150, "100")
df.to_csv("data2.csv",index=False)