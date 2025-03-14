import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
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

    event = {
    'summary': 'Safaricom Decode 2025',
    'location': 'Nairobi',
    'description': 'A chance to hear more about Safaricom\'s developer products.',
    'start': {
        'dateTime': '2025-03-14T08:00:00+03:00',
        'timeZone': 'Africa/Nairobi',
    },
    'end': {
        'dateTime': '2025-03-14T09:30:00+03:00',
        'timeZone': 'Africa/Nairobi',
    },
     'attendees': [
    {'email': 'admiralkrhemaz@gmail.com'},
    {'email': 'rhematesh@gmail.com'},
  ],
   'conferenceData': {
            'createRequest': {
                'requestId': 'testing123',  # This should be unique for each request
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 12},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    print('Event created: %s' % (event.get('htmlLink')))

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()