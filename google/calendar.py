import os
import pytz
import httplib2
import datetime
import argparse
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleCalendar(object):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    APPLICATION_NAME = 'Google Calendar API For Bot'

    def __init__(self):
        cred_dir = os.path.join(os.path.expanduser('~'), '.config', 'credentials')
        if not os.path.exists(cred_dir):
            os.makedirs(cred_dir)

        self._client_secret_file = os.path.join(cred_dir, 'google-client-secret.json')
        self._credential_file = os.path.join(cred_dir, 'goole-credential.json')
        self._service = None
        self._time_zone = pytz.timezone('Europe/Moscow')

    def _get_credentials(self):
        store = Storage(self._credential_file)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self._client_secret_file, GoogleCalendar.SCOPES)
            flow.user_agent = GoogleCalendar.APPLICATION_NAME
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + self._credential_file)
        return credentials

    def _get_primary_calendar_timezone(self):
        calendar = self._service.calendars().get(calendarId='primary').execute()
        return pytz.timezone(calendar['timeZone'])

    def create(self):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        self._service = discovery.build('calendar', 'v3', http=http)
        self._time_zone = self._get_primary_calendar_timezone()

    def add_single_event(self, summary, description, start_data_time):
        start_data_time_str = self._time_zone.localize(start_data_time).isoformat()
        time_zone = self._time_zone.zone

        event = {
            'summary': summary,
            'location': '',
            'description': description,
            'start': {
                'dateTime': start_data_time_str,
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': start_data_time_str,
                'timeZone': time_zone,
            },
        }

        self._service.events().insert(calendarId='primary', body=event).execute()

    def get_events(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self._service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
