#!/bin/bash

# push csv file to github

DIR="/tmp/daily-house-deal"

test -d "$DIR" && rm -rf "$DIR"

export GH_TOKEN="a3daf10ca081250fa30d5e6549a13882d09988c5"
REPO_URL="https://${GH_TOKEN}@github.com/ox0spy/daily-house-deal.git"

git clone "$REPO_URL" "$DIR" && \
    cp daily-house-deal.csv "$DIR/" && \
    cd "$DIR" && \
    git commit -m "update csv file." daily-house-deal.csv && \
    echo "done"
    # git push origin master
