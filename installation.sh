#!/usr/bin/env bash
# This script was created to run in a linux enviroment
# Was tested in a Ubuntu 18.04 machine but should work in a
# Debian enviroment too.

# System-wide requirements
sudo apt-get install python3-venv
sudo apt-get install python3-tk

# Create a virtual enviroment for modules installation
python3 -m venv .venv
# Activate the created enviroment
source .venv/bin/activate

# Install the need requirements
pip3 install -r requirements.txt
