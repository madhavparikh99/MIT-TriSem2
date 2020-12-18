from types import MethodDescriptorType
from bson.objectid import ObjectId
from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from functools import wraps
from flask_pymongo import PyMongo
from bson.json_util import dumps,loads
import random
import string
from .controller import *

auth = Blueprint('auth',
                __name__,
                template_folder='templates/auth',
                static_folder='static/auth',
                url_prefix='/')


def password_generator(length):
    letters = string.ascii_lowercase
    rpassword = ''.join(random.choice(letters) for i in range(length))
    return rpassword

@auth.app_errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@auth.route('/pymongo')
def pymongo_testrun():
    
    # print("db_operations:   "+str(db_operations))
    data = db_operations.find({'personal_info.email':"parikh.madhav1999@gmail.com",'personal_info.password':'MADHAVPARIKH'},{'personal_info.entity':1,'_id':0})
    ls_data = list(data)
    json_data = dumps(ls_data)
    print("data:  "+str(json_data))
    return str(json_data)

@auth.route('/login')
def login():
    return render_template('index.html')

@auth.route('/loginscr', methods=['POST'])
def loginscr():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = db_operations.find({'personal_info.password':str(password),'personal_info.email':str(email)},{'personal_info.entity':1,'_id':0})
        ls_data = list(data)
        json_data = dumps(ls_data)
        print("data:  "+json_data[0])
        return json_data[0]
        
        # return redirect(url_for('admin.admintest'))
    return 'loginotp'


# LOGOUT CODE
@auth.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))

@auth.route('/register')
def register():
  return render_template('register.html')

@auth.route('/index')
@login_required
def index_template():
    return render_template('index.html')


@auth.route('/main')
def mainpage():
    return render_template('mainpage.html')


@auth.route('/prac')
@login_required
def prac():
    return render_template('prac.htm.j2')
