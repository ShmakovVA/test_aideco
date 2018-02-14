from django import forms

from airport import models


class FormFilterFlights(forms.Form):
    city_name = forms.CharField(max_length=100, label=u'City', required=False)
    flight_name = forms.CharField(max_length=25, label=u'Flight', required=False)
    status_name = forms.ModelChoiceField(models.Status.objects.all(), label=u'Status', required=False, empty_label='any')

