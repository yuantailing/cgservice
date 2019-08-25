import json
import os
import requests
import settings
import sys

if __name__ == '__main__':
    username = os.environ.get('USER_NAME').strip('"')
    nas_ip = os.environ.get('NAS_IP_ADDRESS')
    res = requests.post(
        settings.API_URL,
        data=dict(
            username=username,
            nas_ip=nas_ip,
            key='NT-Password',
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
