#!/bin/bash

mkdir -p /server/config
cp database.sqlite /server/config
chown -R vscode:vscode /server
