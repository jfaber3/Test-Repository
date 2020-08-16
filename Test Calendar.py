from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

'''
#Making credentials to sign in to a google account.  We only need to do this part the first time we sign in.
scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)  #download the .json file when setting up the api client
credentials = flow.run_console()
pickle.dump(credentials, open("token.pkl", "wb"))  #after signing in, save credentials like this so that you don't have to sign in manually every time.
'''

#This takes the primary calendar of the google account we have access to and extracts the events.
credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']  #takes the calendar ID for the account's primary calendar
Events = service.events().list(calendarId=calendar_id).execute()

#Here is a sample of some already-extracted events, use this for just playing around with calendar format.
#Sample_events = pickle.load(open("sample_events.pkl", "rb"))


#CREATING CALENDAR EVENT

#here is a test event
event = {
  'summary': 'Test Event',
  'location': 'Los Angeles',
  'description': 'Meeting to Talk about GRN TextBot',
  'start': {
    'dateTime': '2020-08-20T07:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2020-08-20T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=1'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId=calendar_id, body=event).execute()  #This creates the event.  We need the calendar ID from earlier


