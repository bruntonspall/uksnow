import os
import datetime
import random


from google.appengine.ext.webapp import template
from google.appengine.api.labs import taskqueue
from google.appengine.api import memcache
from google.appengine.api import users

import models
import twitter
import logging
import functools

def cached(name, timeout=60):
    def wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            data = memcache.get(name)
            if not data:
                logging.info("CACHE MISS for "+name)
                data = method(self, *args, **kwargs)
                memcache.set(name, data, timeout)
            return data
        return wrapper
    return wrapper

def set_content_type(content_type):
    def wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            self.response.headers["Content-Type"] = content_type
            return method(self, *args, **kwargs)
        return wrapper
    return wrapper

def write_response(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.response.out.write(method(self, *args, **kwargs))
    return wrapper
   

def render_admin_template(self, end_point, template_values):
    user = users.get_current_user()
    if user:
        template_values['greeting'] = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                    (user.nickname(), users.create_logout_url("/admin/")))

    return render_template(self, end_point, template_values)

def render_template(self, end_point, template_values):
    path = os.path.join(os.path.dirname(__file__), "templates/" + end_point)
    return template.render(path, template_values)

def fetch_snow_tweets():
    logging.info("Fetching tweets for tag #uksnow")
    key = 'uksnow'
    feeditemcount = 1
    latest_cached = 0
    since_id = models.get_from_keystore(key)
    tweets = twitter.get_twitter_search('uksnow&filter=links', since_id)
    for tweet in tweets['results']:
        if feeditemcount == 1:
            try:
                latest_cached = str(tweet['id'])
            except:
                latest_cached = 0
        taskqueue.add(url='/services/store_tweet', params={
            'userid': tweet['from_user_id'],
            'username': tweet['from_user'],
            'imgurl': tweet['profile_image_url'],
            'message': tweet['text'],
            'messageid': tweet['id'],
            'message_created': tweet['created_at'],
            'geo': tweet['geo'],
        })    
        feeditemcount +=1
    if latest_cached > 0:
        models.add_to_keystore(key, latest_cached)
        
def markup_message(message, query):
    if "http://" in message.lower():
        messageelements = message.split(" ")
        newmessageelements = []
        for messageelement in messageelements:
            if messageelement[0:7].lower() == "http://":
                newmessageelements.append("<a href='"+ messageelement +"' target='_new'>"+ messageelement +"</a>")
            else:
                newmessageelements.append(messageelement)
        markedupmessage = " ".join(newmessageelements)
    else:
        markedupmessage = message
    if "@" in markedupmessage:
        messageelements = markedupmessage.split(" ")
        newmessageelements = []
        for messageelement in messageelements:
            if messageelement[0:1].lower() == "@":
                if len(messageelement) > 1:
                    newmessageelements.append("<a href='http://twitter.com/"+ messageelement[1: len(messageelement)] +"' target='_new'>"+ messageelement +"</a>")
            else:
                newmessageelements.append(messageelement)
        markedupmessage = " ".join(newmessageelements)
    if "#" in markedupmessage:
        messageelements = markedupmessage.split(" ")
        newmessageelements = []
        for messageelement in messageelements:
            if messageelement[0:1].lower() == "#":
                if len(messageelement) > 1:
                    newmessageelements.append("<a href='http://search.twitter.com/search?q=%23"+ messageelement[1: len(messageelement)] +"'>"+ messageelement +"</a>")
            else:
                newmessageelements.append(messageelement)
        markedupmessage = " ".join(newmessageelements)
    return markedupmessage

def monthname_to_month(monthname):
    month = 1
    if monthname == "Jan":
        month = 1
    if monthname == "Feb":
        month = 2
    if monthname == "Mar":
        month = 3
    if monthname == "Apr":
        month = 4
    if monthname == "May":
        month = 5
    if monthname == "Jun":
        month = 6
    if monthname == "Jul":
        month = 7
    if monthname == "Aug":
        month = 8
    if monthname == "Sep":
        month = 9
    if monthname == "Oct":
        month = 10
    if monthname == "Nov":
        month = 11
    if monthname == "Dec":
        month = 12
    return month

#def convert_twitter_datetime(theirdatetime):
#    thisdatetime = datetime.datetime(int(theirdatetime[26: 30]), monthname_to_month(theirdatetime[4: 7]), int(theirdatetime[8: 10]), int(theirdatetime[11: 13]), int(theirdatetime[14: 16]), int(theirdatetime[17: 19]))
#    return thisdatetime

    
def convert_twitter_datetime(theirdatetime):
    thisdatetime = datetime.datetime(int(theirdatetime[12: 16]), monthname_to_month(theirdatetime[8: 11]), int(theirdatetime[5: 7]), int(theirdatetime[17: 19]), int(theirdatetime[20: 22]), int(theirdatetime[23: 25]))
    return thisdatetime

    
    
    
