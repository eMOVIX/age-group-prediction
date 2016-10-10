# -*- coding: utf-8 -*-


__author__ = 'Jordi Vilaplana'

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

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

if __name__ == '__main__':

    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_host = config['database_host']
        database_name = config['database_name']
        database_collection = config['database_collection']

    # Connect to the MongoDB database
    client = MongoClient('mongodb://' + database_host + ':27017/')
    db = client[database_name]

    twitter_user_age_group_list = db[database_collection].find({"following": {"$exists": True}})

    youth_friends = []
    old_friends = []

    print "Let's do this, we got " + str(twitter_user_age_group_list.count()) + " users to chew!"
    if twitter_user_age_group_list:
        for twitter_user_age_group in twitter_user_age_group_list:

            if twitter_user_age_group['ageGroup'] == 4:
                old_friends.extend(twitter_user_age_group['following'])
            else:
                youth_friends.extend(twitter_user_age_group['following'])


    print "youth_friends: " + str(len(youth_friends))
    print "old_friends: " + str(len(old_friends))

    print "Removing duplicates ..."
    youth_friends = list(set(youth_friends))
    old_friends = list(set(old_friends))

    print "youth_friends: " + str(len(youth_friends))
    print "old_friends: " + str(len(old_friends))

    intersect_friends = intersect(youth_friends, old_friends)
    print "intersect: " + str(len(intersect_friends))


    youth_only = list(set(youth_friends) - set(intersect_friends))
    old_only = list(set(old_friends) - set(intersect_friends))

    print "youth_only: " + str(len(youth_only))
    print "old_only: " + str(len(old_only))
