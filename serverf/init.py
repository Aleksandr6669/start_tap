from ast import ImportFrom
from click import password_option
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashlib import md5
from numpy import True_

# from platformdirs import user_runtime_path
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_login import LoginManager
import datetime
from flask_cors import CORS
import logging
from logging import getLogger
from logging.handlers import SMTPHandler
from flask_sslify import SSLify
#from OpenSSL import SSL


#context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
#context.use_privatekey_file('private.key')
#context.use_certificate_file('certificate.crt')
#context.load_cert_chain('PATH_TO_PUBLIC_KEY','PATH_TO_PRIVATE_KEY')


#context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')
#context.load_cert_chain('PATH_TO_PUBLIC_KEY','PATH_TO_PRIVATE_KEY')





app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
#app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SESSION_COOKIE_SAMESITE'] = "None"
cors = CORS(app, supports_credentials= True)
app.config['SECRET_KEY'] = 'jhgcur3ntu98rht56curch566rtrt'
app.config['DEBAG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
context = ('/home/servet_bak/certificate.crt', '/home/servet_bak/private.key')
sslify = SSLify(app, age=300)

from serverf import back, modls, routs


#app.run(debug=True)
app.run(host = '0.0.0.0', port = 5000
       ,
    #ssl_context='adhoc'
    ssl_context=context
    )
   
