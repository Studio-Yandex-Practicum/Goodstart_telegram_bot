#!/bin/bash

python manage.py collectstatic --noinput
export PYTHONPATH=${PWD}
python manage.py migrate --check

status=$?
if [[ $status != 0 ]]; then
  python manage.py migrate
fi
exec "$@"