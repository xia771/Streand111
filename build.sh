#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Making migrations..."
python manage.py migrate --noinput
