import os
import json
import locale
from bots.bot_telegram import Bot
from handler.handler import Handler
from parser.parser_apiai import Parser
from google.calendar import GoogleCalendar


class Run(object):
    def __init__(self):
        self.cal = GoogleCalendar()
        self.bot = Bot()
        self.parser = Parser()
        self.handler = Handler()
        self.time_zone = 'Europe/Moscow'

        # start_data_time = datetime.datetime(2017, 8, 14, hour=0, minute=30)
        # cal.add_single_event('Событие1', '', start_data_time)

    def get_events(self):
        events = [it[0].strftime("%d %B %H:%M") + ': ' + it[1] for it in self.cal.get_events(10)]
        return '/n'.join(events)

    def text_handler(self, text):
        error, result = self.parser.parse(text, self.time_zone)
        if error == '':
            return self.handler.handle(result.intent_name, result.parameters, self.time_zone)
        else:
            return error

    def create(self):
        locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))

        cred_dir = os.path.join(os.path.expanduser('~'), '.config', 'credentials')
        if not os.path.exists(cred_dir):
            os.makedirs(cred_dir)
        config_file = os.path.join(cred_dir, 'bot.json')
        config = json.load(open(config_file, 'r'))

        self.cal.create()
        self.bot.create(config['telegram'], self.text_handler)
        self.parser.create(config['apiai'])
        self.handler.create(config['handler'])

        return self

    def run(self):
        self.bot.run()


if __name__ == '__main__':
    Run().create().run()
