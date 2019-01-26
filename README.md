# PythonImageClassifierApp

This repo is a light-weight micro-service app that allows users to upload an image and have any objects or faces recognized. The application uses Keras with a TensorFlow back-end for the core classification. Flask is used for the REST API. Bootstrap is used as the front-end interface.

For the front-end I used the tutorial created by Traversy Media. See "Python Flask From Scratch" on YouTube.

To run the application use:
$ python app.py

## Installation of the application
You are going to need to install python3.6-dev

$ sudo add-apt-repository ppa:deadsnakes/ppa

$ sudo apt-get install python3.6-dev

Install dependencies with: pip3 install -r requirements.txt

## TODO list

The following items are going to be included in future builds.
* Allow users to choose among several classifiers packages with keras
* Allow users to store images into a folder for easy use
* Integrate Intel Neural Compute Stick 2
* Create button to switch between CPU and VPU for classification
* Allow user to create their own rudimentary model and train this model
* Add asyncio, multiprocessing and multi-threading were convenient
* Ensure the application can run in the cloud with Docker
