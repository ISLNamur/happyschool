#!/usr/bin/env bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $parent_path
cd ..
git pull
rm Pipfile.lock
pipenv install
pipenv run ./manage.py migrate
wget https://test.happyschool.be/static/bundles.tar.bz2 
tar -xf bundles.tar.bz2
