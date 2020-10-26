#!/bin/bash
# Author:       Andrew J. S. 2020
# License:      GPLv3

git reset --hard
git pull
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x16 &
sleep 5
xrandr --query
sleep 5
nohup startx &
sleep 10
xhost + "${HOSTNAME}"
echo "Launched a screen on: ${DISPLAY}"
