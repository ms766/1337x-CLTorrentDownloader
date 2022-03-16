#!#!/usr/bin/env bash

open -a "qBittorrent"

#osascript -e 'tell application "Finder"' -e 'set visible of process "qBittorrent" to false' -e 'end tell'

sleep 1

osascript -e 'tell application "System Events" to set visible of process "qBittorrent" to false'
