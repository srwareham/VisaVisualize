from flask import Flask
import os
app = Flask(__name__, static_url_path='')
app.config.from_object('config')


# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')


from app.routes import index

