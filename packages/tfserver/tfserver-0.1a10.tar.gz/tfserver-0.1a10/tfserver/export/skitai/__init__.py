import tensorflow as tf

def _bootstrap (pref):
	gpu_options = tf.GPUOptions (per_process_gpu_memory_fraction = pref.config.gpu_memory)	
	_tfsess = tf.Session (config = tf.ConfigProto(gpu_options=gpu_options, log_device_placement = False))
	_tfsess.run (tf.global_variables_initializer())	
	tf.saved_model.loader.load (
		_tfsess, [tf.saved_model.tag_constants.SERVING], pref.config.model_dir	
	)	
	pref.tfsess = _tfsess
	print ('------', id (pref.tfsess))
	
	