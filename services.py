#!/usr/bin/env python

import datetime

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue

import models
import twitter
import helpers
import geo
import re
import logging
import urllib

POSTCODE = re.compile('(?: |^)([A-Z]{1,2}\d{1,2}(?: \d[A-Z]{2})?)(?: |$)', re.IGNORECASE)

TWITPIC = re.compile('http://twitpic.com/([a-z0-9]*)(?: |<|$)', re.IGNORECASE)

YFROG = re.compile('(http://yfrog.com/[a-z0-9]*)(?: |<|$)', re.IGNORECASE)

IMGLY = re.compile('http://img.ly/([a-zA-Z0-9]*)(?: |<|$)', re.IGNORECASE)

TWITGOO = re.compile('http://twitgoo.com/([a-zA-Z0-9]*)(?: |<|$)', re.IGNORECASE)

TWITSNAPS1 = re.compile('http://twitsnaps.com/snap/([0-9]*)(?: |<|$)', re.IGNORECASE)

TWITSNAPS2 = re.compile('http://twitsnaps.com/full_photo.php\?img_id=([0-9]*)&act', re.IGNORECASE)

class FetchTweets(webapp.RequestHandler):
    def get(self):
        helpers.fetch_snow_tweets()
         

def get_image(text):
    twitpic_matcher = TWITPIC.search(text)
    if twitpic_matcher:
        photo_id = twitpic_matcher.group(1)
        photo_url = "http://twitpic.com/show/thumb/"+photo_id
        return photo_url
    imgly_matcher = IMGLY.search(text)
    if imgly_matcher:
        photo_id = imgly_matcher.group(1)
        photo_url = "http://img.ly/show/thumb/"+photo_id
        return photo_url
    twit1_matcher = TWITSNAPS1.search(text)
    if twit1_matcher:
        photo_id = twit1_matcher.group(1)
        photo_url = "http://twitsnaps.com/thumb/"+photo_id
        return photo_url
    twit2_matcher = TWITSNAPS2.search(text)
    if twit2_matcher:
        photo_id = twit2_matcher.group(1)
        photo_url = "http://twitsnaps.com/thumb/"+photo_id
        return photo_url
    twitgoo_matcher = TWITGOO.search(text)
    if twitgoo_matcher:
        photo_id = twitgoo_matcher.group(1)
        photo_url = "http://twitgoo.com/show/thumb/"+photo_id
        return photo_url
    yfrog_matcher = YFROG.search(text)
    if yfrog_matcher:
        photo_id = yfrog_matcher.group(1)
        photo_url = photo_id+".th.jpg"
        return photo_url


class StoreTweet(webapp.RequestHandler):
    def post(self):
        tweet = models.get_tweet(int(self.request.get("messageid")))
        if not tweet:
            msgid = int(self.request.get("messageid"))
            text = helpers.markup_message(self.request.get("message"), self.request.get("query"))
            userid =  int(self.request.get("userid"))
            username = self.request.get("username")
            imgurl = self.request.get("imgurl")
            tweetpic = get_image(text)
            if tweetpic:
                logging.info("tweetpic is:" +tweetpic)
            created = self.request.get("message_created")
            matcher = POSTCODE.search(text)
            if matcher:
                postcode = matcher.group(1)
                escaped_postcode = urllib.quote(postcode)
                logging.info("Tweet has escaped postcode %s" %(escaped_postcode))
                longitude, latitude = geo.get_geolocation(escaped_postcode)
                if longitude:
                    models.store_tweet(msgid, text, userid, username, imgurl, tweetpic, helpers.convert_twitter_datetime(created), longitude, latitude)




def main():
  application = webapp.WSGIApplication([
    ('/services/fetch_tweets', FetchTweets),
    ('/services/store_tweet', StoreTweet),
    ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
