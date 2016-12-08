#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Gabriela Surita'
SITENAME = u'Gabi Surita'
SITEURL = 'gabisurita.github.io'

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
FEED_ALL_RSS = 'feeds/all.rss.xml'
OUTREACHY_FEED_RSS = 'feeds/outreachy.rss.xml'
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)


DEFAULT_PAGINATION = 5

THEME = 'theme'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Theme conf
LICENSE_NAME = 'CC-BY-SA 4.0'
LICENSE_URL = 'https://creativecommons.org/licenses/by-sa/4.0/'
PROFILE_IMAGE = '/theme/img/prof-150x150.jpg'
SHOW_ARTICLE_AUTHOR = True
PAGES_ON_MENU = True

# Theme menu
EMAIL_ADDRESS = 'gsurita@mozilla.com'
FB_ADDRESS = 'https://www.facebook.com/gabsurita'
GITHUB_ADDRESS = 'https://github.com/gabisurita'

# Blogroll
# MENU_ITEMS = [
#     ('About', '/about.html'),
# ]
