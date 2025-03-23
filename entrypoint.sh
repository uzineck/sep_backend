#!/bin/bash
# !WARNING This file should not contain last blank line
# gunicorn core.project.wsgi:application -w 2 --bind 0.0.0.0:8000 --reload
python manage.py runserver 0.0.0.0:8000