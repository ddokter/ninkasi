from django import forms
from ..models.batch import BatchTank
from django.forms import ModelForm


class DateTimeInput(forms.DateInput):
    
    input_type = 'datetime-local'

    def format_value(self, value):

        if value:
        
            return value.strftime("%Y-%m-%dT%H:%M")

        else:

            return value

# class BatchTankForm(forms.ModelForm):
#    class Meta:
#        model = BatchTank
#        fields = ["start_date", "end_date"]
#        widgets = {
#            "date_from": DateTimeInput(),
#            "date_to": DateTimeInput(),
#        }
