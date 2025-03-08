# import json
# from datetime import datetime, timedelta
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from decouple import config
# import uuid

# SCOPES = ["https://www.googleapis.com/auth/calendar"]
# service_account_file = config("SERVICE_ACCOUNT_FILE")
# calendar_id = config('CALENDAR_ID')

# def get_calendar_service():
#     credentials = service_account.Credentials.from_service_account_file(
#         service_account_file, scopes=SCOPES
#     )
#     return build("calendar", "v3", credentials=credentials)

# def create_calendar_event(fullname, date, time, timezone, services, description):
#     """Creates a Google Calendar event."""
#     service = get_calendar_service()

#     if isinstance(time, str):
        
#         time = datetime.strptime(time, "%H:%M:%S").time()  # Convert to time object

#         event_start = datetime.combine(date, time)  # Create full datetime object
#         event_end = event_start + timedelta(minutes=30)  # Add 30 minutes
        
#         # Back to Google Calendar format
#         event_start = event_start.strftime("%Y-%m-%dT%H:%M:%S")
#         event_end = event_end.strftime("%Y-%m-%dT%H:%M:%S")
    

#     event = {
#         "summary": f"Booking with {fullname}",
#         "description": f"Services: {services}\n\n{description}",
#         "start": {
#             "dateTime": event_start,
#             "timeZone": timezone
#         },
#         "end": {
#             "dateTime": event_end,
#             "timeZone": timezone
#         },
        
#         "reminders": {
#             "useDefault": False,
#             "overrides": [
#                 {"method": "email", "minutes": 30},
#                 {"method": "popup", "minutes": 10}
#             ]
#         },
#         "conferenceData": {
#         "createRequest": {
#             "requestId": str(uuid.uuid4()),
#             "conferenceSolutionKey": {"type":"hangoutsMeet"}
#         }
#     }
#     }

#     event = service.events().insert(calendarId=calendar_id, body=event, conferenceDataVersion=1).execute()
#     return event.get("hangoutLink", "")
