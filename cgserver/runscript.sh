#!/bin/bash

set -ex

service apache2 start

chown user:user cgserver/settings.py

su user -c "python3 manage.py runserver"
