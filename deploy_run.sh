#!/bin/bash

./init_env.sh

export FLASK_APP=main
export FLASK_ENV=development


flask run -p 5001 --host "0.0.0.0"
