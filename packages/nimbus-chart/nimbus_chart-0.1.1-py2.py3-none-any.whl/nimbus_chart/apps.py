# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig as DJAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(DJAppConfig):
    name = 'nimbus_chart'
    verbose_name = _('nimbus_chart')

