#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python scripts/generate_assets_and_seed.py
