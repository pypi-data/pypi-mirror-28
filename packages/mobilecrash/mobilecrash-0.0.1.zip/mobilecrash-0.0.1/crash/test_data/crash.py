# -*- coding:UTF-8 -*-
from __future__ import unicode_literals


crash_url = '/crash/api/crashs/'
crash_operate_url = '/crash/api/crashs/{pk}/'
crash_search_url = '/crash/api/crashs/?login_name={login_name}'

post_method = 'post'
put_method = 'put'
patch_method = 'patch'
delete_method = 'delete'

created_status_code = 201
delete_status_code = 204

crash_test_data = {
    "id": 1,
    "login_name": "test",
    "app_version_num": "test",
    "phone_version": "test",
    "SDK_version": "test",
    "crash_time": "2018-01-10T12:00:00",
    "crash_description": "test",
    "bug_status": 1
}

crash_post_data = {
    "login_name": "test_post",
    "app_version_num": "",
    "phone_version": "",
    "SDK_version": "",
    "crash_time": "2018-01-10T15:38:00",
    "crash_description": "",
    "bug_status": 1
}