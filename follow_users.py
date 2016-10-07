# -*- coding: utf-8 -*-


__author__ = 'Jordi Vilaplana'

import tweepy
import json
import logging
import time
import datetime
import csv

logging.basicConfig(filename='emovix_twitter_search.log',level=logging.INFO)


# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

client = None
db = None

if __name__ == '__main__':
    logging.info('emovix_twitter_search.py starting ...')

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    followed_users = []

    with open('data/cat_users_sent.csv', 'r') as f:
        for line in f:
            followed_users.append(line.strip())
        f.close()

    with open('data/cat_users_raw_select_to_send.csv') as input, open('data/cat_users_sent.csv', 'a') as out:
    #with open('data/cat_users_raw_select_3_to_send.csv') as input, open('data/cat_users_sent.csv', 'wb') as out:
        writer = csv.writer(out)
        for line in input:
            username = line.strip()
            if username not in followed_users:
                try:
                    api.create_friendship(username)
                    out.write(username + '\n')
                except tweepy.error.TweepError as e:
                    print "[ERROR] Unable to follow user: " + username
                    print e
                    continue
