import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 

def run_twitter_etl():

    access_key = "" 
    access_secret = "" 
    consumer_key = ""
    consumer_secret = ""


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
                            #User timeline takes username you want to extract data from, count is the number of tweets you want to extract, include rts is for retweets.--Sakthe.
                            # extended gives full tweeets #Tweets is in form of json object

    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv('s3://sakthe-twitter-data-pipelining/refined_tweets.csv')

    #add iam permisiion rpoles to the ec2 the s3full access and ec2 full access
    #after that open airflow select twitter_dags and then go to the graph part then click run then you can see that yur s3 will get the data
    #all data is in cd airflow and then the sudo nano files. the codes have that
    #https://www.youtube.com/watch?v=q8q3OFFfY6c&t=1572s