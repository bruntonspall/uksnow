import random

from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

import helpers

MODEL_VERSION=1

class Tweet(search.SearchableModel):
    messageid = db.IntegerProperty(required=True)
    message = db.TextProperty(required=True)
    userid = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
    lusername = db.StringProperty()
    imgurl = db.TextProperty()
    tweetpic = db.TextProperty()
    created_at = db.DateTimeProperty()
    added_at = db.DateTimeProperty(auto_now_add=True)
    to_check = db.BooleanProperty(default=False)
    long = db.StringProperty()
    lat = db.StringProperty()

    def url(self):
        if self.userid == 1:
            return None
        return "http://twitter.com/%s/status/%d" % (self.lusername, self.messageid)

    def description(self):
        return '%s<br/>Tweeted at: %s<img src=\"%s\" width="150" height="150"/>' % (self.message, self.created_at, self.tweetpic)


class ManualTweet(search.SearchableModel):
    message = db.TextProperty(required=True)
    username = db.StringProperty(required=True)
    tweetpic = db.TextProperty(required=True)
    postcode = db.TextProperty(required=True)
   

class TweetForm(djangoforms.ModelForm):
      class Meta:
        model = ManualTweet


def store_tweet(messageid, message, userid, username, imgurl, tweetpic, created_at, long, lat):
    key = "id_" + str(messageid)
    tweet = Tweet(key_name=key, message=message, messageid=messageid, userid=userid, username=username, lusername = username.lower(), imgurl = imgurl, tweetpic = tweetpic,  created_at=created_at, long=long, lat=lat)
    tweet.put()


def get_tweet(messageid):
    query = db.Query(Tweet)
    query.filter('messageid =', messageid)
    return query.get()

def get_tweets(maximum=250):
    return db.Query(Tweet).order('-created_at').fetch(maximum)


class KeyStore(db.Model):
    name = db.StringProperty(required=True)
    value = db.StringProperty()


def add_to_keystore(name, value):
    keystore = KeyStore.get_or_insert(name, name=name)
    keystore.value = value
    keystore.put()


def get_from_keystore(name):
    keystore = KeyStore.get_by_key_name(name)
    if keystore:
        return str(keystore.value)
    else:
        return "1"



