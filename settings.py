# These are global settings
# We also import settings_local for TWITTER_USERNAME, TWITTER_PASSWORD and MAPS_KEY
import logging

try:
    from settings_local import *
except ImportError:
    logging.error("Failed to import settings_local, Usernames and Passwords may not work")
    pass

GOOGLE_MAPS_KEY = "ABQIAAAA4O8mCoruMQHuBixJP9HGBRRZE1TQY638hgp6pQcoB7U-Ql8n_BRPdxCkAgKLkS-hNXwMhE6KsaxExQ"

