import praw
import datetime as dt
import pandas as pd
import re
import requests
import json
import time
import emoji

RE_EMOJI = emoji.get_emoji_regexp()
RE_WORDS = r"\w+"

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
            selftext = submission["selftext"]
            if re.search(RE_EMOJI, selftext) and selftext not in hashedTitles:
                data["titles"].append(submission["title"])
                data["texts"].append(selftext)
                hashedTitles.add(submission["title"])
                count += 1
        day -= 1
        print("Day:{}, Amount of data gathered:{}".format(day, count))
    print("Total data size:{}".format(len(data["titles"])))
    return pd.DataFrame(data)

def clean_dataset(path):
    data = pd.read_csv(path)
    dropping = []
    for i in range(len(data["texts"])):
        text = data["texts"][i]
        numWords = len(re.findall(RE_WORDS, text)) + 1
        numEmojis = len(re.findall(RE_EMOJI, text)) + 1
        ratio = numEmojis / numWords
        if ratio > 3 or ratio < 0.05:
            dropping.append(i)
            # print(text)
    for drop in dropping:
        data = data.drop([drop], axis=0)
    print("Total data size:{}".format(len(data["titles"])))
    return data

# df = scrape_subreddit_pushshift("copypasta", 150, "100")
# df.to_csv("data3.csv",index=False)
# df = clean_dataset("data2.csv")
# df.to_csv("data3.csv", index=False)