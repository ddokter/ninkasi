from django import forms


class DateTimeInput(forms.DateTimeInput):

    """ Use modern html5 datetime widget """

    input_type = 'datetime-local'

    def format_value(self, value):

        """ Format python value to proper string for widget """

        if value:

            try:
                return value.strftime("%Y-%m-%dT%H:%M")
            except AttributeError:
                pass

        return value
