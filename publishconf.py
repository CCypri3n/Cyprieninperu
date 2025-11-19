# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://cyprieninperu.netlify.app'
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

OUTPUT_PATH = '__site/'

I18N_SUBSITES = {
    'fr': {
        'SITENAME': 'Cyprien au Pérou',
        'OUTPUT_PATH': '__site/fr/',
        'LOCALE': 'fr_FR',
        'LINKS_WIDGET_NAME': 'Liens',
        'SOCIAL_WIDGET_NAME': 'Social',
    },
    'de': {
        'SITENAME': 'Cyprien in Peru',
        'OUTPUT_PATH': '__site/de/',
        'LOCALE': 'de_DE',
        'LINKS_WIDGET_NAME': 'Links',
        'SOCIAL_WIDGET_NAME': 'Sozial',
    }
}

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""
