from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api


api = Api(title="Connecting Traveller")
db = SQLAlchemy()