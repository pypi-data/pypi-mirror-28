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

from pyecharts import (
    Bar,
    Line,
    Line3D,
    Pie,
    Gauge,
    Geo,
    GeoLines,
    Graph,
    Liquid,
    Radar,
    Scatter,
    EffectScatter,
    WordCloud,
    Funnel,
    Map,
    Parallel,
    Polar,
    HeatMap,
    TreeMap,
    Kline,
    Boxplot,

    Style,
    Page,
    Overlap,
    Grid,
    Timeline,
)

from ..constants import *
from .mixin import ChartMixin, JSONEncoder

__all__ = [
    "EChartsMixin",
    "EChartsView",
]
logger = logging.getLogger(__name__)


class EChartsMixin(ChartMixin):

    def get_echarts_data(self, chart=None, chart_type=None, xfield=None, yfields=None):
        raise NotImplementedError

    def get_echarts_options(self, chart=None, chart_type=None, xfield=None, yfields=None, datas=None):
        datas = [] if datas is None else datas
        page = Page()
        title = chart.get("title", "")
        subtitle = chart.get("subtitle", "")
        option = chart.get("option", {})
        x_option = option.get(xfield, {})
        x_format = x_option.pop("x-format", None)
        style = Style(title=title, subtitle=subtitle, **x_option)
        echart = ""
        if chart_type == CHART_TYPE_LINE:
            echart = Line(**style.init_style)
            for i, yfname in enumerate(yfields):
                e_label = self.get_chart_label(chart=chart, option=option, yfield=yfname)
                # e_label = force_unicode(label_for_field(yfname, self.model, model_admin=self))
                e_attrs = []
                e_values = []
                for index, obj in enumerate(datas, start=1):
                    xvalue = self.get_chart_xfiled(chart=chart, xfield=xfield, obj=obj)
                    yvalue = self.get_chart_yfiled(chart=chart, yfield=yfname, obj=obj)
                    e_attrs.append(xvalue)
                    e_values.append(yvalue)
                kwargs = option.get(yfname, {})
                echart.add(e_label, e_attrs, e_values, **kwargs)
        elif chart_type == CHART_TYPE_BAR:
            echart = Bar(**style.init_style)
            for i, yfname in enumerate(yfields):
                e_label = self.get_chart_label(chart=chart, option=option, yfield=yfname)
                # e_label = force_unicode(label_for_field(yfname, self.model, model_admin=self))
                e_attrs = []
                e_values = []
                for index, obj in enumerate(datas, start=1):
                    xvalue = self.get_chart_xfiled(chart=chart, xfield=xfield, obj=obj)
                    yvalue = self.get_chart_yfiled(chart=chart, yfield=yfname, obj=obj)
                    e_attrs.append(xvalue)
                    e_values.append(yvalue)
                kwargs = option.get(yfname, {})
                echart.add(e_label, e_attrs, e_values, **kwargs)
        elif chart_type == CHART_TYPE_PIE:
            echart = Pie(**style.init_style)
            for i, yfname in enumerate(yfields):
                e_label = self.get_chart_label(option=option, yfield=yfname)
                # e_label = force_unicode(label_for_field(yfname, self.model, model_admin=self))
                e_attrs = []
                e_values = []
                for index, obj in enumerate(datas, start=1):
                    xvalue = self.get_chart_xfiled(chart=chart, xfield=xfield, obj=obj)
                    yvalue = self.get_chart_yfiled(chart=chart, yfield=yfname, obj=obj)
                    e_attrs.append(xvalue)
                    e_values.append(yvalue)
                kwargs = option.get(yfname, {})
                echart.add(e_label, e_attrs, e_values, **kwargs)
        elif chart_type == CHART_TYPE_LIQUID:
            echart = Liquid(**style.init_style)
            echart.add(u"Liquid", [0.6])

        elif chart_type == CHART_TYPE_LINE3D:
            echart = Line3D(**style.init_style)

        elif chart_type == CHART_TYPE_GAUGE:
            echart = Gauge(**style.init_style)

        elif chart_type == CHART_TYPE_GEO:
            echart = Geo(**style.init_style)

        elif chart_type == CHART_TYPE_GEOLINES:
            echart = GeoLines(**style.init_style)

        elif chart_type == CHART_TYPE_GRAPH:
            echart = Graph(**style.init_style)

        elif chart_type == CHART_TYPE_RADAR:
            echart = Radar(**style.init_style)
            config = chart.get("config", {})
            echart.config(**config)

        elif chart_type == CHART_TYPE_SCATTER:
            echart = Scatter(**style.init_style)

        elif chart_type == CHART_TYPE_WORDCLOUD:
            echart = WordCloud(**style.init_style)

        elif chart_type == CHART_TYPE_FUNNEL:
            echart = Funnel(**style.init_style)

        elif chart_type == CHART_TYPE_MAP:
            echart = Map(**style.init_style)

        elif chart_type == CHART_TYPE_PARALLEL:
            echart = Parallel(**style.init_style)

        elif chart_type == CHART_TYPE_POLAR:
            echart = Polar(**style.init_style)

        elif chart_type == CHART_TYPE_HEATMAP:
            echart = HeatMap(**style.init_style)

        elif chart_type == CHART_TYPE_TREEMAP:
            echart = TreeMap(**style.init_style)

        elif chart_type == CHART_TYPE_BOXPLOT:
            echart = Boxplot(**style.init_style)

        elif chart_type == CHART_TYPE_KLINE:
            echart = Kline(**style.init_style)

        elif chart_type == CHART_TYPE_TIMELINE:
            echart = Timeline(**x_option)

        elif chart_type == CHART_TYPE_OVERLAp:
            echart = Overlap(**option)

        elif chart_type == CHART_TYPE_GRID:
            echart = Grid(**option)

        elif chart_type == CHART_TYPE_PAGE:
            echart = Page()

        if not echart:
            return copy.deepcopy(DEMO)
            # page.add(echart)
        return echart.options

    def get_chart_data(self, chart=None, chart_type=None, xfield=None, yfields=None):
        datas = self.get_echarts_data(
            chart=self.chart,
            chart_type=chart_type,
            xfield=xfield,
            yfields=yfields,
        )
        content = self.get_echarts_options(
            chart=self.chart,
            chart_type=chart_type,
            xfield=xfield,
            yfields=yfields,
            datas=datas,
        )
        return content


class EChartsView(EChartsMixin, View):

    def get(self, request, *args, **kwargs):
        content = self.get_chart_response(request, *args, **kwargs)
        result = json.dumps(content, cls=JSONEncoder)
        logger.debug(u"option:{}".format(result))
        return HttpResponse(result)


