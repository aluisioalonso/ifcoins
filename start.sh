#!/bin/bash
set -e
python CriarBD.py
python criar_admin.py
exec gunicorn --bind 0.0.0.0:5002 app:app --workers 3