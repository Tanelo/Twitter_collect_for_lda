#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import csv
import pandas as pd
import numpy as np

#http://www.tweepy.org/
import tweepy as tw

# The fields you can select on tweets are found here : 
# https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

# The fields you can select on users are found here : 
# https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user


#Get your Twitter API credentials and enter them here
api_key = json.load(open('credentials.json'))["second_key"]
#method to get a user's last tweets
def get_tweets(username, number_of_tweets):
    # identification
	auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
	auth.set_access_token(api_key['access_key'], api_key['access_secret'])
	api = tw.API(auth) #If you wish to have the application sleep when 
    #it hits a rate limityou should instantiate the API with sleep_on_rate_limit=True

	#set count to however many tweets you want 
	number_of_tweets = number_of_tweets
    
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
    tweets = tw.Cursor(api.search_tweets,
              q=topic,
              lang="en",
              since=year+'-'+month+'-'+day, ).items(number_of_tweets)
    tweets_topics_csv = []
    for i, tweet in enumerate(tweets):
        #tweets_topics_csv.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])
        df.loc[i] = [tweet.id_str, tweet.created_at, tweet.text]

    return df

def get_tweets_from_people(usernames,number_of_tweets):
    """
    """
    #Giving nb of rows to pre-allocate and be memory efficient
    df = pd.DataFrame(index=np.arange(0, len(usernames) * number_of_tweets), columns=['id', 'date', 'text','retweet_count'])
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth,wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
    #geo_code can be a parameter
    for k, username in enumerate(usernames):
        try: 
            tweets = tw.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets)
    
            for i, tweet in enumerate(tweets):
                df.loc[k*number_of_tweets + i] = [tweet.user.name, tweet.created_at, tweet.text, tweet.retweet_count]
        except:
            print("\n....There has beenproblem with the name of one twittos in the list...")
            pass


            

    return df

def get_tweets_with_comments(usernames,number_of_tweets):
    df = pd.DataFrame(index=np.arange(0, len(usernames) * number_of_tweets), columns=['id','name', 'date', 'text','comments','retweet_count'])
    #comments is a list
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth,wait_on_rate_limit=True,
    )
    for k, username in enumerate(usernames):
        try: 
            tweets = tw.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets)
    
            for i, tweet in enumerate(tweets):
                name = str(tweet.user.name)
                tweet_id = tweet.id
                replies=[]
                if tweet.is_quote_status:
                    print("is quote")

                    
                    for comment in tw.Cursor(api.search_tweets,q=name, result_type='recent').items(1000):
                        if hasattr(comment, 'in_reply_to_status_id'):
                            
                            if (comment.in_reply_to_status_id==tweet_id):
                                print("on a trouvé")
                                replies.append([str(comment.text), str(comment.user.name)])

                    df.loc[k*number_of_tweets + i] = [tweet.id,tweet.user.name, tweet.created_at, tweet.text, replies, tweet.retweet_count]

                else:
                    df.loc[k*number_of_tweets + i] = [tweet.id,tweet.user.name, tweet.created_at, tweet.text, replies, tweet.retweet_count]

        except:
            print("\n....There has beenproblem with the name of one twittos in the list...")
            pass

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
        tweets = tw.Cursor(api.search_tweets,
                q=topic,
                lang="en",
                since=year+'-'+month+'-'+day, ).items(number_of_tweets)
    
        for i, tweet in enumerate(tweets):
            df.loc[k*number_of_tweets + i] = [tweet.id_str, tweet.created_at, tweet.text]

    return df

def test_query(username, number_of_tweets):
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth,wait_on_rate_limit=True,
    )

    # tweets = tw.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets)
    name = str("NYU Stern")
    tweet_id = 1442487073731190786
    replies=[]
    
                    
    for comment in tw.Cursor(api.search_tweets,q=name, result_type='recent', ).items(1000):
        
        if hasattr(comment, 'in_reply_to_status_id'):
            print("on a trouvé")
            if comment.in_reply_to_status_id!=None:

                print(str(comment.in_reply_to_status_id)+" vs "+ str(tweet_id))
                if (comment.in_reply_to_status_id==tweet_id):
                    print("les tweets collent")
                    replies.append([str(comment.text), str(comment.user.name)])
    print(replies)

def get_tweet_comments(screen_name="Bitcoin", number_of_tweets= 5):
    #accessing to the number of replies is impossible
    #we assume the number of retweets is close to the number of replies
    #because generaly there differ from a factor of 1 to 9
    """
    args: 
        screen_name : string, its the twitter unique tag of the account
        number_of_tweets: integer, the number of most recent tweets we need

    outputs:
        tuple: (dict of tweets, dict of comments per tweet)
    """
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth,wait_on_rate_limit=True,
    )
    tweets_dict = {}
    replies = {}


    for tweet in tw.Cursor(api.user_timeline, screen_name= screen_name,).items(number_of_tweets):
        id = tweet.id
        retweet_count = tweet.retweet_count
        tweets_dict[id] = {
            "text": tweet.text,
            "username": tweet.user.screen_name,
            "retweeted_status": retweet_count!=0,
            "retweet_count": retweet_count,
            "entities": tweet.entities
        }

        tweet_comments_dict = {}

        for comment in tw.Cursor(api.search_tweets,q="to:"+screen_name, result_type='recent', ).items(retweet_count):
            
            if hasattr(comment, 'in_reply_to_status_id'):
                if comment.in_reply_to_status_id!=None:

                    if (comment.in_reply_to_status_id==id):
                        reply = {"text":comment.text, 
                        "username":comment.user.screen_name}
                        tweet_comments_dict[comment.id] = reply
                        
        tweet_comments_dict["number of retweets found"] = len(tweet_comments_dict.keys() )     
        replies[id] = tweet_comments_dict
    

    return tweets_dict, replies


#if we're running this as a script
if __name__ == '__main__':
    number_of_tweets = 50

    
    file = open("dict.json", "r")
    data = json.loads(file.read())
    topics = list(data.keys())
    # new_df = get_tweets_with_comments(data[topics[-2]],10)
    # new_df.to_csv("good_df"+str(topics[-2])+'.csv', index=False)
    # test_query("NYU Stern",100)

    # for topic in topics:
            
    #     print("The topic scrapped is : "+ topic)
    #     full_df = get_tweets_from_people(data[topic],number_of_tweets=number_of_tweets)
    #     full_df.to_csv("df_on_"+str(topic)+'.csv', index=False)
    #         #Api dépassée
    # file.close()
    got = get_tweet_comments(number_of_tweets=1)
    my_dict = got[0]
    my_comments = got[1]
    print(my_comments)
    # print(list(my_dict.values()))
    
