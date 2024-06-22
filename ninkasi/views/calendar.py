from datetime import datetime, date
import calendar


class Calendar:

    """ Mixin for calendar function, like 'month' """

    @property
    def month(self):

        """Return current month data, for displaying of the month
        calendar

        """

        if self.request.GET.get('go', None):

            year, month = self.request.GET['go'].split('-')

            now = date(int(year), int(month), 1)
        else:
            now = datetime.now()

        if now.month == 12:
            _next = date(now.year + 1, 1, 1)
        else:
            _next = date(now.year, now.month + 1, 1)

        if now.month == 1:
            _prev = date(now.year - 1, 12, 1)
        else:
            _prev = date(now.year, now.month - 1, 1)

        cal = calendar.Calendar()

        days = list(cal.itermonthdates(now.year, now.month))

        weeks = []
        week = []

        for idx, val in enumerate(days):
            week.append(val)

            if (idx + 1) % 7 == 0:
                weeks.append(week)
                week = []

        return {
            'title': now.strftime("%B %Y"),
            'days': days,
            'today': now,
            'weeks': weeks,
            'next': _next.strftime("%Y-%m"),
            'prev': _prev.strftime("%Y-%m"),
            'month': now.month,
            'year': now.year
            }
