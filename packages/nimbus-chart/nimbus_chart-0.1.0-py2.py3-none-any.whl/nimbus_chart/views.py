# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import uuid
import logging
import collections
from django.contrib import auth
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate, Max, Min
from django.db.models.signals import post_save, post_delete
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.safestring import mark_safe, mark_for_escaping
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import MiddlewareNotUsed, PermissionDenied, SuspiciousOperation
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, TemplateView
from django.urls import reverse
from django.shortcuts import resolve_url
from django.shortcuts import render_to_response, render
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_unicode
from django.template import RequestContext

from .models import *
from .chart import ChartMixin, ChartView, EChartsMixin, EChartsView, JSONEncoder

logger = logging.getLogger(__name__)


class EChartsBackendView(TemplateView):
    template_name = 'nimbus_chart/echarts.html'
    chart_title = "ECharts"
    chart_url = None

    def get_chart_title(self):
        return self.chart_title

    def get_chart_url(self):
        raise NotImplementedError()

    def get_chart_height(self):
        return '400px'

    def get_chart_width(self):
        return '100%'

    def get_context_data(self, **kwargs):
        params = {
            "chart_title": self.get_chart_title(),
            "chart_url": self.get_chart_url(),
            "chart_width": self.get_chart_width(),
            "chart_height": self.get_chart_height(),
        }
        kwargs.update(params)
        return super(EChartsBackendView, self).get_context_data(**kwargs)


class EChartsView(EChartsMixin, View):
    chart = {}

    def get(self, request, *args, **kwargs):
        content = self.get_chart_response(request, *args, **kwargs)
        result = json.dumps(content, cls=JSONEncoder)
        logger.debug(u"option:{}".format(result))
        return HttpResponse(result)





