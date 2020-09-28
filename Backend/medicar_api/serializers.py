from rest_framework import serializers
from medicar_api.models import (
    Especialidade, Medico, Consulta, Agenda
)


class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = '__all__'


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer(many=False, read_only=True)

    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'email', 'telefone', 'especialidade']


class ConsultaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(many=False, read_only=True)

    class Meta:
        model = Consulta
        fields = ['id', 'dia', 'horario', 'data_agendamento', 'medico']


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(many=False, read_only=True)
    horarios = serializers.ListField(child=serializers.TimeField(format='%H:%M'))

    class Meta:
        model = Agenda
        fields = '__all__'
