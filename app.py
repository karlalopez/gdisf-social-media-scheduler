import os
import re
import random
import codecs
import json
import gspread
import threading
import tweepy
from sys import argv, exit
from datetime import datetime, timedelta
from PIL import Image
from oauth2client.client import SignedJwtAssertionCredentials

# get tweets
def getTweets():
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    try:
        gc = gspread.authorize(credentials)
    except Exception, e:
        print "ERROR: {} - {} \n".format(e,now)
    
    # spreadsheet needs to be shared with the email on the credentials
    sh = gc.open_by_key(os.environ.get('SPREADSHEET_ID'))
    worksheet = sh.sheet1
    valid_tweets = []
    for row in worksheet.get_all_values():
        if row[2] != "" and row[2] != "Day":
            workshop_date_raw = "{}/{}".format(row[8],row[2])
            workshop_date = datetime.strptime(workshop_date_raw, '%Y/%m/%d')
            tomorrow = datetime.utcnow() + timedelta(days=0.5)
            if workshop_date > tomorrow:
                valid_tweets.append(row[7])
    return valid_tweets

# pick ramdomly from contents
def rndm(contents):
        random_content = random.choice(contents)
        return str(random_content)

# post to twitter   
def postToTwitter(tweets_available,keys):
    # get a random photo to tweet
    photos_available = os.listdir('photos')
    photo = rndm(photos_available)
    filename = "photos/{}".format(photo)
    file = Image.open(filename)
    
    # get a random message to tweet & get rid of tabs or line breaks
    msg = rndm(tweets_available)
    tweet = re.sub(r"\t","\n",msg)
    
    # authenticate with twitter
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    now = str(datetime.strftime(datetime.utcnow(), '%c'))

    # post tweet
    try:
        api = tweepy.API(auth)
        api.update_with_media(filename, tweet, file)
    except tweepy.TweepError as e:
        print "ERROR: {} - {} - {} \n".format(e,now,msg)
        return

    print "SUCCESS: {} - {} \n".format(now,msg)

if __name__ == '__main__':
    # twitter credentials
    ckey = os.environ.get('TWITTER_CKEY')
    csecret = os.environ.get('TWITTER_CSECRET')
    atoken = os.environ.get('TWITTER_ATOKEN')
    asecret = os.environ.get('TWITTER_ASECRET')
    keys = [ckey,csecret,atoken,asecret]

    # google spreasheet credentials
    json_key = json.loads(os.environ.get('SPREADSHEET_CREDENTIALS'))
    scope = ['https://spreadsheets.google.com/feeds']

    # sets the interval
    interval = int(os.environ.get('INTERVAL'))

    def setInterval(func,keys,sec):
        def func_wrapper():
            setInterval(func, keys, sec)
            tweets_available = getTweets()
            func(tweets_available,keys)  
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
    setInterval(postToTwitter,keys,interval)

