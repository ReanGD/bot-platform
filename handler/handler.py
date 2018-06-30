import pytz
import datetime
import dateutil.parser


class Handler(object):
    def __init__(self):
        self._config = {}

    def create(self, config):
        self._config = config

    def _work_breakfast(self, parameters, time_zone):
        date = parameters['date']
        if date != '':
            weekday = dateutil.parser.parse(parameters['date']).weekday()
        else:
            weekday = datetime.datetime.now(pytz.timezone(time_zone)).weekday()

        if weekday in [5, 6]:
            weekday = 5
        return self._config['work.breakfast'][weekday]

    def handle(self, intent_name, parameters, time_zone):
        if intent_name == 'calendar.events':
            return 'calendar.events'
        elif intent_name == 'work.breakfast':
            return self._work_breakfast(parameters, time_zone)
        else:
            return 'Unknown intent_name: {}'.format(intent_name)