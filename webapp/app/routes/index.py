from app import app
from app import APP_STATIC
import os
import json
@app.route('/')
def root():
	return app.send_static_file('index.html')

@app.route('/api/getCountyLines', methods=['GET'])
def getCountyLines():
	return app.send_static_file('mapdata/county.json')
	
@app.route('/api/getStateLines', methods=['GET'])
def getStateLines():
	return app.send_static_file('mapdata/states.json')
