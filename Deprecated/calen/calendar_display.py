import calendar
import datetime

class CalendarDisplay:
    def __init__(self):
        self.events = {}

    def get_calendar(self):
        # Get current year and month
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        # Generate a text calendar for the current month
        cal = calendar.TextCalendar(calendar.SUNDAY)
        calendar_str = cal.formatmonth(year, month)
        return calendar_str

    def highlight_dates(self, dates):
        # Code to highlight specific dates based on events
        for date in dates:
            self.events[date] = True  # Mark the date as highlighted
        pass