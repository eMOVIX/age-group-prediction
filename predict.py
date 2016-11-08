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

    age_group_buffer = db['age_group_buffer'].find()

    twitterUserAgeGroup = db['twitterUserAgeGroup'].find({"following": {"$exists": True}})

    age_group_1 = []
    age_group_2 = []
    age_group_3 = []
    age_group_4 = []

    for twitter_user in twitterUserAgeGroup:
        if twitter_user['ageGroup'] == 1:
            age_group_1.extend(twitter_user['following'])
        elif twitter_user['ageGroup'] == 2:
            age_group_2.extend(twitter_user['following'])
        elif twitter_user['ageGroup'] == 3:
            age_group_3.extend(twitter_user['following'])
        elif twitter_user['ageGroup'] == 4:
            age_group_4.extend(twitter_user['following'])

    print "Let's do this, we got " + str(age_group_buffer.count()) + " users to chew!"
    if age_group_buffer:
        for age_group in age_group_buffer:
            print "Working with the user @" + age_group['username']
            friends_ids = []
            for page in tweepy.Cursor(api.followers_ids, screen_name=age_group['username']).pages():
                friends_ids.extend(page)

            score_1 = 0
            score_2 = 0
            score_3 = 0
            score_4 = 0

            for friend in friends_ids:
                if friend in age_group_1:
                    score_1 += 1
                elif friend in age_group_2:
                    score_2 += 1
                elif friend in age_group_3:
                    score_3 += 1
                elif friend in age_group_4:
                    score_4 += 1

            predicted = {}
            predicted['username'] = age_group['username']
            predicted['score_1'] = score_1
            predicted['score_2'] = score_2
            predicted['score_3'] = score_3
            predicted['score_4'] = score_4
            predicted['following'] = friends_ids

            total_score = score_1 + score_2 + score_3 + score_4

            n_score_1 = score_1 / total_score
            n_score_2 = score_2 / total_score
            n_score_3 = score_3 / total_score
            n_score_4 = score_4 / total_score

            d = {'1': n_score_1, '2': n_score_2, '3': n_score_3, '4': n_score_4}

            predicted['group'] = max(d, key=d.get)
            predicted['n_score'] = max(d)
            if max(d) > 50:
                predicted['certain'] = True
            else:
                predicted['certain'] = False

            db['age_group_predicted'].insert(predicted)

            db['age_group_buffer'].remove({"_id": age_group['_id']})

    print "We are done, bye!"
