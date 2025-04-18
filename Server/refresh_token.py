import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def refresh_token():
    """Refresh the access token using the refresh token."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/calendar"])

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save the refreshed credentials back to token.json
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        print("Token refreshed successfully.")
    else:
        print("No valid credentials available. Please reauthenticate.")
    
if __name__ == "__main__":
    refresh_token()
