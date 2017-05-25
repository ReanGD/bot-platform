import locale
from parser.parser_apiai import Parser
from bots.bot_telegram import Bot
from google.calendar import GoogleCalendar


class Run(object):
    def __init__(self):
        self.cal = GoogleCalendar()
        self.bot = Bot()
        self.parser = Parser()

        # start_data_time = datetime.datetime(2017, 8, 14, hour=0, minute=30)
        # cal.add_single_event('Событие1', '', start_data_time)

    def get_events(self):
        events = [it[0].strftime("%d %B %H:%M") + ': ' + it[1] for it in self.cal.get_events(10)]
        return '/n'.join(events)

    def handler(self, text):
        result = self.parser.parse(text)
        if result.success():
            return result.intent_name
        else:
            return result.error_msg

    def create(self):
        locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
        self.cal.create()
        self.bot.create(self.handler)
        self.parser.create('ru')

        return self

    def run(self):
        self.bot.run()


if __name__ == '__main__':
    Run().create().run()
