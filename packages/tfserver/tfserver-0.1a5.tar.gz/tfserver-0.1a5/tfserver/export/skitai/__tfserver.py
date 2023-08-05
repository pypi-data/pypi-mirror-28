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
def Predict_pb (was, request, timeout = 10):
	problem = tensor_util.MakeNdarray (request.inputs ["x"])
	print (problem)
	predict_result = tfserver.tfsess.run (app.config.tf_predict_op.name, feed_dict = { app.config.tf_x.name: problem })
	response = predict_pb2.PredictResponse()
	response.outputs ["y"].CopyFrom (
		tensor_util.make_tensor_proto(predict_result.astype('float32'), shape=predict_result.shape)
	)
	return response
	
@app.route ("/predict")
def predict (was, x):
	problem = np.array (x)
	predict_result = tfserver.tfsess.run (app.config.tf_predict_op.name, feed_dict = { app.config.tf_x.name: problem })	
	return was.response.api ({"y": predict_result.astype ("float32").tolist ()})
	