from django import forms

from airport import models


class FormFilterFlights(forms.Form):
    city_name = forms.CharField(max_length=100, label=u'Город', required=False)
    flight_name = forms.CharField(max_length=25, label=u'Рейс', required=False)
    status_name = forms.ModelChoiceField(models.Status.objects.all(), label=u'Статус', required=False,
                                         empty_label='Любой')
