# -*- coding: utf-8 -*-


__author__ = 'Jordi Vilaplana'

import tweepy
import json
import logging
from time import sleep
from random import randint

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

    users_survey_link_sent = []
    file_users_survey_link_sent = open('data/users_survey_link_sent.txt', 'r')
    for user in file_users_survey_link_sent:
        users_survey_link_sent.append(user.strip())
    file_users_survey_link_sent.close()

    users_to_send = []
    file_users_to_send = open('data/cat_users_raw_select_to_send.csv', 'r')
    for user in file_users_to_send:
        users_to_send.append(user.strip())
    file_users_to_send.close()

    print "users_survey_link_sent: " + str(len(users_survey_link_sent))
    print "users_to_send: " + str(len(users_to_send))

    file_users_survey_link_sent = open('data/users_survey_link_sent.txt', 'a')

    counter = 0
    for user in tweepy.Cursor(api.followers, screen_name="e_movix").items():
        if counter > 7:
            print "7 consecutive requests, let's not test our luck and stop here."
            break
        if user.screen_name in users_to_send and user.screen_name not in users_survey_link_sent:
            try:
                print "Sending DM to " + user.screen_name
                api.send_direct_message(screen_name=user.screen_name, text=u"Hola @" + user.screen_name + u", des del projecte #eMOVIX estem fent un estudi dels usuaris Catalans a Twitter, podries respondre aquesta pregunta anònima sobre la teva edat? Moltes gràcies: http://emovix.udl.cat/main/twitterSurveyLink/" + user.screen_name)
                file_users_survey_link_sent.write(user.screen_name + '\n')
                counter += 1
                sleep(randint(1, 5))
            except tweepy.error.TweepError as e:
                print "[ERROR] Could not send DM to user " + user.screen_name
                print e
                continue

    file_users_survey_link_sent.close()
