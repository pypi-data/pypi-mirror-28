# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import uuid
import logging
import collections
from collections import Mapping, OrderedDict
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import MiddlewareNotUsed, PermissionDenied, SuspiciousOperation
from django.conf import settings
from django.utils import six, timezone
from django.contrib import auth
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models import F, Q
from django.db.models import Count, Avg, Sum, Aggregate, Max, Min
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.urls import reverse
from django.shortcuts import resolve_url
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe, mark_for_escaping
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_unicode, smart_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.fields import get_error_detail, set_value, empty
from rest_framework.compat import set_rollback
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils import formatting
from rest_framework import serializers, viewsets, generics, mixins
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet, ViewSetMixin
from rest_framework.decorators import api_view, authentication_classes, throttle_classes, permission_classes

from .models import *
from .chart import ChartMixin, ChartView, EChartsMixin, EChartsView, JSONEncoder

logger = logging.getLogger(__name__)


class EChartAPIView(EChartsMixin, APIView):
    chart = {}

    def get(self, request, *args, **kwargs):
        content = self.get_chart_response(request, *args, **kwargs)
        result = json.dumps(content, cls=JSONEncoder)
        logger.debug(u"option:{}".format(result))
        return HttpResponse(result)


