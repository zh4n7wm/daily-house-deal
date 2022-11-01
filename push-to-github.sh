#!/bin/bash

# push csv file to github

DIR="/tmp/.daily-house-deal"

test -d "$DIR" && rm -rf "$DIR"

source .envrc
# GH_TOKEN 作为环境变量，在其它地方复制
REPO_URL="https://${GH_TOKEN}@github.com/zhangwm404/daily-house-deal.git"

# set git config
git config --global user.name "zhangwm404"
git config --global user.email "442798+zhangwm404@users.noreply.github.com"

git clone "$REPO_URL" "$DIR" && \
    cp daily-house-deal.csv "$DIR/" && \
    cd "$DIR" && \
    git commit -m "update csv file." daily-house-deal.csv && \
    git push origin master

rm -rf "$DIR"
