#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import csv

#http://www.tweepy.org/
import tweepy as tw

#Get your Twitter API credentials and enter them here
api_key = json.load(open('credentials.json'))
#method to get a user's last tweets
def get_tweets(username):
    # identification
	auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
	auth.set_access_token(api_key['access_key'], api_key['access_secret'])
	api = tw.API(auth) #If you wish to have the application sleep when 
    #it hits a rate limityou should instantiate the API with sleep_on_rate_limit=True

	#set count to however many tweets you want 
	number_of_tweets = 20
    
	#get tweets
	tweets_for_csv = []
	for tweet in tw.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets):
        #create array of tweet information: username, tweet id, date/time, text
		tweets_for_csv.append([username, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])

	#write to a new csv file from the array of tweets
	outfile = username + "_tweets.csv"
	print ("writing to " + outfile)

	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(tweets_for_csv)



def get_tweets_per_topic(topic,year,month,day,number_of_tweets):
    """
    args : topic, year, month , day are Strings, number_of_tweets is an int
    year is like '2020', 'month' is among ['01',...'12'], same for days
    """

    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth)
    #geo_code can be a parameter
    tweets = tw.Cursor(api.search_tweets,
              q=topic,
              lang="en",
              since=year+'-'+month+'-'+day, ).items(number_of_tweets)
    # results = tw.cursor()
    # results = api.search_tweets(keywords="vacation", limit=10)
    tweets_topics_csv = []
    for tweet in tweets:
        tweets_topics_csv.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])

    outfile = topic + "_tweets.csv"
    print ("writing to " + outfile)

    with open(outfile, 'w+') as file:
	    writer = csv.writer(file, delimiter=',')
	    writer.writerows(tweets_topics_csv)

#if we're running this as a script
if __name__ == '__main__':
    # #alternative method: loop through multiple users
	# # users = ['user1','user2']
    get_tweets('joebiden')
    get_tweets_per_topic("plane","2021","05","01",20)
	# for user in users:
	# 	get_tweets(user)