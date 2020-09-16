
from rest_framework.serializers import ModelSerializer

from django.http import JsonResponse
from rest_framework import status
from medicar_api.serializers import (
    EspecialidadeSerializer, MedicoSerializer
)


def map_delete_response():
    return JsonResponse(
        None,
        safe=False,
        status=status.HTTP_204_NO_CONTENT
    )


def map_get_especialidade_response(serialized_response: EspecialidadeSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_medico_response(serialized_response: MedicoSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_update_response():
    return JsonResponse(
        None,
        safe=False,
        status=status.HTTP_204_NO_CONTENT
    )


def map_post_card_response(serialized_response: ModelSerializer):
    """
    Returns a response in JSON format with the fields present in the Especialidade model.

    #Parameters:
        serialized_response (ModelSerializer): Serializer created from the Especialidade model

    #Returns:
        (JsonResponse): Dictionary in JSON format with the data of a created object of type Especialidade.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )
