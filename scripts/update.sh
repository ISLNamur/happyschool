#!/usr/bin/env bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd $parent_path
cd ..
git pull
uv sync
uv run ./manage.py migrate
wget https://test.happyschool.be/media/bundles.tar.bz2
tar -xf bundles.tar.bz2
