#!/usr/bin/env bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $parent_path
cd ..
git pull
pip3 install --user -r requirements.txt
python3 manage.py migrate
npm install
./node_modules/.bin/webpack --config webpack.prod.js
