import datetime

from django import forms
from django.contrib import admin

# Register your models here.
from medicar_api.models import (
    Especialidade,
    Medico,
    Agenda
)


class AgendaForm(forms.ModelForm):
    """
    Represents the form for creating Agenda's in the administrative interface.
    """
    class Meta:
        model = Agenda
        fields = '__all__'

    def clean_dia(self):
        """
        Validates the day field entered by the user, in relation to past days and agendas already existing on the same
        day.
        """
        today = datetime.date.today()
        given_date = self.cleaned_data.get('dia')
        given_medico = self.cleaned_data.get('medico')

        if given_date < today:
            raise forms.ValidationError("Incorrect Date")
        retrieved_agenda = Agenda.objects.filter(dia=given_date, medico=given_medico).first()

        if retrieved_agenda:
            raise forms.ValidationError("Already existent Agenda")
        return self.cleaned_data['dia']


class AgendaAdmin(admin.ModelAdmin):
    """
    Instantiate the form and the order in which the fields are presented.
    """
    form = AgendaForm
    list_display = ('medico', 'dia', 'horarios')


admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Agenda, AgendaAdmin)
