import tweepy
import json
import urlmarker
import threading
import re
from funko_scraper import get_product_details
from Slack import post
import sys
import config

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
access_token = config.twitterConfig.ACCESS_TOKEN
access_token_secret = config.twitterConfig.ACCESS_TOKEN_SECRET
consumer_key = config.twitterConfig.CONSUMER_KEY
consumer_secret = config.twitterConfig.CONSUMER_SECRET
keys = [consumer_key, consumer_secret, access_token, access_token_secret]


class Bot:
    def __init__(self, keys):
        self._consumer_key = keys[0]
        self._consumer_secret = keys[1]
        self._access_token = keys[2]
        self._access_secret = keys[3]

        try:
            auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            auth.set_access_token(self._access_token, self._access_secret)

            self.client = tweepy.API(auth)
            if not self.client.verify_credentials():
                raise tweepy.TweepError
        except tweepy.TweepError as e:
            print("ERROR : connection failed. Check your OAuth keys.")
        else:
            print(
                "Connected as @{}, you can start to tweet !".format(
                    self.client.me().screen_name
                )
            )
            self.client_id = self.client.me().id

    def get_last_tweet(self):
        tweet = self.client.user_timeline(id="920155348866142213", count=1)[0]
        # Extract link
        link = re.findall(urlmarker.WEB_URL_REGEX, tweet.text)
        return "".join(link)


def main():
    main_thread = threading.Timer(180, main)
    main_thread.start()
    obj = Bot(keys)
    with open("funko.txt", "r+") as file:
        content = file.read()
        if content == obj.get_last_tweet():
            print("No new Items")
        else:
            try:
                link_ = obj.get_last_tweet()
                # print (link)
                items = get_product_details(link_)
                if items:
                    for each in items:
                        post(each)
                        # print (each)
            except NameError:
                print("No new Items")
        file.seek(0)
        file.write(obj.get_last_tweet())
        file.truncate()


if __name__ == "__main__":
    main()
