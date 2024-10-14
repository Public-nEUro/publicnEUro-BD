#!/bin/bash

if [ -d "repo" ] && [ -d "repo/.git" ]; then
    cd repo && git pull
else
    git clone https://github.com/Public-nEUro/DataCatalogue.git repo
fi

