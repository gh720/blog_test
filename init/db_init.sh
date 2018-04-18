#!/usr/bin/env bash

set -ex 

python3 manage.py flush --noinput
python3 manage.py migrate
python3 manage.py loaddata init/auth.json
python3 manage.py loaddata init/posts.json
python3 manage.py runserver 0.0.0.0:8001
