#!/bin/bash
/opt/conda/bin/python -m pip install --upgrade pip
/opt/conda/bin/pip install -r requirements.txt
/opt/conda/bin/python manage.py collectstatic --noinput
/opt/conda/bin/python manage.py migrate --noinput
