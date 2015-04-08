try:
   import cPickle as pickle
except:
   import pickle
import os

PROJECT_ROOT_PATH = os.path.abspath(__file__ + "/../../")
PICKLES_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "pickles")

	
def get_local_path(name):
    	return os.path.join(PICKLES_DIRECTORY, name)

# serialization
def save_pickle(pickle_name):
	f = open(get_local_path(pickle_name), "wb")
	pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
	f.close()

# de-serialization
def load_pickle(pickle_name):
	f = open(get_local_path(pickle_name), "rb")
	try:
		return pickle.load(f)
		f.close()
	except:
        print "Error: invalid pickle name"
    # print f