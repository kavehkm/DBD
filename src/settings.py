# standard
import os
import json


# base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# settings file
SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.json')


# snap directory
SNAP_DIR = os.path.join(BASE_DIR, 'snaps')


# load settings
try:
    with open(SETTINGS_FILE, 'rt') as f:
        SETTINGS = json.loads(f.read())
except Exception as e:
    # cannot load user settings
    # log error and load default
    SETTINGS = {}


# databases
DATABASES = SETTINGS.get('databases', [])
