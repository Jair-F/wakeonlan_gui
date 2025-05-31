#!/bin/bash

./init_env.sh

export FLASK_APP=main
export FLASK_ENV=development
flask run