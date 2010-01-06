#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.api import memcache

import models
import helpers
import logging


class MainHandler(webapp.RequestHandler):
    @helpers.write_response
    @helpers.cached('main')
    def get(self):
        return helpers.render_template(self, 'webviews/front.html', {})

class GeoRSSHandler(webapp.RequestHandler):
    @helpers.write_response
    @helpers.cached('georss', timeout=300)
    def get(self):
        return helpers.render_template(self, 'webviews/georss.html', {'items': models.get_tweets()})

class GeoJSONHandler(webapp.RequestHandler):
    @helpers.write_response
    @helpers.cached('geojson', timeout=300)
    def get(self):
        return helpers.render_template(self, 'webviews/geojson.html', {'items': models.get_tweets(100)})

def main():
  application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/georss', GeoRSSHandler),
        ('/geojson', GeoJSONHandler),
        ],    debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
