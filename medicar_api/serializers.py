from rest_framework import serializers
from medicar_api.models import (
    Especialidade, Medico
)


class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = '__all__'


class MedicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medico
        fields = '__all__'
