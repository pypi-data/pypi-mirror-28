import os
import tensorflow as tf
import time

__version__ = "0.1a6"

tfsess = None

def load_model (model_dir, tfconfig = None):
	global tfsess
		
	_tfsess = tf.Session (config = tfconfig)
	_tfsess.run (tf.global_variables_initializer())	
	tf.saved_model.loader.load (
		_tfsess, [tf.saved_model.tag_constants.SERVING], model_dir
	)		
	tfsess = _tfsess
	
def close ():
	global tfsess
	
	tfsess.close ()
	