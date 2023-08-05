# -*- coding:UTF-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import CrashLog
from . import serializers


headers = {'content-type': 'application/json'}

class CrashPagination(PageNumberPagination):
    """
    分页
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class CrashListView(generics.ListCreateAPIView):
    """
    app闪退列表页,分页,搜索,排序
    """
    queryset = CrashLog.objects.all()
    serializer_class = serializers.CrashLogSerializer
    pagination_class = CrashPagination

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('login_name', 'app_version_num', 'phone_version', 'SDK_version', 'crash_time')
    ordering_fields = '__all__'
    ordering = ('-crash_time', )

    def get_queryset(self):
        queryset = CrashLog.objects.all()

        login_name = self.request.query_params.get('login_name')
        app_version_num = self.request.query_params.get('app_version_num')
        phone_version = self.request.query_params.get('phone_version')
        SDK_version = self.request.query_params.get('SDK_version')
        crash_time = self.request.query_params.get('crash_time')
        bug_status = self.request.query_params.get('bug_status')

        if login_name:
            queryset = queryset.filter(login_name=login_name)

        if app_version_num:
            queryset = queryset.filter(app_version_num=app_version_num)

        if phone_version:
            queryset = queryset.filter(phone_version=phone_version)

        if SDK_version:
            queryset = queryset.filter(SDK_version=SDK_version)

        if crash_time:
            queryset = queryset.filter(crash_time=crash_time)

        if bug_status:
            queryset = queryset.filter(bug_status=bug_status)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CrashLogSerializer
        else:
            return serializers.CrashLogSerializerEdit

class CrashDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrashLog.objects.all()
    serializer_class = serializers.CrashLogSerializerEdit




