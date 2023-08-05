import os
import tensorflow as tf
import time

__version__ = "0.1a24"

class Session:
	def __init__ (self, model_dir, tfconfig = None):
		self.model_dir = model_dir
		self.tfconfig = tfconfig
		
		self.tfsess = tf.Session (config = tfconfig)
		self.tfsess.run (tf.global_variables_initializer())	
		meta = tf.saved_model.loader.load (
			self.tfsess, 
			[tf.saved_model.tag_constants.SERVING], 
			model_dir
		)
		
		self.signature_def_name, signature_def = meta.signature_def.popitem ()	
		self.input_map = {}
		self.output_map = {}

		for k, v in signature_def.inputs.items ():
			self.input_map [k] = v.name
		for k, v in signature_def.outputs.items ():
			self.output_map [k] = v.name
	
	def run (self, *args, **kargs):
		return self.tfsess.run (*args, **kargs)
		
	def close (self):
		self.tfsess.close ()
	
tfsess = None
			
def load_model (model_dir, tfconfig = None):
	global tfsess	
	tfsess = Session (model_dir, tfconfig)
	
def close ():
	global tfsess	
	tfsess.close ()
	tfsess = None
	