# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.signals import setting_changed
from django.utils.module_loading import import_string

IGNORE_EXCEPTIONS = []


class Config(object):
    _ignore_exceptions = []


def update_config(sender=None, setting=None, value=None, enter=False, **kwargs):
    conf._ignore_exceptions = [import_string(a) for a in (getattr(settings, 'CRASHLOG_IGNORE_EXCEPTIONS',
                                      IGNORE_EXCEPTIONS))]


conf = Config()
update_config()

setting_changed.connect(update_config)
