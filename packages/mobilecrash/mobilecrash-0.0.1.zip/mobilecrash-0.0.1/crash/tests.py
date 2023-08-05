# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.conf import settings
from .test_data import crash
from .models import CrashLog
import json

# Create your tests here.


class PublicBaseClass(TestCase):
    def operations(self, method='get', url=None, headers=None, status_code=200, params=None):
        if method == 'get':
            res = self.client.get(url)
        elif method == 'post':
            res = self.client.post(url, data=json.dumps(params), content_type='application/json')
        elif method == 'put':
            res = self.client.put(url, data=json.dumps(params), content_type='application/json')
        elif method == 'patch':
            res = self.client.patch(url, data=json.dumps(params), content_type='application/json')
        elif method == 'delete':
            res = self.client.delete(url)
        else:
            self.assertEqual(method, 'not supported')
        if res.status_code != status_code:
            print res.data
        self.assertEquals(res.status_code, status_code)
        return res

    def setUp(self):
        settings.USE_TZ = False
        self.client = Client()

    def tearDown(self):
        pass


class TestCrashViewCase(PublicBaseClass):
    @classmethod
    def setUpTestData(cls):
        cls.crash = CrashLog.objects.create(**crash.crash_test_data)

    def test_crash_list(self):
        res = self.operations(url=crash.crash_url)
        self.assertEquals(res.data.get('results')[0].get('login_name'), crash.crash_test_data.get('login_name'))

    def test_crash_post(self):
        res = self.operations(url=crash.crash_url, method=crash.post_method, params=crash.crash_post_data,
                              status_code=crash.created_status_code)
        self.assertEquals(res.data.get('login_name'), crash.crash_post_data.get('login_name'))
        self.assertEquals(res.data.get('crash_time'), crash.crash_post_data.get('crash_time'))

    def test_crash_detail(self):
        res = self.operations(url=crash.crash_operate_url.format(pk=self.crash.id))
        self.assertEquals(res.data.get('id'), crash.crash_test_data.get('id'))
        self.assertEquals(res.data.get('crash_time'), crash.crash_test_data.get('crash_time'))

    def test_crash_put(self):
        res = self.operations(url=crash.crash_operate_url.format(pk=self.crash.id), method=crash.put_method,
                              params=crash.crash_post_data)
        self.assertEquals(res.data.get('login_name'), crash.crash_post_data.get('login_name'))
        self.assertEquals(res.data.get('crash_time'), crash.crash_post_data.get('crash_time'))

    def test_crash_patch(self):
        res = self.operations(url=crash.crash_operate_url.format(pk=self.crash.id), method=crash.patch_method,
                              params=crash.crash_post_data)
        self.assertEquals(res.data.get('login_name'), crash.crash_post_data.get('login_name'))
        self.assertEquals(res.data.get('crash_time'), crash.crash_post_data.get('crash_time'))

    def test_crash_delete(self):
        self.operations(url=crash.crash_operate_url.format(pk=self.crash.id), method=crash.delete_method,
                        status_code=crash.delete_status_code)

    def test_crash_search(self):
        res = self.operations(url=crash.crash_search_url.format(login_name=self.crash.login_name))
        self.assertEquals(res.data.get('results')[0].get('crash_time'), crash.crash_test_data.get('crash_time'))