#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from logging import raiseExceptions
import sys
import csv
import pandas as pd
import numpy as np

#http://www.tweepy.org/
import tweepy as tw

#Get your Twitter API credentials and enter them here
api_key = json.load(open('credentials.json'))
#method to get a user's last tweets
def get_tweets(username, number_of_tweets):
    # identification
	auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
	auth.set_access_token(api_key['access_key'], api_key['access_secret'])
	api = tw.API(auth) #If you wish to have the application sleep when 
    #it hits a rate limityou should instantiate the API with sleep_on_rate_limit=True

	#set count to however many tweets you want 
	number_of_tweets
    
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
    #Giving nb of rows to pre-allocate and be memory efficient
    df = pd.DataFrame(index=np.arange(0, number_of_tweets), columns=['id', 'date', 'text'])

    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth)
    #geo_code can be a parameter
    tweets = tw.Cursor(api.search,
              q=topic,
              lang="en",
              since=year+'-'+month+'-'+day, ).items(number_of_tweets)
    # results = tw.cursor()
    # results = api.search_tweets(keywords="vacation", limit=10)
    tweets_topics_csv = []
    for i, tweet in enumerate(tweets):
        #tweets_topics_csv.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])
        df.loc[i] = [tweet.id_str, tweet.created_at, tweet.text]

    #outfile = topic + "_tweets.csv"
    #print ("writing to " + outfile)

    # with open(outfile, 'w+') as file:
	#     writer = csv.writer(file, delimiter=',')
	#     writer.writerows(tweets_topics_csv)
    
    #df.to_csv("df_euro.csv", index=False)

    return df

def get_tweets_from_people(usernames,number_of_tweets):
    """
    """
    #Giving nb of rows to pre-allocate and be memory efficient
    df = pd.DataFrame(index=np.arange(0, len(usernames) * number_of_tweets), columns=['id', 'date', 'text'])
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth)
    #geo_code can be a parameter
    for k, username in enumerate(usernames):
        tweets = tw.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets)
    
        for i, tweet in enumerate(tweets):
            df.loc[k*number_of_tweets + i] = [tweet.user.name, tweet.created_at, tweet.text]

    return df

def get_tweets_dataframe(topics,year,month,day,number_of_tweets):
    """
    args : topics, year, month , day are Strings, number_of_tweets is an int
    year is like '2020', 'month' is among ['01',...'12'], same for days
    """
    #Giving nb of rows to pre-allocate and be memory efficient
    df = pd.DataFrame(index=np.arange(0, len(topics) * number_of_tweets), columns=['id', 'date', 'text'])

    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth)
    #geo_code can be a parameter
    for k, topic in enumerate(topics):
        try:
            tweets = tw.Cursor(api.search,
                    q=topic,
                    lang="en",
                    since=year+'-'+month+'-'+day, ).items(number_of_tweets)
        except: raiseExceptions("person not found")
    
        for i, tweet in enumerate(tweets):
            df.loc[k*number_of_tweets + i] = [tweet.id_str, tweet.user.name, tweet.created_at, tweet.text]

    return df

def list_manip():
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth)

    #my_list = api.create_list(name="influenceurs")    # id  1409134672387481600
    
    #api.add_list_members(list_id=1409134672387481600, screen_name=['stevenbjohnson', 'SecretLocDining', 'Malaytravelblog'])
    #for tweet in tw.Cursor(api.list_timeline, list_id=1409134672387481600, count=1, include_entities=False, include_rts=False).items(10):
    for tweet in tw.Cursor(api.user_timeline, screen_name = 'Malaytravelblog').items(4):
        print(tweet.user.screen_name)
        print(tweet.text)
        print("")

#if we're running this as a script
if __name__ == '__main__':
    # #alternative method: loop through multiple users
	# # users = ['user1','user2']
    number_of_tweets = 30
    #who = 'joebiden'
    #get_tweets(who, number_of_tweets)

    #topics = ["euro2021", "festival", "holidays"]
    #full_df = pd.DataFrame(index=np.arange(0, number_of_tweets * len(topics)), columns=['id', 'date', 'text'])
    #full_df = get_tweets_dataframe(topics, "2021","06","25",number_of_tweets)

    
    file = open("dict.json", "r")
    data = json.loads(file.read())
    topics = list(data.keys())
    for topic in topics:
        if topic =="tech_companies": #we have a problem with travel_blog
            
            print(topic)
            full_df = get_tweets_from_people(data[topic],30)
            
            full_df.to_csv("full_df"+str(topic)+'.csv', index=False)
            #faire à partir de tech_companies
            #Api dépassée
    file.close()
    #ok trop de requete -> recommencer ) après fashionistat , cad newspaper 
    #et rechercher à nouveau pour ["brain_food","foodies","travel","travel_mag"] car 30 pas assez