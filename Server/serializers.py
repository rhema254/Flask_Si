from flask_restx import fields
from Server.exts import api

#serializer_model:
booking_model = api.model(
        'Booking',
        {
            "id": fields.Integer(required=True, description="Id"),
            "fullname": fields.String(required=True, description="Full Name"),
            "email": fields.String(required=True, description="Booker's Email"), 
            "phone": fields.String(required=False, description="Phone Number"),
            "date": fields.Date(required=True, description="Session Date"),
            "time": fields.String(required=True, description="Session Time in Format: HH:MM"),
            "timezone":fields.String(required=True, description="Timezone"),
            "status":fields.String(required=True, default='Scheduled', description="Booking Status"),
            "services": fields.String(fields.String,required=True, description="Service Required"),
            "meet_link": fields.String(nullable=True, default = 'none'),
            "description": fields.String(max_length=200, required=True, description="Description of the problem"),
            "created_at": fields.DateTime(required=True, description="Booking Creation Date")

        }
)
