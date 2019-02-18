# PythonImageClassifierApp

This repo is a light-weight micro-service app that allows users to upload an image and have any objects or faces recognized. The application uses Keras with a TensorFlow back-end for the core classification. Flask is used for the REST API. Bootstrap is used as the front-end interface.

For the front-end I used the tutorial created by Traversy Media. See "Python Flask From Scratch" on YouTube.

To run the application use:
$ python app.py

## Installation of the application

Install dependencies with: pip3 install -r requirements.txt

To create a docker image: docker build -t keras .
To run the docker container: docker run -p 5000:5000 keras

## TODO list

The following items are going to be included in future builds.
* Allow users to choose among several classifier packages with keras
* Allow users to store images into a folder for easy use
* Integrate Intel Neural Compute Stick 2
* Create button to switch between CPU and VPU for classification
* Allow user to create their own rudimentary model and train this model
* Add asyncio, multiprocessing and multi-threading were convenient
