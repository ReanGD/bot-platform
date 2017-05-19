import os
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

    def create(self):
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        self._service = discovery.build('calendar', 'v3', http=http)

    def get_events(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = self._service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])