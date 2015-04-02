__author__ = 'srwareham'
import sys
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
PROJ_PATH = PARENT_DIR
sys.path.insert(0, PROJ_PATH)
import campaignadvisor