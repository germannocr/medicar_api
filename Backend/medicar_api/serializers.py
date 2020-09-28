from rest_framework import serializers
from medicar_api.models import (
    Especialidade,
    Medico,
    Consulta,
    Agenda
)


class EspecialidadeSerializer(serializers.ModelSerializer):
    """
    Especialidade Serializer responsible for mapping existing Especialidade objects to dictionaries,
    making it possible to map responses.
    """

    class Meta:
        model = Especialidade
        fields = '__all__'


class MedicoSerializer(serializers.ModelSerializer):
    """
    Medico Serializer responsible for mapping existing Medico objects to dictionaries,
    making it possible to map responses.
    """
    especialidade = EspecialidadeSerializer(many=False, read_only=True)

    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'email', 'telefone', 'especialidade']


class ConsultaSerializer(serializers.ModelSerializer):
    """
    Consulta Serializer responsible for mapping existing Consulta objects to dictionaries,
    making it possible to map responses.
    """
    medico = MedicoSerializer(many=False, read_only=True)

    class Meta:
        model = Consulta
        fields = ['id', 'dia', 'horario', 'data_agendamento', 'medico']


class AgendaSerializer(serializers.ModelSerializer):
    """
    Agenda Serializer responsible for mapping existing Agenda objects to dictionaries,
    making it possible to map responses.
    """
    medico = MedicoSerializer(many=False, read_only=True)
    horarios = serializers.ListField(child=serializers.TimeField(format='%H:%M'))

    class Meta:
        model = Agenda
        fields = '__all__'
