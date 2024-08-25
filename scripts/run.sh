#!/usr/bin/env bash

cd ~/order_app
source .venv/bin/activate -v
git pull 
sleep 20 && cmd.exe /C start http://localhost:8000/orderInventory/ & 
python manage.py runserver 
