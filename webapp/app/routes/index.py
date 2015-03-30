from app import app
from app import APP_STATIC
import os
import json
@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/getCountyLines', methods=['GET'])
def getCountyLines():
	return app.send_static_file('mapdata/us-counties.json')
