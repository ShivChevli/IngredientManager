#!/usr/bin/env bash

#system setup
apt update && sudo apt upgrade
apt upgrade python3
apt install python3-pip
apt install python3-venv
apt-get install libpangocairo-1.0-0

# clone application
git clone -b NewVersion https://github.com/ShivChevli/IngredientManager.git ~/order_app
cd ~/order_app

# create python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create application data 
python manage.py migrate
python manage.py loaddata ./seedData/orderInventory.json

alias order_app='~/order_app/scripts/run.sh'

order_app