#!/bin/bash

pip3 install -r requirements.txt
pip3 install pre-commit

sudo mkdir -p /server/config
sudo chown -R $USER /server
sudo chmod 766 /server/config

cp database.sqlite /server/config
chown -R vscode:vscode /server

git config --global --add safe.directory .
git config --global user.name Jair
git config --global user.email jair.fehlauer@gmail.com

pre-commit install
pre-commit run
