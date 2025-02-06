from flask import Blueprint
from Server.config import DevConfig
from flask_restx import Api, Resource, fields
from Server.serializers import booking_model
from Server.models import *
from Server.exts import api

admin_blueprint = Blueprint('admin', __name__, url_prefix='/api')


@api.route('/bookings', methods=['GET'])
class resourceBookings(Resource):

    @api.marshal_list_with(booking_model)
    def get(self):
        """ To get all bookings """

        bookings_list = Booking.query.all()
        return bookings_list, 200



@api.route('/bookings/<int:id>', methods=['GET', 'PATCH', 'POST'])    
class bookingResource(Resource):

    @api.marshal_with(booking_model)
    def get(self, id):
        """ To get a booking by id """

        booking = Booking.query.get_or_404(id)
        return booking, 200


    @api.expect(booking_model)
    @api.marshal_with(booking_model)
    def patch(self, id):
        """ To update a booking by id partially"""

        updated_booking = Booking.query.get_or_404(id)
        data = api.payload
        
        for key, value in data.items():
            if hasattr(updated_booking, key):
                setattr(updated_booking, key, value)

        updated_booking.update(**data)

        return updated_booking, 200


    def delete(self, id):
        """ To delete a booking by id """

        booking = Booking.query.get_or_404(id)
        booking.delete()
        return booking, 204









