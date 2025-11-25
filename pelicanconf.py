AUTHOR = 'Cyprien Chevallier'
SITENAME = 'Cyprien in Peru'
SITEURL = ""

PATH = "content"

TIMEZONE = 'America/Lima'

PLUGIN_PATHS = ['plugins']

PLUGINS = ['i18n_subsites', 'statistics', 'image_gallery', 'metadata_goatcounter_viewcount']


MARKDOWN = {
    'extensions': [
        'markdown.extensions.extra',
        'markdown.extensions.meta',
        'plugins.static_url_rewrite.static_url_rewrite',
        'plugins.carousel_extension.carousel_extension',  # Assuming carousel_extension.py in plugins folder
    ],
    'output_format': 'html5',
}

JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

DEFAULT_LANG = 'en'  # Main site language

THEME = 'theme/smashing-magazine'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Donate", "https://www.betterplace.org/de/projects/142389?utm_campaign=user_share&utm_medium=ppp_sticky&utm_source=Link&utm_content=bp"),
    ("Ecoselva", "https://ecoselva.org/"),
    ('CACI Satinaki', 'https://cacisatinaki.com/'),
    ('PachaMama', 'https://peru-kaffee.de/'),
)

# Social widget
SOCIAL = (
    ("Instagram", "https://www.instagram.com/ccypri3n/"),
)

#MENUITEMS = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

TYPOGRIFY = True

IGNORE_FILES = ["templates", ".obsidian"]

I18N_SUBSITES = {
    'fr': {
        'SITENAME': 'Cyprien au Pérou',
        'OUTPUT_PATH': 'output/fr/',
        'LOCALE': 'fr_FR',
        'LINKS_WIDGET_NAME': 'Liens',
        'SOCIAL_WIDGET_NAME': 'Social',
        'LINKS': [
            ('Faire un don', 'https://www.betterplace.org/de/projects/142389?utm_campaign=user_share&utm_medium=ppp_sticky&utm_source=Link&utm_content=bp'), 
            ('Ecoselva', 'https://ecoselva.org/'),
            ('CACI Satinaki', 'https://cacisatinaki.com/'),
            ('PachaMama', 'https://peru-kaffee.de/'),
                  ],
    },
    'de': {
        'SITENAME': 'Cyprien in Peru',
        'OUTPUT_PATH': 'output/de/',
        'LOCALE': 'de_DE',
        'LINKS_WIDGET_NAME': 'Links',
        'SOCIAL_WIDGET_NAME': 'Sozial',
        'LINKS': [
            ('Spenden', 'https://www.betterplace.org/de/projects/142389?utm_campaign=user_share&utm_medium=ppp_sticky&utm_source=Link&utm_content=bp'),
            ('Ecoselva', 'https://ecoselva.org/'),
            ('CACI Satinaki', 'https://cacisatinaki.com/'),
            ('PachaMama', 'https://peru-kaffee.de/'),
        ],
    },
}

ARTICLE_PATHS = ['articles']
PAGE_PATHS = ['pages']
STATIC_PATHS = ['extra', 'newsletters']
EXTRA_PATH_METADATA = {
    'extra/gallery.json': {'path': 'gallery.json'},
}

ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

ARTICLE_LANG_URL = '{lang}/{slug}/'
ARTICLE_LANG_SAVE_AS = '{lang}/{slug}/index.html'

PAGE_LANG_URL = '{lang}/{slug}/'
PAGE_LANG_SAVE_AS = '{lang}/{slug}/index.html'

AUTHOR_URL = 'author/'
AUTHOR_SAVE_AS = 'author/index.html'

CATEGORY_URL = '{slug}/'
CATEGORY_SAVE_AS = '{slug}/index.html'

I18N_GETTEXT_LOCALEDIR = 'theme/locale'
I18N_GETTEXT_DOMAIN = 'messages'


CATEGORY_TRANSLATIONS = {
    'en': {
        'peru': 'Peru',
        'articles':'Articles',
    },
    'fr': {
        'peru': 'Pérou',
        'articles':'Articles',
    },
    'de': {
        'peru': 'Peru',
        'articles':'Artikel',
    }
}

# The defaults for the OpenGraph headers.

OG = {
    'en': {
        'description':'Cyprien in Peru is a personal blog for my one year adventure in Peru.',
        'author':'Cyprien Chevallier',
        'site_name':'Cyprien in Peru'
    },
    'fr': {
        'description':'Cyprien au Pérou est un blog personnel pour mon aventure d\'un an au Pérou ',
        'author':'Cyprien Chevallier',
        'site_name':'Cyprien au Pérou',
    },
    'de': {
        'description':'Cyprien in Peru ist ein persönlicher Blog für mein einjähriges Abenteuer in Peru',
        'author':'Cyprien Chevallier',
        'site_name':'Cyprien in Peru',
    },
    'author':'Cyprien Chevallier',
    'image':'https://ik.imagekit.io/721zjc9b0/images/P8260493_DxO_oWrPud-bS.jpg?updatedAt=1763596726655',
    'logo':'https://ik.imagekit.io/721zjc9b0/images/machu-picchu_zPDSNYFy_.png?updatedAt=1763607436597',
    'date':'23-08-2025',
}

AUTHOR_AVATAR = {
    "Cyprien Chevallier":"https://ik.imagekit.io/721zjc9b0/images/CyprienChevallier_R2MC3rPjn.JPG",
    "Baum":"https://ik.imagekit.io/721zjc9b0/images/CyprienChevallier_R2MC3rPjn.JPG",
}