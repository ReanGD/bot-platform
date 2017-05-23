import locale
import datetime
import bots.bot_telegram as tbot
import google.calendar as gcal


class Run(object):
    def __init__(self):
        self.cal = gcal.GoogleCalendar()
        self.bot = tbot.Bot()

        # start_data_time = datetime.datetime(2017, 8, 14, hour=0, minute=30)
        # cal.add_single_event('Событие1', '', start_data_time)

    def handler(self, msg):
        events = [it[0].strftime("%d %B %H:%M") + ': ' + it[1] for it in self.cal.get_events(10)]
        return '/n'.join(events)

    def create(self):
        locale.setlocale(locale.LC_ALL, ('RU', 'UTF8'))
        self.cal.create()
        self.bot.create(self.handler)

        return self

    def run(self):
        self.bot.run()


if __name__ == '__main__':
    Run().create().run()
