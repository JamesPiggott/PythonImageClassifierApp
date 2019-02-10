from keras.applications import *
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import numpy as np

class Process:

    # model_choice

    def __init__(self):
        print()
        self._target = 224

    def process_model_request(self, model_name):
        if 'ResNet50' in model_name:
            self.model = ResNet50(weights='imagenet')
            self.model_choice = "ResNet50"
            self.target = 224
        if 'VGG16' in model_name:
            self.model = VGG16(weights='imagenet')
            self.model_choice = "VGG16"
            self._target = 224
        if 'VGG19' in model_name:
            self.model = VGG19(weights='imagenet')
            self.model_choice = "VGG19"
            self._target = 224
        if 'Xception' in model_name:
            self.model = Xception(weights='imagenet')
            self.model_choice = "Xception"
            self._target = 299
        if 'InceptionV3' in model_name:
            self.model = InceptionV3(weights='imagenet')
            self.model_choice = "InceptionV3"
            self._target = 299
        if 'InceptionResNetV2' in model_name:
            self.model = InceptionResNetV2(weights='imagenet')
            self.model_choice = "InceptionResNetV2"
            self._target = 299
        if 'MobileNet' in model_name:
            self.model = MobileNet(weights='imagenet')
            self.model_choice = "MobileNet"
            self._target = 224
        if 'MobileNetV2' in model_name:
            self.model = MobileNetV2(weights='imagenet')
            self.model_choice = "MobileNetV2"
            self._target = 224
        if 'DenseNet121' in model_name:
            self.model = DenseNet121(weights='imagenet')
            self.model_choice = "DenseNet121"
            self._target = 224
        if 'DenseNet169' in model_name:
            self.model = DenseNet169(weights='imagenet')
            self.model_choice = "DenseNet169"
            self._target = 224
        if 'DenseNet201' in model_name:
            self.model = DenseNet201(weights='imagenet')
            self.model_choice = "DenseNet201"
            self._target = 224
        if 'NASNetMobile' in model_name:
            self.model = NASNetMobile(weights='imagenet')
            self.model_choice = "NASNetMobile"
            self._target = 224
        global graph
        graph = tf.get_default_graph()

    # @property
    def get_image_dimension_target(self):
        return (self._target, self._target)

    def load_model(self):
        # load the pre-trained Keras model (here we are using a model
        # pre-trained on ImageNet and provided by Keras, but you can
        # substitute in your own networks just as easily)
        # global model
        self.model = ResNet50(weights="imagenet")
        global graph
        graph = tf.get_default_graph()

    def prepare_image(self, image, target):
        # if the image mode is not RGB, convert it
        if image.mode != "RGB":
            image = image.convert("RGB")

        # resize the input image and preprocess it
        image = image.resize(self.get_image_dimension_target())
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)

        # return the processed image
        return image

    def perform_inference(self, image, queue):
        # initialize the data dictionary that will be returned from the view
        data = {"success": False}

        # classify the input image and then initialize the list
        # of predictions to return to the client
        global graph
        with graph.as_default():

            preds = self.model.predict(image)
            results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True
            self.model = None
        queue.put(data)
