#!/bin/bash

# Attiva l'ambiente virtuale
source /home/master/flask_coaim/venv/bin/activate

# Avvia l'app Flask
exec python3 /home/master/flask_coaim/coaimed_db_api.py
