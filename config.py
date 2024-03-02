# from flask import Flask
# from flask_mysqldb import MySQL
# import mysql.connector as msc
# from app import app
# # app = Flask(__name__)
# # app.config['MYSQL_HOST'] = 'localhost'
# # app.config['MYSQL_USER'] = 'root'
# # app.config['MYSQL_PASSWORD'] = 'root'
# # app.config['MYSQL_DB'] = 'career_module'
# conn = msc.connect(host = "localhost", user = "root",passwd = "root", database = "career_module")  
# #creating the cursor object  
# cursor = conn.cursor() 
# mysql = MySQL(app)

import os
from dotenv import load_dotenv

from sqlalchemy.engine import create_engine

load_dotenv()

DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

CONN = create_engine(DATABASE_URL)


class Config(object):

    """ Base configuration class  """   

    DEBUG = False
    Testing = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changeds'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

class DevelopmentConfig(Config):

    """ configuration for the Development environment. """

    DEVELOPMENT = True
    DEBUG = True

