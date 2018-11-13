# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image,ImageOps
import numpy as np
import flask
import io
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None

def load_model():
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
	import pickle
	filename='LinearRegressionDecathlonP2.sav'
	global model
	model = pickle.load(open(filename, 'rb'))

def padding_image(image_input):
    width, height = image_input.size
    max_size = max(width, height)
    padding = ((max_size - width)//2, (max_size - height)//2, (max_size - width )//2, (max_size - height)//2)
    image_trans = ImageOps.expand(image_input,padding,fill = 'black')
    return image_trans

def resize_image(image_input, size):
    new_size = [size,size] 
    image_size = image_input.resize(new_size, Image.ANTIALIAS)
    return image_size

def predict_imagen(image):
    image = padding_image(image)
    image = resize_image(image, 128)
    image = ImageOps.autocontrast(image, cutoff=0, ignore=None)
    image_array = np.asarray(image).flatten()    
    ds = []
    ds.append(image_array)
    return ds

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# read the image in PIL format
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))

			# preprocess the image and prepare it for classification
			ds = predict_imagen(image)
			global graph
			global model
			with graph.as_default():
			# classify the input image and then initialize the list
			# of predictions to return to the client
				
			data["predictions"] = []
			data["predictions"].append(preds[0])
			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	graph = tf.get_default_graph()
	app.run()
