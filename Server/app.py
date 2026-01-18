from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from Server.config import DevConfig
from decouple import config
from flask_restx import Resource, fields, Namespace
from Server.models import *
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Server.exts import db, api, migrate
from flask_mail import Mail, Message
from Server.send_email import send_mail, reschedule_mail, cancel_mail
from Server.calendar_event import create_event
from datetime import datetime, timedelta
from Server.admin import admin_blueprint
from Server.serializers import booking_model
from datetime import datetime, timezone
import pytz



app = Flask(__name__)


app.config.from_object(DevConfig)
# api.init_app(app, version='1.0', title='SifaFX APIs', contact='support@sifafx.com')
CORS(app)
db.init_app(app)
migrate.init_app(app, db)
mail = Mail(app)

app.register_blueprint(admin_blueprint, url_prefix='/admin')

admin_email = config('ADMIN_EMAIL')


def convert_to_12_hour(time_24):

    # time_obj = datetime.strptime(time_24, "%H:%M:%S")
    time_12 = time_24.strftime("%I:%M %p").lstrip("0")

    return time_12

def format_date(date_str):
      
    formatted_date = date_str.strftime("%B %d, %Y")

    return formatted_date

def format_to_gmt(date_time_str):
    
    # Convert input string to datetime object
    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

    # Convert to UTC time
    date_time_obj_utc = date_time_obj.datetime(timezone.utc())

    # Format as yyyyMMdd'T'HHmmss'Z'
    formatted_gmt = date_time_obj_utc.strftime("%Y%m%dT%H%M%SZ")
    
    return formatted_gmt


@app.route('/bookings/<int:id>', methods=['GET'])
def getdata(id):
    
    booking = Booking.query.get_or_404(id)
    
    if booking.status =='Cancelled':
        return 404

    return jsonify({
        "id": booking.id,
        "fullname": booking.fullname,
        "email": booking.email,
        "phone": booking.phone,
        "date": booking.date.strftime('%Y-%m-%d'),
        "time": str(booking.time),
        "timezone": booking.timezone,
        "services": booking.services,  # Ensure it's a list
        "description": booking.description,
        "status": booking.status.value,  # If status is an Enum, use .value
        "created_at": booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }), 200



@app.route('/Booking', methods=['POST'])
def post():

    """ To create a new booking """
    
    data = request.get_json()
    fullname=data['fullname']
    email=data['email']
    timezone = data['timezone']
    services =data['services']['services'] if isinstance(data['services'], dict) else data['services']
    
    phone=data['phone']
    description=data['description']
    time = data['time']
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    
    
    print(time, date, services)
# Ensure services is a list
    
    print(f"Received services: {services} | Type: {type(services)}")


    new_booking = Booking(
        fullname=fullname,
        email=email,
        phone=phone,
        date=date,
        time=time,
        timezone=timezone,
        services=services,
        description=description,
        
    )
    new_booking.save()
    new_id = new_booking.id
    print(new_id)
    time_12 = convert_to_12_hour(new_booking.time)
    formatted_date = format_date(date)
    
    
    
    local_tmz = pytz.timezone(timezone)
    
    starttime_str = datetime.strftime(date, "%Y-%m-%d") + 'T' + time
    starttime_obj = local_tmz.localize(datetime.strptime(starttime_str, "%Y-%m-%dT%H:%M:%S"))
    start = datetime.strftime(starttime_obj, "%Y-%m-%dT%H:%M:%S%z")

    endtime_obj = starttime_obj + timedelta(minutes=30)
    end = datetime.strftime(endtime_obj, '%Y-%m-%dT%H:%M:%S%z')
    
    print(admin_email, start, end, local_tmz)


    send_mail(fullname,email,formatted_date,time_12,new_id)
    calendar_details = create_event(fullname,start, end, email, services, admin_email)
    meet_link = calendar_details.get('meet_link')

    new_booking.meet_link = meet_link
    new_booking.save()

    print(new_booking)

    return jsonify({
            "id": new_booking.id,
            "fullname": new_booking.fullname,
            "email": new_booking.email,
            "phone": new_booking.phone,
            "date": new_booking.date.strftime('%Y-%m-%d'),
            "time": str(new_booking.time),
            "timezone": new_booking.timezone,
            "services": new_booking.services,
            "description": new_booking.description,
            "meet_link":new_booking.meet_link
            
        }), 201


        


@app.route('/Reschedule/<int:id>', methods=['PATCH'])
def patch(id):
        """ To update a booking by id partially"""

        updated_booking = Booking.query.get_or_404(id)

        if updated_booking.status == 'Cancelled':
            return jsonify({"message": "This appointment was cancelled. Please create a new appointment"}), 404

        else:

            data = request.get_json()
            print(data)
            
            for key, value in data.items():
                if hasattr(updated_booking, key):
                    setattr(updated_booking, key, value)

            updated_booking.update(**data)
            
            email = updated_booking.email
            fullname= updated_booking.fullname
            new_time = convert_to_12_hour(updated_booking.time)
            new_date = format_date(updated_booking.date)
            
            reschedule_mail(fullname, email, new_date, new_time, id)
        

        return jsonify({
            
            "id": updated_booking.id,
            "fullname": updated_booking.fullname,
            "email": updated_booking.email,
            "phone": updated_booking.phone,
            "date": updated_booking.date.strftime('%Y-%m-%d'),
            "time": str(updated_booking.time),
            "timezone": updated_booking.timezone,
            "services": updated_booking.services,
            "description": updated_booking.description

        }), 200



@app.route('/Cancel/<int:id>', methods=['PUT'])
def put(id):
        """ Update the booking to cancelled """

        data = request.get_json()
        id = id
        booking_to_update = Booking.query.get_or_404(id)

       
        if not booking_to_update:
            return 404
        
       
        booking_to_update.status = 'Cancelled'
        booking_to_update.update()
                        
        email = booking_to_update.email
        new_time = convert_to_12_hour(booking_to_update.time)
        new_date = format_date(booking_to_update.date)
        cancel_mail(email, new_date, new_time)


        return jsonify({
            'message': f'The Appoinment is by {booking_to_update.email}'
        }), 200


@app.route('/', methods=['GET'])
def index():
    
    return render_template('Homepage.html')

@app.route('/Homepage', methods=['GET'])
def home():
    
    return render_template('Homepage.html')



@app.route('/Services/Api_Integration', methods=['GET'])
def apiint():
    
    return render_template('API-Integration.html')


@app.route('/Booking', methods=['GET'])
def booking():
    
    return render_template('Booking.html')

@app.route('/Cancel/<int:id>', methods=['GET'])
def cancel(id):

    booked_id = Booking.query.get_or_404(id)
    print("The booking is:" ,booked_id.status)

    if booked_id.status == 'Status.Cancelled':
        return 404
        
    
    return render_template('Cancel.html', booking_id=booked_id)

@app.route('/HowWeWork', methods=['GET'])
def howwework():
    
    return render_template('HowWeWork.html')

@app.route('/Services/MachineLearningEnhancement', methods=['GET'])
def ml():
    
    return render_template('MachineLearningEnhancement.html')

@app.route('/Services/MarketDataAnalysisTools', methods=['GET'])
def mdat():
    
    return render_template('MarketDataAnalysisTools.html')

@app.route('/Services/Multi-Platform_Development', methods=['GET'])
def mpd():
    
    return render_template('Multiplatform-Development.html')

@app.route('/Reschedule/<int:id>', methods=['GET'])
def reschedule(id):
    """ Renders the Reschedule page """
    
    booked_id = Booking.query.get_or_404(id)
    
    return render_template('Reschedule.html', booking_id=booked_id)


@app.route('/Services/RiskManagement', methods=['POST', 'GET'])
def riskm():
    
    return render_template('RiskManagement.html')


@app.route('/Services', methods=['GET'])
def services():
    
    return render_template('services.html')

@app.route('/Services/StrategyAutomation', methods=['GET'])
def strategy():
    
    return render_template('StrategyAutomation.html')

@app.route('/Services/TechnicalSupport', methods=['GET'])
def techSupport():
    
    return render_template('TechnicalSupport.html')

@app.route('/Services/TestingAndOptimization', methods=['GET'])
def testing():
    
    return render_template('Testing&Optimization.html')


@app.route('/callback', methods=['POST', 'GET'])
def callback():
    
    return 'Callback'



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Database created or already exists')
        app.run(debug=True)
        
