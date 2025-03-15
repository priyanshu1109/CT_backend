from .extensions import db

class User_trip_details(db.Model):
    __tablename__='user_trip_details'
    id = db.Column(db.Integer,primary_key=True)
    username =  db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    mobile = db.Column(db.String,nullable=False)
    source = db.Column(db.String,nullable=False)
    visa_status = db.Column(db.String,nullable=False)
    visa_required = db.Column(db.String,default='N',nullable=False)
    destination = db.Column(db.String,nullable=False)
    start_date = db.Column(db.DateTime,nullable=False)
    end_date = db.Column(db.DateTime,nullable=False)
    land_package = db.Column(db.String,default='N',nullable=False)
    flight_package = db.Column(db.String,default='N',nullable=False)
    hotel_package = db.Column(db.String,default='N',nullable=False)
    itenary = db.relationship('Itenary',backref='user_trip_details',lazy=True)

class Itenary(db.Model):
    __tablename__='itenary'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String,nullable=False)
    day = db.Column(db.Integer,nullable=False)
    user_trip_id = db.Column(db.Integer,db.ForeignKey('user_trip_details.id'),nullable=False)


    

    


    