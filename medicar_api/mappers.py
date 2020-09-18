import datetime

from rest_framework.serializers import ModelSerializer

from django.http import JsonResponse
from rest_framework import status
from medicar_api.serializers import (
    EspecialidadeSerializer, MedicoSerializer, ConsultaSerializer, AgendaSerializer
)


def map_get_especialidade_response(serialized_response: EspecialidadeSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_delete_response():
    return JsonResponse(
        {},
        safe=False,
        status=status.HTTP_204_NO_CONTENT
    )


def map_get_medico_response(serialized_response: MedicoSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_agenda_response(serialized_response: AgendaSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_consulta_response(serialized_response: ConsultaSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_post_consulta_response(serialized_response: ModelSerializer):
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


def map_agenda_query_params(query_params: dict):
    filters_dict = {}

    medico_ids_list = query_params.get('medico', None)
    if medico_ids_list:
        filters_dict['medico__id__in']: medico_ids_list

    especialidade_ids_list = query_params.get('especialidade', None)
    if especialidade_ids_list:
        filters_dict['medico__especialidade__id__in']: especialidade_ids_list

    initial_date = query_params.get('data_inicio', None)

    final_date = query_params.get('data_final', None)

    if initial_date and final_date:
        filters_dict['dia__range']: [initial_date, final_date]

    return filters_dict


def retrieve_current_date_and_time():
    current_date = datetime.date.today()
    current_time = datetime.time(hour=datetime.datetime.utcnow().hour, minute=datetime.datetime.utcnow().minute)

    return current_date, current_time
