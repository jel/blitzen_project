# -*- coding: utf-8 -*-
from db import *
from apps import app_root, app_resolver
from keys import secret_key_manager

import os as _os

MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/'

MEDIA_ROOT = _os.path.join(app_root, 'media')
