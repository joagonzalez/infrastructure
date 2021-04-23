#!/bin/bash

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -

source /etc/lsb-release

echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

# Debian: Add the InfluxData repository with the following commands:

# Before adding Influx repository, run this so that apt will be able to read the repository.

sudo apt-get update --fix-missing -y && sudo apt-get install apt-transport-https  -y --fix-missing

# Add the InfluxData key

wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -

source /etc/os-release

sudo apt-get update --fix-missing -y && sudo apt-get install telegraf --fix-missing -y

sudo service telegraf start
