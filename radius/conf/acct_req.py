import ipaddress
import json
import os
import re
import requests
import settings
import sys

if __name__ == '__main__':
    username = os.environ.get('USER_NAME').strip('"')
    nas_ip = os.environ.get('NAS_IP_ADDRESS')

    if os.environ.get('NAS_PORT_ID', '').strip('"') == 'xauth':
        nas_type = 'xauth'
    elif os.environ.get('CALLING_STATION_ID'):
        assert os.environ.get('FRAMED_PROTOCOL') == 'PPP'
        nas_type = 'pptp'
    else:
        assert os.environ.get('FRAMED_PROTOCOL') == 'PPP'
        nas_type = 'l2tp'

    ip = os.environ.get('CALLING_STATION_ID') or None
    if ip:
        ip = re.match('^(\d+\.\d+\.\d+\.\d+)(\[\d+\])?$', ip.strip('"')).group(1)
    if not ip or ipaddress.ip_address(ip).is_private:
        ip = os.environ.get('FRAMED_IP_ADDRESS')

    res = requests.post(
        settings.API_URL,
        data=dict(
            username=username,
            nas_ip=nas_ip,
            nas_type=nas_type,
            ip=ip,
            account_status_type=os.environ.get('ACCT_STATUS_TYPE'),
            key='Accounting-Request',
            api_secret=settings.API_SECRET,
        )
    )
    assert True is res.ok
    res = res.json()
    if 0 == res['error']:
        pass
    else:
        print(res['msg'], file=sys.stderr)
        exit(1)
