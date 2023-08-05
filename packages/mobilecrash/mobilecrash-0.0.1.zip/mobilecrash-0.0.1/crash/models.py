# -*- coding:UTF-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.

class CrashLog(models.Model):
    login_name = models.CharField(max_length=128)   # 登录账号
    app_version_num = models.CharField(max_length=128, null=True, blank=True)  # app版本号
    phone_version = models.CharField(max_length=128, null=True, blank=True)    # 手机型号
    SDK_version = models.CharField(max_length=128, null=True, blank=True)      # SDK版本
    crash_time = models.DateTimeField(default=datetime.now)     # 闪退时间
    crash_description = models.TextField(max_length=500, null=True, blank=True)    # 闪退异常描述
    bug_status = models.IntegerField(default=1)     # bug状态 1:开启 0:关闭

    def __unicode__(self):
        return self.login_name



