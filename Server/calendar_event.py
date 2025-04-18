import datetime
import os.path
import secrets


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]



def create_event(fullname, start, end, email,services,admin_email):
  
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    request_id = secrets.token_urlsafe(8)

    for service in services:
       myServices = service

    event = {
    'summary': f"Test Meeting with {fullname}",
    'location': 'Nairobi, Kenya',
    'description': f"A meeting to discuss the following:\n{services}\n\n ",
    'start': {
        'dateTime': f'{start}',
        
    },
    'end': {
        'dateTime': f'{end}',
        
    },
     'attendees': [
    {'email': f"{email}"},
    {'email': f"{admin_email}"},

  ],
   'conferenceData': {
            'createRequest': {
                'requestId': f"{request_id}",  # This should be unique for each request
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    'sendUpdates':'all',
    'guestsCanSeeOtherGuests': False
    }

    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    
    print('Event created: %s' % (event.get('hangoutLink')))

    meet_link = event.get('hangoutLink')
    
    return_data = {
      'Event_data': event,
      'meet_link': f"{meet_link}",
    }

    return return_data
  
  except HttpError as error:
    print(f"An error occurred: {error}")



def update_event(event_id, new_start, new_end, new_timezone):
    """Update an existing event's start, end, and timezone."""
    creds = None
    # Check if token.json exists and load credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If credentials are not valid, re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        event['start'] = {
            'dateTime': new_start,
            'timeZone': new_timezone
        }
        event['end'] = {
            'dateTime': new_end,
            'timeZone': new_timezone
        }

        updated_event = service.events().update(
            calendarId='primary', 
            eventId=event_id, 
            body=event
        ).execute()

        print('Event updated: %s' % (updated_event.get('hangoutLink')))
        return updated_event

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def cancel_event(event_id):
    """Cancel or delete an event."""
    creds = None
    # Check if token.json exists and load credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If credentials are not valid, re-authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        
        # Delete the event using event ID
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event with ID {event_id} has been deleted.")

    except HttpError as error:
        print(f"An error occurred: {error}")
