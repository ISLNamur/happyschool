#!/usr/bin/env bash

if hash supervisorctl 2>/dev/null; then
    sudo supervisorctl restart all
fi
