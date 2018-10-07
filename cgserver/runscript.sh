#!/bin/bash

set -ex

service apache2 start

su user -c "python3 manage.py runserver"
