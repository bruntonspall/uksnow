import base64
import urllib

from google.appengine.api import urlfetch
from google.appengine.api import memcache
from django.utils import simplejson

import models
import logging


import settings
    
def get_twitter_credentials(character):
    username=settings.TWITTER_USERNAME
    password=settings.TWITTER_PASSWORD
    return username, password



def get_from_twitter(person, url):
    username, password = get_twitter_credentials(person)
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    headers = {'Authorization': "Basic %s" % base64string} 
    result = urlfetch.fetch(url, method=urlfetch.GET, headers=headers)
    json = simplejson.loads(result.content)
    return json


def get_direct_messages(person, last_id):
    url = "http://twitter.com/direct_messages.json?count=50&since_id=" + last_id
    messages = get_from_twitter(person, url)
    return messages    


def get_sent_direct_messages(person, last_id):
    url = "http://twitter.com/direct_messages/sent.json?count=50&since_id=" + last_id 
    messages = get_from_twitter(person, url)
    return messages    


def get_twitter_statuses(person, last_id):
    url = "http://twitter.com/statuses/user_timeline.json?screen_name=" + person +"&count=50&since_id=" + last_id 
    messages = get_from_twitter(person, url)
    return messages



def get_twitter_replies(person, last_id):
    url = "http://twitter.com/statuses/replies.json?since_id=" + last_id
    messages = get_from_twitter(person, url)
    return messages



def get_twitter_search(query, last_id):
    if last_id != '1':
        url = "http://search.twitter.com/search.json?q=" + query + "&rpp=100&since_id=" + last_id
    else:
        url = "http://search.twitter.com/search.json?q=" + query + "&rpp=100"
        
    messages = get_from_twitter("default", url)
    return messages






def get_twitter_user(twitterid):
    twitterid = str(twitterid)
    key = "user_" + twitterid
    user = memcache.get(key)
    if not user:
        url = "http://twitter.com/users/"+ twitterid + ".json"
        user = get_from_twitter("default", url)
        memcache.add(key, user, 360)
    return user



