import json
import os
import requests
import settings
import sys

if __name__ == '__main__':
    nas_ip = os.environ.get('NAS_IP_ADDRESS')
    username = os.environ.get('USER_NAME').strip('"')
    res = requests.post(
        settings.API_URL,
        data=dict(
            username=username,
            key='NT-Password',
            nas_ip=nas_ip,
            api_secret=settings.API_SECRET,
        )
    )
    assert True is res.ok
    res = res.json()
    if 0 == res['error']:
        print(res['nt_password_hash'])
    else:
        print(res['msg'], file=sys.stderr)
        exit(1)
