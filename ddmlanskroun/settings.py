"""
Django settings for ddmlanskroun project.
"""

from django.utils.translation import ugettext_lazy as _
from leprikon.site.settings import *

# Application definition
INSTALLED_APPS = (
    [
        "ddmlanskroun",
    ]
    + INSTALLED_APPS
    + [
        "django.contrib.redirects",
        "cms_articles",
        "cms_articles.import_wordpress",
        "aldryn_search",
        "cmsplugin_iframe2",
    ]
)

MIDDLEWARE = [
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
] + MIDDLEWARE

CMS_TEMPLATES = [
    ("default.html", "Výchozí"),
    ("with_submenu.html", "Se submenu"),
    ("home.html", "Titulní stránka"),
]

# templates used to render plugin article
CMS_ARTICLES_PLUGIN_ARTICLE_TEMPLATES = [
    ("default", "Výchozí"),
    ("home", _("Na titulní stránku")),
]

# templates used to render plugin articles
CMS_ARTICLES_PLUGIN_ARTICLES_TEMPLATES = [
    ("default", "Výchozí"),
    ("archive", "Archiv"),
    ("home", _("Na titulní stránku")),
]

CMS_PLACEHOLDER_CONF = {
    "content": {
        "name": "Obsah",
    },
    "sidebar": {"name": "Boční panel"},
    "footer": {
        "name": "Patička",
    },
}

THUMBNAIL_ALIASES = {
    "": {
        "preview": {
            "size": (240, 10000),
        },
        "view": {
            "size": (760, 570),
        },
    },
}

# search settings
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "data", "search"),
    },
    "cs": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "data", "search"),
    },
}

DJANGOCMS_FILE_TEMPLATES = [("gallery", _("Gallery")), ("homepage", _("Homepage"))]
