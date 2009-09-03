# -*- coding: utf-8 -*-
from deps import DependencyResolver
import os as _os

class AppInfo(object):
    def __init__(self, full_path):
        self._full_path = full_path

    def root_urls(self):
        urls = (
            ( r"^%s/" % a.name(),               include( a.name() )),
        )
        return urls

    def template_paths(self):
        dirs = []

        template_dir = _os.path.join(self._full_path, 'templates')
        if _os.path.isdir(template_dir):
            dirs.append(template_dir)

        return dirs

    def _default_settings(self):
        class DefaultSettings(object):
            def __init__(self):
                super(DefaultSettings, self).__init__()
                self.APP_DEPENDENCIES = {}
                self.MIDDLEWARE_DEPENDENCIES = {}

        return DefaultSettings()

    def load_settings(self):
        try:
            modname = self.name() + '.quickening'
            mod = __import__(modname).quickening
        except (ImportError, AttributeError):
            mod = self._default_settings()
        return mod

    def app_dependencies(self):
        mod = self.load_settings()
        try:
            deps = mod.APP_DEPENDENCIES
        except AttributeError:
            deps = {}
        return deps

    def middleware_dependencies(self):
        mod = self.load_settings()
        try:
            deps = mod.MIDDLEWARE_DEPENDENCIES
        except AttributeError:
            deps = {}
        return deps

    def name(self):
        n = _os.path.basename(_os.path.abspath(self._full_path))
        assert n != "" and n is not None
        return n

    def path(self):
        return self._full_path

class AppResolver(object):
    def __init__(self, app_root, dep_items={}):
        super(AppResolver, self).__init__(dep_items)

        self._app_root = app_root
        self._apps = []
        self._resolver = DependencyResolver()

        self._load_apps()

    def _load_apps(self):
        app_dir_entries = _os.listdir(self._app_root)
        for fname in app_dir_entries:
            if fname.startswith('.'):
                continue

            full_path = _os.path.join(self._app_root, fname)

            if self._is_app(full_path):
                app = AppInfo(full_path)
                self._apps.append(app)

    def app_info(self):
        return self._apps

    def _is_app(self, dir_path):
        settings_dir = _os.path.join(dir_path, 'quickening')
        settings_file = _os.path.join(dir_path, 'quickening.py')
        return _os.path.isdir(settings_dir) or _os.path.isfile(settings_file)

    def root(self):
        return self._app_root

    def _default_app_deps(self):
        """Returns default apps and their dependencies as a dict"""
        return {
            'quickening':                   None,
            'django.contrib.auth':          None,
            'django.contrib.contenttypes':  ('django.contrib.auth',),
            'django.contrib.sessions':      ('django.contrib.contenttypes',),
            'django.contrib.sites':         ('django.contrib.sessions',),
            'django.contrib.admin':         ('django.contrib.sites',),
            'django.contrib.admindocs':     ('django.contrib.admin',),
        }

    def _default_middleware_deps(self):
        """Returns default middleware and dependencies as a dict"""
        default_deps = {
            'django.middleware.common.CommonMiddleware':            (
            ),

            'django.contrib.sessions.middleware.SessionMiddleware': (
                'django.middleware.common.CommonMiddleware',
            ),

            'django.contrib.auth.middleware.AuthenticationMiddleware': (
                'django.contrib.sessions.middleware.SessionMiddleware',
            ),
        }
        return default_deps

    def installed_apps(self):
        deps = self._default_app_deps()
        for a in self._apps:
            deps.update(a.app_dependencies())
        return self._resolver.resolve(deps)

    def middleware_classes(self):
        deps = self._default_middleware_deps()
        for a in self._apps:
            mod_deps = a.middleware_dependencies()
            print "%s.mod_deps:" % a.name(), mod_deps
            deps.update(mod_deps)

        return self._resolver.resolve(deps)

    def root_urls(self):
        urls = []
        for a in self._apps:
            urls += a.root_urls()
        return urls

    def template_loaders(self):
        return (
            'django.template.loaders.filesystem.load_template_source',
            'django.template.loaders.app_directories.load_template_source',
            #'django.template.loaders.eggs.load_template_source',
        )

    def template_paths(self):
        paths = []
        for a in self._apps:
            paths += a.template_paths()
        return paths

    def _default_root_urls(self):
        return (
            (r'^admin/doc/',        include('django.contrib.admindocs.urls')),
            (r'^admin/',            include(admin.site.urls)),
        )

    def url_patterns(self):
        root_urls = self._default_root_urls()

        for a in self._apps:
            root_urls += a.root_urls()

        return root_urls

app_root = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..'))
app_resolver = AppResolver(app_root)
