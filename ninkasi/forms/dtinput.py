from django import forms


class DateTimeInput(forms.DateInput):

    """ Use modern html5 datetime widget """

    input_type = 'datetime-local'

    def format_value(self, value):

        """ Format python value to proper string for widget """

        if value:

            return value.strftime("%Y-%m-%dT%H:%M")

        return value
