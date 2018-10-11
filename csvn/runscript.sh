#!/bin/bash

set -ex

if [ ! -d "/var/csvn/data" ]; then
	chown -R csvn:csvn data
    mv data /var/csvn/data
fi

rm -rf data
ln -s /var/csvn/data data

su csvn -c "bin/csvn-httpd start"

su csvn -c "bin/csvn console"
