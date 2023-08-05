from skitai.saddle import Saddle
import tfserver
import tensorflow as tf
from tfserver import prediction_service_pb2, predict_pb2
from tensorflow.python.framework import tensor_util
import numpy as np
import os

app = Saddle (__name__)
app.debug = True
app.use_reloader = True

app.access_control_allow_origin = ["*"]
	
@app.shutdown
def shutdown (wasc):
	# loading TF checkpoint
	tfserver.close ()
	
@app.startup
def startup (wasc):
	tfserver.load_model (app.config.tf_model_dir, app.config.get ("tf_config"))
	
@app.route ("/tensorflow.serving.PredictionService/Predict")
def Predict (was, request, timeout = 10):
	feed_dict = {}
	for k, v in request.inputs.items ():
		feed_dict [tfserver.tfsess.input_map [k]] = tensor_util.MakeNdarray (v)	
	outputs = []
	for k, v in tfserver.tfsess.output_map.items ():
		outputs.append ((k, v))	
	predict_results = tfserver.tfsess.run ([op for name, op in outputs], feed_dict = feed_dict)
	
	response = predict_pb2.PredictResponse()	
	for i, result in enumerate (predict_results):	
		predict_result = predict_results [i]
		response.outputs [outputs [i][0]].CopyFrom (
			tensor_util.make_tensor_proto(predict_result.astype('float32'), shape=predict_result.shape)
		)
	return response
	
@app.route ("/predict")
def predict (was, **inputs):
	feed_dict = {}
	for k, v in inputs.items ():
		feed_dict [tfserver.tfsess.input_map [k]] = np.array (v)
	outputs = []
	for k, v in tfserver.tfsess.output_map.items ():
		outputs.append ((k, v))	
	predict_results = tfserver.tfsess.run ([op for name, op in outputs], feed_dict = feed_dict)
	
	response = {}
	for i, result in enumerate (predict_results):	
		predict_result = predict_results [i]		
		response [outputs [i][0]] = predict_result.astype ("float32").tolist ()		
	return was.response.api (response)
	