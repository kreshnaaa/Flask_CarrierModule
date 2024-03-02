# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import psycopg2
# import os
# from flask_cors import CORS
# from config import DATABASE, DATABASE_URL, DATABASE_PASSWORD,DATABASE_USERNAME
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from flask_cors import CORS
from config import DATABASE, DATABASE_URL, DATABASE_PASSWORD,DATABASE_USERNAME
from sqlalchemy.ext.automap import automap_base
from flask_marshmallow import Marshmallow
from flask_mail import *
from flask import *  

app = Flask(__name__)

CORS(app)

env_config = os.getenv("APP_SETTINGS","config.DevelopmentConfig")
app.config.from_object(env_config)

#Flask-SQLAlchemy will track modifications of objects and emit signals. 
# The default is None, which enables tracking but issues a warning that 
# it will be disabled by default in the future.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
ma = Marshmallow(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)


engine = db.engine
session = db.session


app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER_EMAIL')
app.config['MAIL_SERVER']='smtp.mail.yahoo.com'  
app.config["MAIL_PORT"] =465  
app.config["MAIL_USERNAME"] ='krishna_45@yahoo.com' 
app.config['MAIL_PASSWORD'] ='lqjxzpllfgaowaqq'  
app.config['MAIL_USE_TLS'] =False  
app.config['MAIL_USE_SSL'] =True 

mail = Mail(app)
 

# app.config['MAIL_SENDER'] = os.environ.get('MAIL_SENDER_EMAIL')
# app.config['MAIL_SERVER']='smtp.mail.yahoo.com' 



