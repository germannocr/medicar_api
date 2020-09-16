import datetime

from django.contrib import admin
from django import forms

# Register your models here.
from medicar_api.models import Especialidade, Medico, Agenda


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = '__all__'

    def clean_dia(self):
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
    form = AgendaForm
    list_display = ('medico', 'dia', 'horarios')


admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Agenda, AgendaAdmin)
