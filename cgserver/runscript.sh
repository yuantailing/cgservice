#!/bin/bash

set -ex

service apache2 start
useradd user
su user -c "python3 manage.py runserver"
