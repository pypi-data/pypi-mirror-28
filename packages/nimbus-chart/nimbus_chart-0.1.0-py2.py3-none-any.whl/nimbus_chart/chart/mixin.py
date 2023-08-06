# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import uuid
import copy
import logging
import calendar
import datetime
import decimal
import collections
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import widgets
from django.contrib.admin.utils import label_for_field, lookup_field
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import resolve_url
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate, Max, Min
from django.db.models.fields import BLANK_CHOICE_DASH
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.sessions.models import Session
from django.utils.html import escape
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_unicode, force_unicode
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, TemplateView
from django.urls import reverse
from django.shortcuts import resolve_url
from django.shortcuts import render_to_response, render
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_unicode
from django.template import RequestContext
from .. import constants

__all__ = [
    "ChartMixin",
    "ChartView",
    "JSONEncoder",
]
logger = logging.getLogger(__name__)


class JSONEncoder(DjangoJSONEncoder):
    pass


class ChartMixin(object):
    chart = {}

    def get_chart_response(self, request, *args, **kwargs):
        if not self.chart:
            return HttpResponseNotFound()
        chart_type = self.get_chart_type(self.chart)
        logger.debug(u"chart_type:{} self.chart:{}".format(chart_type, self.chart))
        xfield = self.chart['x-field']
        yfields = self.chart['y-field']
        yfields = (yfields,) if not isinstance(yfields, (list, tuple)) else yfields
        response = self.get_chart_data(chart=self.chart, chart_type=chart_type, xfield=xfield, yfields=yfields)
        return response or {}

    def get_chart_type(self, chart):
        if isinstance(chart, dict):
            return chart.get("chart_type", constants.CHART_TYPE_LINE)
        return constants.CHART_TYPE_LINE

    def get_chart_data(self, chart=None, chart_type=None, xfield=None, yfields=None):
        raise NotImplementedError

    def get_chart_xfiled(self, chart=None, xfield=None, obj=None, ):
        if isinstance(obj, dict):
            value = obj.get(xfield, None)
        else:
            value = getattr(obj, xfield, None)
        return value

    def get_chart_yfiled(self, chart=None, yfield=None, obj=None, ):
        if isinstance(obj, dict):
            value = obj.get(yfield, None)
        else:
            value = getattr(obj, yfield, None)
        return value

    def get_chart_label(self, chart=None, option=None, yfield=None):
        key = u"{}_label".format(yfield)
        if isinstance(option, dict):
            value = option.get(key, "")
        else:
            value = ""
        return value


class ChartView(ChartMixin, View):

    def get(self, request, *args, **kwargs):
        content = self.get_chart_response(request, *args, **kwargs)
        result = json.dumps(content, cls=JSONEncoder)
        logger.debug(u"option:{}".format(result))
        return HttpResponse(result)

