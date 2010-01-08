UK Snow Map In Pictures
=======================

Overview
--------

This is the code that powers the #uksnow pictures map at http://www.guardian.co.uk/uk/interactive/2010/jan/05/weather-snow-pictures
We wrote this code in about 5 hours on Tuesday 5th Jan, 2010 when we had the idea that it might be a useful mashup to throw together.

Authors
-------

Michael Brunton-Spall 
Lisa van-Gelder


Code Overview
-------------

The code is pretty simple, There is a cronjob in cron.yaml that fires once every 2 minutes and calls /services/fetch_tweets.  This is defined in services.py, it makes a twitter call to fetch the search result for #uksnow filter:links.

The twitter search result brings back every tweet that has mentioned uksnow and has a URL in it. We fire off a taskqueue for each tweet, storing the tweet data in the task payload.
The queue processes at 5 entries a second, each one calling /services/store_tweet, and analyses the tweet, looking for an image url.  We support the 5 most likely image buckets that people use, and calculate the thumbnail image to use on the map.  We also look for a postcode.  If we have a postcode, we use Googles Geocoder to locate the tweet, and then store it into the datastore.

When you request '/' you get back a nice static front, that imports Google maps, and loads '/georss'.  This RSS feed is the last 250 tweets, ordered by tweet creation time.  Using Googles GGeoXml object automatically creates an overlay with pins on the map.  We have since added /geojson and /kml for anyone else that wants to get our data (limited to 100 items to save processing power).
This code is not quite complete, you will need to create a settings_local.py file that contains TWITTER_USERNAME and TWITTER_PASSWORD so that the twitter search is authenticated and therefore not rate-limited as much.

TODO
----

 * Using KML, we can provide custom icons, including the image thumbnail as an icon.  It doesn't however look pretty -- DONE
 * With a KML network link, we can be given the geo bounding box you are looking at, and the scale.  We could use that to only return say the latest 25 / 50 pictures in the area you are looking.  We would need to precompute the bounding boxes at tweet creation time however
