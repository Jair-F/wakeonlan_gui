#!/bin/bash

./init_env.sh

export FLASK_APP=main
export FLASK_ENV=development
FLASK_ENV=development FLASK_APP=main flask run