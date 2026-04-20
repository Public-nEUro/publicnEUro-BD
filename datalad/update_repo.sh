#!/bin/bash

if [ -d "repo" ] && [ -d "repo/.git" ]; then
    cd repo && git fetch origin && git reset --hard origin/master
else
    git clone https://github.com/Public-nEUro/DataCatalogue.git repo
fi

