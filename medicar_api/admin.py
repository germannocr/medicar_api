from django.contrib import admin
from django import forms

# Register your models here.
from todo_list_api.models import Especialidade, Medico, Agenda

admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Agenda)
#
# class AgendaForm(forms.ModelForm):
#     class Meta:
#         model = Agenda
#
#     def clean_form(self):
#