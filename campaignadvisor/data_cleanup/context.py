__author__ = 'srwareham'
import sys
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
GRANDPARENT_DIR = os.path.dirname(PARENT_DIR)
PROJ_PATH = GRANDPARENT_DIR
sys.path.insert(0, PROJ_PATH)
import campaignadvisor