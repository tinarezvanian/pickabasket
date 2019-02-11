from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models.Users import User
from models.Users import db
# import re
import os
# import io
# import csv
import modelcode
from wtforms import Form, FloatField, validators, SubmitField, FieldList
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
# import flask_excel as excel

from werkzeug import secure_filename
# from flask_cache import Cache
import pandas as pd
# import math
#import json

# Packages from model----------------------


import pandas as pd
import numpy as np
import networkx as nx
import random
import efficient_apriori
from pyvis.network import Network
# import apyori
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
# from io import BytesIO

# import base64
import mpld3
#import json


# Packages from model----------------------


class UploadForm(FlaskForm):
    validators = [
         # FileRequired(message='There was no file!')
         # FileAllowed(['csv'], message='Must be a CSV file!')
    ]
    input_file = FileField('', validators=validators)
    submit = SubmitField(label="Upload")
    uploads = FieldList(FileField())


import sys

if sys.version_info[0] >= 3:
    unicode = str

# cache = Cache(config={'CACHE_TYPE': 'simple'})

# setup the app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "SuperSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# cache.init_app(app)
# cache.clear()


db.init_app(app)
bcrypt = Bcrypt(app)

# setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# create the db structure
with app.app_context():
    db.create_all()


#
# Model
class InputForm(Form):
    r = FloatField(validators=[validators.InputRequired()])


####  setup routes  ####
# @app.route('/')
# # @login_required
# def index():
#     return render_template('index.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    # clear the inital flash message
    session.clear()
    if request.method == 'GET':
        return render_template('login.html')

    # get the form data
    username = request.form['username']
    password = request.form['password']

    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    # query the user
    registered_user = User.query.filter_by(username=username).first()

    # check the passwords
    if registered_user is None and bcrypt.check_password_hash(registered_user.password, password) == False:
        flash('Invalid Username/Password')
        return render_template('login.html')

    # login the user
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')

    # get the data from our form
    password = request.form['password']
    conf_password = request.form['confirm-password']
    username = request.form['username']
    email = request.form['email']

    # make sure the password match
    if conf_password != password:
        flash("Passwords do not match")
        return render_template('register.html')

    # check if it meets the right complexity
    check_password = password_check(password)

    # generate error messages if it doesnt pass
    if True in check_password.values():
        for k, v in check_password.iteritems():
            if str(v) is "True":
                flash(k)

        return render_template('register.html')

    # hash the password for storage
    pw_hash = bcrypt.generate_password_hash(password)

    # create a user, and check if its unique
    user = User(username, pw_hash, email)
    u_unique = user.unique()

    # add the user
    if u_unique == 0:
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('login'))

    # else error check what the problem is
    elif u_unique == -1:
        flash("Email address already in use.")
        return render_template('register.html')

    elif u_unique == -2:
        flash("Username already in use.")
        return render_template('register.html')

    else:
        flash("Username and Email already in use.")
        return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# @app.route('/charts')
# def charts():
#     return render_template('charts.html', user=current_user)


# @app.route('/tables')
# def tables():
#     return render_template('tables.html', user=current_user)


# @app.route('/forms')
# def forms():
#     return render_template('forms.html', user=current_user)
#
#
# @app.route('/bootstrap-elements')
# def bootstrap_elements():
#     return render_template('bootstrap-elements.html', user=current_user)
#
#
# @app.route('/bootstrap-grid')
# def bootstrap_grid():
#     return render_template('bootstrap-grid.html', user=current_user)

#
# @app.route('/iframetest')
# def iframetest():
#     df = pd.read_csv('static/data.csv').drop('Open', axis=1)
#     # df = pd.read_csv('static/confidence_df.csv').drop('Open', axis=1)
#
#     chart_data = df.to_dict(orient='records')
#     chart_data = json.dumps(chart_data, indent=2)
#     data = {'chart_data': chart_data}
#     return render_template('iframetest.html', data=data, user=current_user)


# @app.route('/ehsanjs')
# def ehsanjs():
#     df = pd.read_csv('static/data.csv').drop('Open', axis=1)
#     chart_data = df.to_dict(orient='records')
#     chart_data = json.dumps(chart_data, indent=2)
#     data = {'chart_data': chart_data}
#     return render_template("ehsanjs.html", data=data, user=current_user)


# @app.route('/input_page',methods=["GET", "POST"])
# def input_page():
#     form = InputForm(request.form)
#     if request.method == 'POST' and form.validate():
#         r = form.r.data
#         s = compute(r)
#         return render_template("output_page.html", user=current_user, form=form, s=s)

#     else:
#         s = 1.2345
#         return render_template("input_page.html", user=current_user, form=form, s=s)

# @app.route('/input_page', methods=['GET', 'POST'])
# def input_page():
#     form = UploadForm()
#     for i in range(1):
#         form.uploads.append_entry()

#     filedata = []
#     if request.method == 'POST' and form.validate_on_submit():
#         for upload in form.uploads.entries:
#             filedata.append(upload)
#         return render_template('output_page.html', form=form, user=current_user, filedata=filedata)
#     else:
#         return render_template('input_page.html', form=form, user=current_user, filedata=filedata)


@app.route('/', methods=['GET', 'POST'])
# @cache.cached(timeout=10)
def output_page():
    form = UploadForm()
    for i in range(1):
        form.uploads.append_entry()
        filedata = []

        if request.method == 'POST' and form.validate_on_submit():
            for upload in form.uploads.entries:
                filedata.append(upload)


                if len(filedata) >1:

                    file = request.files['file']
                    data = os.path.join('static', 'inputfile_arm.csv')
                    filename = secure_filename(file.filename)
                    file.save(data)



                # stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                # csv_input = csv.reader(stream)
            # print("file contents: ", file_contents)
            # print(type(file_contents))
            # print(csv_input)
            # for row in csv_input:
            #     print(row)

            return render_template('output_page.html', form=form, user=current_user, filedata=filedata,
                                   randomvar='sasa')
        else:
            return render_template('input_page.html', form=form, user=current_user, filedata=filedata, randomvar='sasa')


# @app.route('/EDA', methods=['GET', 'POST'])
# # @cache.cached(timeout=0)
# def EDA():
#     modelcodef.edafunc()
#     form = UploadForm()
#     if request.method == 'POST' and form.validate_on_submit():
#
#         # input_file = request.files['input_file']
#         return redirect(url_for('EDA'))
#     else:
#         return render_template('EDA.html', form=form, user=current_user)  # 'static/images/7.png'


@app.route('/simul', methods=['GET', 'POST'])
# @cache.cached(timeout=0)
# cache.clear()
def simul():
    modelcode.simulfunc()
    form = UploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        # input_file = request.files['input_file']
        e = pd.read_csv('static/soft_clusters.csv')
        f = pd.read_csv('static/clusters_out_df.csv')
        # import modelcode
        return render_template('simul.html', form=form, user=current_user, data1=e.to_html(), data2=f.to_html())



    else:
        e = pd.read_csv('static/soft_clusters.csv')
        f = pd.read_csv('static/clusters_out_df.csv')
        return render_template('simul.html', form=form, user=current_user, data1=e.to_html(), data2=f.to_html())
        # import modelcode


@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/settings')
def settings():
    return render_template('settings.html', user=current_user)


####  end routes  ####


# required function for loading the right user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# check password complexity
def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
        credit to: ePi272314
        https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions
    """

    # calculating the length
    length_error = len(password) <= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    ret = {
        'Password is less than 8 characters': length_error,
        'Password does not contain a number': digit_error,
        'Password does not contain a uppercase character': uppercase_error,
        'Password does not contain a lowercase character': lowercase_error,
        'Password does not contain a special character': symbol_error,
    }

    return ret



if __name__ == "__main__":
    app.run()
  
