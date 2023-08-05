# -*- coding:UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import api_views

urlpatterns = [
    url(r'^api/crashs/$',api_views.CrashListView.as_view()),
    url(r'^api/crashs/(?P<pk>[0-9]+)/$',api_views.CrashDetailView.as_view()),
]