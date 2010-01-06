#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp
import logging
import models
import helpers
import time
import geo
import re
import datetime
import services
import random
import time


def get_id_for_tweet():
    current_id = models.get_from_keystore("tweet_id")
    id_as_number = int(current_id)
    next_id = id_as_number + 1
    models.add_to_keystore("tweet_id", str(next_id))
    t = datetime.datetime.now()
    secs = time.mktime(t.timetuple())
    milis = int(secs)
    id_plus_currenttime = str(milis) + current_id
    return int(id_plus_currenttime)

class CreateTweet(webapp.RequestHandler):
    @helpers.write_response
    def get(self):
        template_values = {
            "form": models.TweetForm()
        }
        return helpers.render_admin_template(self, "adminviews/create_tweet.html", template_values)

    @helpers.write_response
    def post(self):
        form = models.TweetForm(data=self.request.POST)
        if form.is_valid():
            logging.warn("got postcode: "+form.clean_data["postcode"])
            longitude, latitude = geo.get_geolocation(form.clean_data["postcode"])
            tweetpic = services.get_image(form.clean_data["tweetpic"])
            models.store_tweet(get_id_for_tweet(), form.clean_data["message"], 1, form.clean_data["username"], None, tweetpic, datetime.datetime.now(), longitude, latitude)
            self.redirect("/admin/")
        else:
            template_values = {
            "form": form
            }
            return helpers.render_admin_template(self, "adminviews/create_tweet.html", template_values)


def main():
    application = webapp.WSGIApplication([
    ('/admin/', CreateTweet),
    ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
