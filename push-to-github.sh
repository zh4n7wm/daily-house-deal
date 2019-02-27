#!/bin/bash

# push csv file to github

DIR="/tmp/.daily-house-deal"

test -d "$DIR" && rm -rf "$DIR"

# GH_TOKEN 作为环境变量，在其它地方复制
REPO_URL="https://${GH_TOKEN}@github.com/ox0spy/daily-house-deal.git"

# set git config
git config --global user.name "Junkman"
git config --global user.email "ox0spy@gmail.com"

git clone "$REPO_URL" "$DIR" && \
    cp daily-house-deal.csv "$DIR/" && \
    cd "$DIR" && \
    git commit -m "update csv file." daily-house-deal.csv && \
    git push origin master
