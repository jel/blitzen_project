# -*- coding: utf-8 -*-
import os as _os
from apps import app_resolver

class KeyManager(object):
    def __init__(self, app_res,  key_name='secret'):
        self._app_res = app_res
        self._key_name = key_name
        self._key_path = _os.path.abspath(
            _os.path.join(self._app_res.root(), 'keys/secret.key')
        )

    def get_key(self):
        if _os.path.exists(self._key_path):
            key_data = open(self._key_path).read()
            return key_data
        else:
            key_data = self._generate_key()
            fp = open(self._key_path,  'wb')
            fp.write(unicode(key_data))
            fp.close()
            return key_data

    def _generate_key(self):
        import uuid
        key = uuid.uuid4()
        return key

secret_key_manager = KeyManager(app_resolver, 'secret')
