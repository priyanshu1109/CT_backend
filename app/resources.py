import json
from flask_restx import Resource,Namespace

from app.models import Itenary, User_trip_details
from .serializers import *
from .extensions import db
from flask import jsonify, request
from flask_cors import cross_origin
import boto3
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename


load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

BUCKET_NAME = "ctusertrips"


# Initialize S3 Client
s3_client = boto3.client("s3")

ns = Namespace('trip_details',path="/api")


def upload_file(file,folder_name):
    
    filename = secure_filename(file.filename)  # Ensure safe filename
    s3_key = f"{folder_name}/{filename}"  # Create S3 key with folder prefix
    print(filename)
    try:
        # Upload the file to S3
        s3.upload_fileobj(file, BUCKET_NAME, s3_key)
        
        # Generate file URL
        file_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        print(file_url)
        # return jsonify({"message": "File uploaded successfully", "file_url": file_url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@ns.route('/trip_details')
class PatientAPI(Resource):

    @ns.doc(description="Get list of all the patients")
    # @ns.marshal_list_with(patient_serializer)
    def get(self):
        
        '''Get list of all patients'''
        return User_trip_details.query.all()

    # @ns.expect(patient_input_serializer)
    # @ns.marshal_with(patient_serializer)
    def post(self):

        '''Add new patient'''
        print("Received Content-Type:", request.content_type)
        username = request.form['username']
        email= request.form['email']
        mobile= request.form['mobile']
        sourceCity= request.form['sourceCity']
        destinationCity= request.form['destinationCity']
        visaApproved=request.form['visaApproved']
        startDate= request.form['startDate']
        endDate= request.form['endDate']
        landPackage= request.form['landPackage']
        flightPackage= request.form['flightPackage']
        hotelPackage= request.form['hotelPackage']
        activities= request.form['activities']
        # print(activities)
        trip = User_trip_details(
            username=username,
            email=email,
            mobile=mobile,
            source = sourceCity,
            destination = destinationCity,
            visa_status = 'Y' if visaApproved!='false' else 'N',
            start_date = startDate,
            end_date = endDate,
            land_package = 'Y' if landPackage!='false' else 'N',
            flight_package = 'Y' if flightPackage!='false' else 'N',
            hotel_package = 'Y' if hotelPackage!='false' else 'N'
        )
        db.session.add(trip)
        db.session.commit()
        total = 0
        activities = json.loads(activities)
        for a in activities.keys():
            i = Itenary(description=activities[a],day=int(a),user_trip_id=trip.id)
            db.session.add(i)
            total+=1
            trip.itenary.append(i)
        files = {}

        # print(request.files)
        for key, file_list in request.files.lists():
            key_parts = key.replace("files[", "").replace("]", "").split("[")
            if len(key_parts) == 2:
                category, day = key_parts  # Extract "land" / "flight" and "day1" / "day2"
            else:
                continue  # Skip invalid keys

            # Ensure dictionary structure exists
            if category not in files:
                files[category] = {}
            if day not in files[category]:
                files[category][day] = []
            for file in file_list:
                files[category][day].append(file)

        db.session.commit()
        folder = email+'/'+sourceCity+'_to_'+destinationCity+'_'+str(trip.id)
        if landPackage!='false':
            for i in range(0,total):
                # print(files)
                if 'land' in files:
                    if 'day'+str(i+1) in files['land']:
                        # print('sdfs')
                        file_list = files['land']['day'+str(i+1)]
                        for file in file_list:

                            if file.filename == '':
                                return jsonify({"error": "No selected file"}), 400
                            upload_file(file,folder+'/land/day'+str(i+1))
        if flightPackage!='false':
            for i in range(0,total):
                if 'flight' in files:
                    if 'day'+str(i+1) in files['flight']:
                        # print('sdfs')
                        file_list = files['flight']['day'+str(i+1)]
                        # folder_name = request.form.get('folder', '')  # Default folder: "uploads"
                        for file in file_list:
                            if file.filename == '':
                                return jsonify({"error": "No selected file"}), 400
                            upload_file(file,folder++'/flight/day'+str(i+1))
        print(hotelPackage)
        if hotelPackage!='false':
            for i in range(0,total):
                if 'hotel' in files:
                    if 'day'+str(i+1) in files['hotel']:
                        # print('sdfs')
                        file_list = files['hotel']['day'+str(i+1)]
                        # folder_name = request.form.get('folder', '')  # Default folder: "uploads"
                        for file in file_list:
                            if file.filename == '':
                                return jsonify({"error": "No selected file"}), 400
                            upload_file(file,folder++'/hotel/day'+str(i+1))
        return jsonify({'data':''})
    