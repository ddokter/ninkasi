from django import forms
from ..models.batch import BatchTank
from django.forms import ModelForm


class DateTimeInput(forms.DateInput):

    input_type = 'datetime-local'


# class BatchTankForm(forms.ModelForm):
#    class Meta:
#        model = BatchTank
#        fields = ["start_date", "end_date"]
#        widgets = {
#            "date_from": DateTimeInput(),
#            "date_to": DateTimeInput(),
#        }
