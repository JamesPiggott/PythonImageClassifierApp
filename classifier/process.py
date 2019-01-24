from keras.applications import *
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import numpy as np

model = None

class Process:

    def __init__(self):
        self.load_model()

    def process_model_request(self, model_name):
        global model
        if 'VGG16' in model_name:
            model = VGG16(weights='imagenet')
        if 'VGG19' in model_name:
            model = VGG19(weights='imagenet')
        if 'InceptionV3' in model_name:
            model = InceptionV3(weights='imagenet')
        if 'MobileNet' in model_name:
            model = MobileNet(weights='imagenet')
        global graph
        graph = tf.get_default_graph()

    def load_model(self):
        # load the pre-trained Keras model (here we are using a model
        # pre-trained on ImageNet and provided by Keras, but you can
        # substitute in your own networks just as easily)
        global model
        model = ResNet50(weights="imagenet")
        global graph
        graph = tf.get_default_graph()

    def prepare_image(self, image, target):
        # if the image mode is not RGB, convert it
        if image.mode != "RGB":
            image = image.convert("RGB")

        # resize the input image and preprocess it
        image = image.resize(target)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)

        # return the processed image
        return image

    def perform_inference(self, image):
        # initialize the data dictionary that will be returned from the view
        data = {"success": False}

        # classify the input image and then initialize the list
        # of predictions to return to the client
        with graph.as_default():

            preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True
        return data
