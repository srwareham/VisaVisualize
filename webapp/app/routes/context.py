__author__ = 'srwareham'
import sys
import os

ROUTES_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(ROUTES_DIR)
WEBAPP_DIR = os.path.dirname(APP_DIR)
PROJ_PATH = os.path.dirname(WEBAPP_DIR)
sys.path.insert(0, PROJ_PATH)
import campaignadvisor