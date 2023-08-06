import inspect
import os

from django_zero._version import __version__

DEFAULT_DJANGO_SETTINGS_MODULE = 'config.settings'


def configure(django_settings_module=DEFAULT_DJANGO_SETTINGS_MODULE):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_module)
    os.environ.setdefault("DJANGO_BASE_DIR", os.path.dirname(os.path.abspath((inspect.stack()[1])[1])))

    from django_zero.config import settings


__version__ = __version__