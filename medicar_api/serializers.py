from rest_framework import serializers
from todo_list_api.models import (
    Especialidade
)


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = '__all__'
