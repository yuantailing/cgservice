#!/bin/bash

set -ex

if [ ! -d "/var/csvn/data" ]; then
	chown -R data
    mv data /var/csvn/data
fi

rm -rf data
ln -s /var/csvn/data data

su csvn -c "bin/csvn console"
