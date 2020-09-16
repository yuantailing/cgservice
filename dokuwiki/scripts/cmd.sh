#!/bin/bash -e

service apache2 start
python3 $(dirname $(realpath "$0"))/idle.py
