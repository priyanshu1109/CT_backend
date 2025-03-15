from flask import Flask
from .extensions import api,db
from .resources import *
from sqlalchemy import text
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://connekpi_priyanshu:Priyanshu%40123@103.50.161.108/connekpi_connecting'


    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    
    
    return app