#!/usr/bin/env bash
#running version 5.1.16(1)

if [[ ! -f ".gitignore" ]];then
    git init 
    touch .gitignore
    echo ".DS_Store" >> .gitignore
    echo "ver 2.0" >> .gitignore
    echo "tm.txt" >> .gitignore
    echo "torrentdata.txt" >> .gitignore
    echo "ver in development" >> .gitignore
fi

git add .
git commit -m "First MVP ready and working"
git status

git remote add orgin "git@github.com:ms766/1337x-CLTorrentDownloader.git"

git push --set-upstream orgin master