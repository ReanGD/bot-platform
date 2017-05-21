import datetime
import google.calendar as gcal

def main():
    cal = gcal.GoogleCalendar()
    cal.create()

    start_data_time = datetime.datetime(2017, 8, 14, hour=0, minute=30)
    cal.add_single_event('Событие1', '', start_data_time)
    cal.get_events()


if __name__ == '__main__':
    main()
