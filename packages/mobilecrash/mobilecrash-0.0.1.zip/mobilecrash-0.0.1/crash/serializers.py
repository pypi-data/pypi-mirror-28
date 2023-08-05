# -*- coding:UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from .models import CrashLog

headers = {'content-type', 'application/json'}

class CrashLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrashLog
        fields = ('id', 'login_name', 'app_version_num', 'phone_version', 'SDK_version',
                    'crash_time', 'crash_description', 'bug_status')

class CrashLogSerializerEdit(serializers.ModelSerializer):

    class Meta:
        model = CrashLog
        fields = ('id', 'login_name', 'app_version_num', 'phone_version', 'SDK_version',
                    'crash_time', 'crash_description', 'bug_status')