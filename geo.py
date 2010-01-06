import base64
import urllib

from google.appengine.api import urlfetch
from django.utils import simplejson

import models
import logging
import settings


def get_geolocation(postcode):
    url = "http://maps.google.com/maps/geo?q="+postcode+",UK&output=json&sensor=false&key="+settings.GOOGLE_MAPS_KEY
    location = get_from_geo(url)
    status = location["Status"]["code"]
    if status != 200:
        return None, None
    country_code = location["Placemark"][0]["AddressDetails"]["Country"]["CountryNameCode"]
    if country_code !="GB":
        return None, None
    longitude,latitude ,height = location["Placemark"][0]["Point"]["coordinates"]
    return str(longitude), str(latitude)   


def get_from_geo(url):
    logging.info("Fetching url: "+url)
    result = urlfetch.fetch(url, method=urlfetch.GET)
    json = simplejson.loads(result.content)
    return json
