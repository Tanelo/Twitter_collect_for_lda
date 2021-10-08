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

# The fields you can select on tweets are found here : 
# https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

# The fields you can select on users are found here : 
# https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user


#Get your Twitter API credentials and enter them here
api_key = json.load(open('credentials.json'))["first_key"]
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
   )
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
    
                    
    for comment in tw.Cursor(api.search_tweets,q="to:"+name, result_type='recent', ).items(100):
        
        if hasattr(comment, 'in_reply_to_status_id'):
            print("on a trouvé")
            if comment.in_reply_to_status_id!=None:

                print(str(comment.in_reply_to_status_id)+" vs "+ str(tweet_id))
                if (comment.in_reply_to_status_id==tweet_id):
                    print("les tweets collent")
                    replies.append([str(comment.text), str(comment.user.name)])
    print(replies)

def get_tweet_comments(screen_name="anne_sinclair", number_of_tweets= 5):
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

    #faire le edge case du tweet si c'est un retweet

    for tweet in tw.Cursor(api.user_timeline, screen_name= screen_name,).items(number_of_tweets):
        try :

            if not (tweet.retweeted):

                id = tweet.id
                retweet_count = tweet.retweet_count
                tweets_dict[str(id)] = {
                    "id": str(tweet.id),
                    "text": tweet.text,
                    "date": str(tweet.created_at),
                    "username": tweet.user.screen_name,
                    "retweeted_status": retweet_count!=0,
                    "retweet_count": retweet_count,
                    "likes": tweet.favorite_count,
                    # "entities": tweet.entities,
                    
                }

                tweet_comments_dict = {}
                comments_ids = []
                #it works better with "to"
                for comment in tw.Cursor(api.search_tweets,q="to:"+screen_name, result_type='recent', ).items(retweet_count):
                    
                    if hasattr(comment, 'in_reply_to_status_id'):
                        if comment.in_reply_to_status_id!=None:
                            

                            if (comment.in_reply_to_status_id==id):
                                comment_count = comment.retweet_count
                                comments_ids.append(str(comment.id))
                                reply = {
                                        "tweet_id": str(id),
                                        "text": comment.text,
                                        "date": str(comment.created_at),
                                        "username": comment.user.screen_name,
                                        "retweeted_status": comment_count!=0,
                                        "retweet_count": comment_count,
                                        "likes": comment.favorite_count,
                                        # "entities":comment.entities,
                                        }
                                tweet_comments_dict[str(comment.id)] = reply
                            
                tweet_comments_dict["number of replies found"] = len(tweet_comments_dict.keys() )     
                replies[str(id)] = tweet_comments_dict
                tweets_dict[str(id)]["comments"] = replies[str(id)]
                tweets_dict[str(id)]["comments_ids"]= comments_ids
        except:
            pass
    

    return tweets_dict, replies


def scrap_topic(topic="world_leaders"):
        scrapped_tweets = get_tweet_comments(number_of_tweets=1)
        comments_df = pd.DataFrame.from_dict(scrapped_tweets[1])
        tweets_df = pd.DataFrame.from_dict(scrapped_tweets[0])
        comments_df.to_excel('dataframes_for_recommenders_training/comments_df1.xlsx')
        tweets_df.to_excel('dataframes_for_recommenders_training/tweets_df1.xlsx')

        return comments_df, tweets_df

def get_tweets_from(users = ["anne_sinclair"], name_of_the_list ="anne_sinclair", isDf= True, number_of_tweets=1):
    path = "df_for_training_recommenders/"
    if isDf:
        dfs_tweets = []
        dfs_comments = []
        dfs_fulls = []
        for user in users:
            tweets_dict, comments_dict = get_tweet_comments(user, number_of_tweets=number_of_tweets)
            df_tweets = pd.DataFrame.from_dict(tweets_dict)
            df_comments = pd.DataFrame.from_dict(comments_dict)
            df_full = pd.concat([df_tweets,df_comments],axis=0)
            dfs_tweets.append(df_tweets)
            dfs_comments.append(df_comments)
            dfs_fulls.append(df_full)
            
        dfs_tweets = pd.concat(dfs_tweets, axis=1).T
        dfs_comments = pd.concat(dfs_comments, axis=1).T
        dfs_fulls = pd.concat(dfs_fulls, axis=1).T
        dfs_tweets.to_excel(path+"df_tweets"+"_"+name_of_the_list+'.xlsx')
        dfs_comments.to_excel(path+"df_comments"+"_"+name_of_the_list+'.xlsx')
        dfs_fulls.to_excel(path+"df_all"+"_"+name_of_the_list+'.xlsx')
        dfs_tweets.to_csv(path+"df_tweets"+"_"+name_of_the_list+'.csv')
        dfs_comments.to_csv(path+"df_comments"+"_"+name_of_the_list+'.csv')
        dfs_fulls.to_csv(path+"df_all"+"_"+name_of_the_list+'.csv')

            

    else : 
        with open('tweets_and_comments'+name_of_the_list+'.json', 'w') as fp:
            big_dict   = {
            }
            for user in users:
                tweets_dict, comments_dict = get_tweet_comments(user, number_of_tweets=1)
                big_dict[user] = {
                    "tweets_dict": tweets_dict,
                    "comments_dict": comments_dict,
                }

            json.dump(big_dict, fp)


def get_tweets_df(users= ["anne_sinclair"],number_of_tweets = 1, name_of_the_list ="anne_sinclair"):
    auth = tw.OAuthHandler(api_key['consumer_key'], api_key['consumer_secret'])
    auth.set_access_token(api_key['access_key'], api_key['access_secret'])
    api = tw.API(auth,wait_on_rate_limit=True,
    )
    df_tweets = pd.DataFrame(index=np.arange(0, len(users) * number_of_tweets), columns=['id', 'username','date', 'text','retweeted_status','retweet_count','likes','comments'])
    big_dict   = {
        }
    for i, user in enumerate(users):
        try:
        # tweets_dict, comments_dict = get_tweet_comments(user, number_of_tweets=1)
            tweets = tw.Cursor(api.user_timeline, screen_name= user,).items(number_of_tweets)
            for k, tweet in enumerate(tweets):
                

                    if not (tweet.retweeted):

                        id = tweet.id
                        retweet_count = tweet.retweet_count
                        # tweets_dict[id] = {
                        #     "id": tweet.id,
                        #     "text": tweet.text,
                        #     "date": tweet.created_at,
                        #     "username": tweet.user.screen_name,
                        #     "retweeted_status": retweet_count!=0,
                        #     "retweet_count": retweet_count,
                        #     "likes": tweet.favorite_count,
                        #     # "entities": tweet.entities,
                            
                        # }

                        tweet_comments_dict = {}
                        #it works better with "to"
                        for comment in tw.Cursor(api.search_tweets,q="to:"+user, result_type='recent', ).items(retweet_count):
                            
                            if hasattr(comment, 'in_reply_to_status_id'):
                                if comment.in_reply_to_status_id!=None:
                                    

                                    if (comment.in_reply_to_status_id==id):
                                        comment_count = comment.retweet_count
                                        reply = {
                                                "tweet_id": id,
                                                "text": comment.text,
                                                "date": comment.created_at,
                                                "username": comment.user.screen_name,
                                                "retweeted_status": comment_count!=0,
                                                "retweet_count": comment_count,
                                                "likes": comment.favorite_count,
                                                # "entities":comment.entities,
                                                }
                                        tweet_comments_dict[comment.id] = reply
                                    
                        # tweet_comments_dict["number of replies found"] = len(tweet_comments_dict.keys() )     
                        # replies[id] = tweet_comments_dict
                        # tweets_dict[id]["comments"] = replies[id]
                        #'id', 'username','date', 'text','retweeted_status','retweet_count','likes','comments'
                        df_tweets.loc[i*number_of_tweets + k] = [tweet.id_str, tweet.user.screen_name,tweet.created_at, tweet.text, retweet_count!=0,tweet.favorite_count, tweet_comments_dict]
        except:
            
            pass    

    df_tweets.to_excel('df_tweets'+name_of_the_list+'.xlsx')
    df_tweets.to_csv('df_tweets'+name_of_the_list+'.csv')

        # for k, tweet in enumerate(tweets_dict.values()):

            

        

#if we're running this as a script
if __name__ == '__main__':
    number_of_tweets = 40
    

    
    file = open("dict.json", "r")
    data = json.loads(file.read())
    topics = list(data.keys())
    
    
    # print(get_tweet_comments(number_of_tweets=1)[1])
    # get_tweets_from(data["entrepreneurs"],"entrepreneurs")
    get_tweets_from(["anne_sinclair","leadlagreport"], "try", number_of_tweets=10)
    # get_tweets_df()

    
    # new_df = get_tweets_with_comments(data[topics[-2]],10)
    # new_df.to_csv("good_df"+str(topics[-2])+'.csv', index=False)
    # test_query("NYU Stern",100)

    # for topic in topics:
            
    #     print("The topic scrapped is : "+ topic)
    """
    to scrap people on precised fields
    """
    # full_df = get_tweets_from_people(data["entrepreneurs"],number_of_tweets=number_of_tweets)
    # full_df.to_csv("df_on_"+str("entrepreneurs")+'.csv', index=False)
    """
    """
    # file.close()
    # got = get_tweet_comments(number_of_tweets=1)
    # my_dict = got[0]
    # my_comments = got[1]
    # print(my_comments)
    # print(list(my_dict.values()))
    
