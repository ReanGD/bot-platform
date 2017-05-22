import datetime
import bots.bot_telegram as tbot
import google.calendar as gcal


class Run(object):
    def __init__(self):
        self.cal = gcal.GoogleCalendar()
        self.bot = tbot.Bot()

        # start_data_time = datetime.datetime(2017, 8, 14, hour=0, minute=30)
        # cal.add_single_event('Событие1', '', start_data_time)
        # cal.get_events()

    def handler(self, msg):
        return msg

    def create(self):
        self.cal.create()
        self.bot.create(self.handler)

        return self

    def run(self):
        self.bot.run()


if __name__ == '__main__':
    Run().create().run()
