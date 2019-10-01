#!/usr/bin/env python3

import os
import subprocess

if __name__ == '__main__':
    domains = os.environ['DOMAINS'].split(':')
    args = ['certbot', 'certonly', '--dns-route53', '--agree-tos', '--register-unsafely-without-email', '--cert-name', 'cgservice', '--keep-until-expiring', '--non-interactive']
    for domain in domains:
        args += ['-d', domain]
    retcode = subprocess.call(args)
    exit(retcode)
