import time
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sys
from pymongo import MongoClient
import json

# keys
ckey = 'YePIl8OYel5dtH2P71B9NbGIe'
consumer_secret = 'gqsKipuAqLlvFXr3j1C66Wk26hIXZmBdDrOMeZU3Br32a7IoY7'
access_token_key = '2354152670-IdMr1ZBfcNS5eamHnaY4w9PqksgHjF7UJVJQknJ'
access_token_secret = 'rWGglrBuxkblkiTKjN7OIXMIBK0Vxk3ZHDyqWfYwtmBgd'

start_time = time.time()  # grabs the system time
keyword_list = ['twitter']  # track list


class listener(StreamListener):
    def __init__(self, start_time, time_limit=120):

        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, data):

        while (time.time() - self.time) < self.limit:
# check this out for more error handlers
#thttp://stackoverflow.com/questions/23601634/how-to-restart-tweepy-script-in-case-of-error
            try:
                client = MongoClient('localhost', 27017)
                db = client['twitter1_db']
                collection = db['twitter_collection']
                tweet = json.loads(data)
                # if tweet['coordinates'] is not None: If you only want geotagged tweets
                collection.insert(tweet)
                return True
            # various exception handling blocks
            except KeyboardInterrupt:
                sys.exit()
            except AttributeError as e:
                print('AttributeError was returned, stupid bug')
                print(e)
                pass
            except tweepy.TweepError as e:
                print('Below is the printed exception')
                print(e)
                if '401' in e:
                    # not sure if this will even work
                    print('Below is the response that came in')
                    print(e)
                    time.sleep(60)
                    pass
                else:
# raise an exception if another status code was returned,we don't like other kinds
                    time.sleep(60)
                    pass
            except BaseException as e:
                print('failed ondata,', str(e))
                time.sleep(5)
                pass
        exit()

    def on_error(self, status):

        print(status)


# Instance
auth = OAuthHandler(ckey, consumer_secret)  # Consumer keys
auth.set_access_token(access_token_key, access_token_secret)  # Secret Keys
# initialize Stream object with a time out limit
twitterStream = Stream(auth, listener(start_time, time_limit=120))
# set bounding box filter
twitterStream.filter(locations=[-118.723549, 33.694679, -117.929466, 34.33926])
#Los Angeles
