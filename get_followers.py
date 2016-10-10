# -*- coding: utf-8 -*-


__author__ = 'Jordi Vilaplana'

import tweepy
import json
from pymongo import MongoClient


# Configuration parameters
database_host = ""
database_name = ""
database_collection = ""
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

client = None
db = None

if __name__ == '__main__':

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_host = config['database_host']
        database_name = config['database_name']
        database_collection = config['database_collection']
        access_token = config['access_token']
        access_token_secret = config['access_token_secret']
        consumer_key = config['consumer_key']
        consumer_secret = config['consumer_secret']

    # Connect to the MongoDB database
    client = MongoClient('mongodb://' + database_host + ':27017/')
    db = client[database_name]

    # Connect to the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    twitter_user_age_group_list = db[database_collection].find({"following": {"$exists": False}})

    print "Let's do this, we got " + str(twitter_user_age_group_list.count()) + " users to chew!"
    if twitter_user_age_group_list:
        for twitter_user_age_group in twitter_user_age_group_list:
            print "Working with the user @" + twitter_user_age_group['username']
            friends_ids = []
            #for twitter_friend in tweepy.Cursor(api.friends, screen_name=twitter_user_age_group['username']).items():
                #friends_ids.append(twitter_friend.screen_name)
            for page in tweepy.Cursor(api.followers_ids, screen_name=twitter_user_age_group['username']).pages():
                friends_ids.extend(page)

            twitter_user_age_group['following'] = friends_ids
            print "\tWe got " + str(len(friends_ids)) + " friends."
            db[database_collection].update({"_id": twitter_user_age_group['_id']}, twitter_user_age_group, upsert=True)

    print "We are done, bye!"
