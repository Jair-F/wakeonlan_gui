#!/bin/bash

# elevate to root
[[ "$EUID" == 0 ]] || exec sudo -s "$0" "$@"

source init_env.sh

flask run --debug -p 5001 --host "0.0.0.0"
