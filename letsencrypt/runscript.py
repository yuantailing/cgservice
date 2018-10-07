#!/usr/bin/env python

import os
import subprocess

if __name__ == '__main__':
    roots = os.environ['ROOTS'].split(':')
    domains = os.environ['DOMAINS'].split(':')
    assert len(roots) == len(domains)
    args = ['certbot', 'certonly', '--webroot', '--agree-tos', '--register-unsafely-without-email', '--cert-name', 'cgservice', '--keep-until-expiring', '--non-interactive']
    for root, domain in zip(roots, domains):
        args += ['-w', root, '-d', domain]
    retcode = subprocess.call(args)
    exit(retcode)
