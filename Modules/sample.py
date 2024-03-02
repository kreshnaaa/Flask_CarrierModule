from pymysql import NULL
from app import app, db, engine, app, session
import pandas as pd
from matplotlib import collections
#from config import DBConfig,cursor
from flask import Flask,render_template,request,jsonify
import json
from typing import OrderedDict
from db_models import TblAppDetails,create
from psycopg2 import DatabaseError, OperationalError, errors, NotSupportedError, Error, InternalError, ProgrammingError, InterfaceError, IntegrityError


@app.route('/createjob/', methods = ['POST'] )
def createjob():
    try:
        data = request.get_json()
        print(data)
    except Exception as e:
        print(e)


















# from tkinter.tix import Form
# from flask_wtf import FlaskForm
# from wtforms import StringField,SubmitField,FileField,IntegerField,PasswordField
# from wtforms.validators import DataRequired

# class Applicantdata():
#     firstname = StringField('Firstname', validators=[DataRequired()])
#     lastname  = StringField('Lastname', validators=[DataRequired()])
#     emailid   = StringField('Emailid', validators=[DataRequired()])
#     contactno = IntegerField('Contact Number', validators=[DataRequired()])
#     addressl1 = StringField('Address Line 1', validators=[DataRequired()])
#     addressl2 = StringField('Address Line 2')
#     city      = StringField('City', validators=[DataRequired()])
#     pincode   = IntegerField('Pincode', validators=[DataRequired()])
#     state     = StringField('State', validasstors=[DataRequired()])
#     country   = StringField('Country', validators=[DataRequired()])
#     submit    = SubmitField('Submit')
    
    