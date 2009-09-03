# -*- coding: utf-8 -*-
# Django settings for djproj project.
import quickening

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en_us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = quickening.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = quickening.MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = quickening.ADMIN_MEDIA_PREFIX

SECRET_KEY = quickening.secret_key_manager.get_key()
TEMPLATE_LOADERS = quickening.app_resolver.template_loaders()
MIDDLEWARE_CLASSES = quickening.app_resolver.middleware_classes()

ROOT_URLCONF = 'quickening.urls'

TEMPLATE_DIRS = quickening.app_resolver.template_paths()
INSTALLED_APPS = quickening.app_resolver.installed_apps()

print "INSTALLED_APPS:", INSTALLED_APPS
print "MIDDLEWARE_CLASSES:", MIDDLEWARE_CLASSES
