import google.calendar as gcal


def main():
    cal = gcal.GoogleCalendar()
    cal.create()
    cal.get_events()


if __name__ == '__main__':
    main()
