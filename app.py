import os
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
import flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug.utils import secure_filename
from PIL import Image
import sqlite3
import io

import multiprocessing as mp
from classifier.process import Process

app = Flask(__name__)
model = None
UPLOAD_FOLDER = os.path.basename('images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kane2026'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

database = "database/kerasapp_db.sqlite"

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = sqlite3.connect(database)
        c = cur.cursor()

        # Execute query
        c.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password,))

        # Commit to DB
        cur.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = sqlite3.connect(database)
        c = cur.cursor()

        # Get user by username
        result = c.execute("SELECT * FROM users WHERE username =?", (username,))

        if result:
            # Get stored hash
            data = c.fetchone()

            if data is None:
                cur.close()
                error = 'Username not found'
                return render_template('login.html', error=error)

            password = data[4]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)

            # Close connection
            cur.close()

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    print()
    return render_template('dashboard.html')


# Classify image
@app.route('/classify_image', methods=['GET', 'POST'])
@is_logged_in
def classify_image():

    # ensure an image was properly uploaded to our endpoint
    if request.method == 'POST':

        if request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()

            model_choice = request.form['model']

            if "ResNet50" not in model_choice :
                print("Maybe we should load a new model:", model_choice)

                # process = mp.Process(target=classify_process.process_model_request, args=(model_choice))
                # process.start()
                # process.join()

                # classify_process.process_model_request(model_choice)
            else:
                print("ResNet50 is already loaded")

            # f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            # file.save(f)

            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = classify_process.prepare_image(image, target=(224, 224))

            data = classify_process.perform_inference(image)

        # return the data dictionary as a JSON response
        # return flask.jsonify(data)

    print("Results: ", data)
    # return redirect(url_for('dashboard', args=data))

    return render_template('dashboard.html', msg=data)

if __name__ == '__main__':
    app.secret_key='secret123'
    print(("* Loading Keras model and Flask starting server..."
            "please wait until server has fully started"))
    classify_process = Process()
    app.run(debug=True)
