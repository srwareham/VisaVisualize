from app import app
from app import APP_STATIC
import os
import json
from flask.ext.restful.reqparse import RequestParser
from flask import jsonify
try:
    import cPickle as pickle
except ImportError:
    import pickle

MAP_DATA_PATH = os.path.abspath(__file__ + "/../../static/mapdata")
def open_pickle(path):
	path = MAP_DATA_PATH + '/' + path
	print path
	with open(path, 'rb') as pickle_file:
		return pickle.load(pickle_file)

county_statistics = open_pickle('people_indexed.pik')
@app.route('/')

def root():
	return app.send_static_file('index.html')

@app.route('/api/getCountyStatisticsColumns', methods=['GET'])
def get_county_statistics_column():
	return jsonify(data_points=list(county_statistics.columns)), 200

@app.route('/api/getCountyLines', methods=['GET'])
def get_county_lines():
	return app.send_static_file('mapdata/county.json')
	
@app.route('/api/getStateLines', methods=['GET'])
def get_state_lines():
	return app.send_static_file('mapdata/states.json')

@app.route('/api/getCountyStatistics', methods=['POST'])
def get_county_statistics():
	parser = RequestParser()
	parser.add_argument('data_column', required=True, type=str, location='json',
						help='Data column is needed.')
	args = parser.parse_args()
	try:
		series_needed = county_statistics[args.data_column]
		max_value = series_needed.max()
		min_value = series_needed.min()
		json_doc = json.loads(series_needed.to_json())
		return jsonify(county_data=json_doc,
						max_value=max_value,
						min_value=min_value)
	except:
		return 'Column does not exist'
	return 'success', 200


