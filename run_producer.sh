#! /bin/bash

source ./venv/bin/activate
cd ./src
python ./kafka_server.py
cd ..
deactivate
