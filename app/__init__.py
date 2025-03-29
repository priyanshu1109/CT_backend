from flask import Flask
from .extensions import api,db
from .resources import *
from sqlalchemy import text
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQL")


    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)
    
    
    return app