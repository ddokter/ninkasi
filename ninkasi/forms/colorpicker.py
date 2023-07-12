from django import forms


class ColorInput(forms.TextInput):

    """ Use modern html5 color widget """

    input_type = 'color'
