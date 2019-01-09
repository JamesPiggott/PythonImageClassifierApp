# PythonImageClassifierApp

This repo is a light-weight micro-service app that allows users to upload an image and have any objects or faces recognized. The application uses Keras with a TensorFlow back-end for the core classification. Flask is used for the REST API. Bootstrap is used as the front-end interface.

For the front-end I used the tutorial created by Traversy Media as the basis. See tutorial series "Python Flask From Scratch" on YouTube.

To run the application use:

python app.py

## Setting up your Python Virtual Environment
1. Navigate to the project root directory
2. You are going to need to install python3.6-dev
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get install python3.6-dev
3. Install MySQL-server with: sudo apt-get install mysql-server libmysqlclient-dev
4. Activate your virtual environment
5. Install dependencies with: pip3 install -r requirements.txt

## Setting up the database
For this app to work you will need to set up a small MySQL database
