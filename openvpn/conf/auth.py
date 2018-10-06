#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import sys
import requests
import settings
import time

with open(sys.argv[1]) as f:
    username, password = f.readlines()[:2]
    assert username.endswith('\n') and password.endswith('\n')
    username = username[:-1]
    password = password[:-1]
untrusted_ip = os.environ.get('untrusted_ip') or os.environ.get('untrusted_ip6')
untrusted_port = os.environ.get('untrusted_port')

try:
    res = requests.post(
        settings.SERVER_AUTH_URL,
        data=dict(
            username=username,
            password=password,
            untrusted_ip=untrusted_ip,
            untrusted_port=untrusted_port,
            client_secret=settings.CLIENT_SECRET,
        )
    )
    assert True == res.ok
    res = res.json()
    ok = 0 == res['error']
    exception = False
except:
    ok = False
    exception = True

with open(settings.LOG_PATH, 'a') as f:
    json.dump(dict(time=time.time(), username=username, password='', untrusted_ip=untrusted_ip,
        untrusted_port=untrusted_port, ok=ok, exception=exception), f, sort_keys=True)
    f.write('\n')

print('auth: ok={:d} exception={:d}'.format(ok, exception))
if ok:
    exit(0)
exit(1)
