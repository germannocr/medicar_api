import datetime

from rest_framework import status
from rest_framework.serializers import ModelSerializer

from django.http import (
    JsonResponse,
    QueryDict
)
from medicar_api.serializers import (
    EspecialidadeSerializer,
    MedicoSerializer,
    ConsultaSerializer,
    AgendaSerializer
)


def map_get_especialidade_response(serialized_response: EspecialidadeSerializer):
    """
    Maps the response to the search for existing Especialidade's.

    #Parameters:
        serialized_response (EspecialidadeSerializer): EspecialidadeSerializer type object that represents the objects
        searched in the database in dictionary form (key: value).

    #Returns:
        JsonResponse: Object of type JsonResponse with a dictionary containing the search response and an HTTP code
         related to the result of the request.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_delete_response():
    """
    Maps the response to the search for existing specialties.

    #Returns:
        JsonResponse [NO-CONTENT]: Object of type JsonResponse with an HTTP code related to the result of the request.
    """
    return JsonResponse(
        {},
        safe=False,
        status=status.HTTP_204_NO_CONTENT
    )


def map_get_medico_response(serialized_response: MedicoSerializer):
    """
    Maps the response to the search for existing Medico's.

    #Parameters:
        serialized_response (MedicoSerializer): MedicoSerializer type object that represents the objects
        searched in the database in dictionary form (key: value).

    #Returns:
        JsonResponse: Object of type JsonResponse with a dictionary containing the search response and an HTTP code
        related to the result of the request.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_agenda_response(serialized_response: AgendaSerializer):
    """
    Maps the response to the search for existing Agenda's.

    #Parameters:
        serialized_response (AgendaSerializer): AgendaSerializer type object that represents the objects
        searched in the database in dictionary form (key: value).

    #Returns:
        JsonResponse: Object of type JsonResponse with a dictionary containing the search response and an HTTP code
        related to the result of the request.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_consulta_response(serialized_response: ConsultaSerializer):
    """
    Maps the response to the search for existing Consulta's.

    #Parameters:
        serialized_response (ConsultaSerializer): ConsultaSerializer type object that represents the objects
        searched in the database in dictionary form (key: value).

    #Returns:
        JsonResponse: Object of type JsonResponse with a dictionary containing the search response and an HTTP code
        related to the result of the request.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_post_consulta_response(serialized_response: ModelSerializer):
    """
    Maps the response for Consulta's creation.

    #Parameters:
        serialized_response (ModelSerializer): ModelSerializer type object that represents the objects created in the
        database in dictionary form (key: value).

    #Returns:
        JsonResponse: Object of type JsonResponse with a dictionary containing the creation response and an HTTP code
        related to the result of the request.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_agenda_query_params(query_params: QueryDict):
    """
    Maps the passed query params to search filters for objects of type Agenda.

    #Parameters:
        query_params (QueryDict): Query parameters dictionaries, generated from the parameters and values
        passed in the request url.

    #Returns:
        filters_dict (Dict): Dictionary with mapped search filters, created from given parameters and values.
    """
    query_params_dict = query_params.copy()
    filters_dict = {}

    medico_ids_list = query_params_dict.pop('medico', None)
    if medico_ids_list:
        filters_dict['medico__id__in'] = medico_ids_list

    especialidade_ids_list = query_params_dict.pop('especialidade', None)
    if especialidade_ids_list:
        filters_dict['medico__especialidade__id__in'] = especialidade_ids_list

    initial_date = query_params.get('data_inicio', None)

    final_date = query_params.get('data_final', None)

    if initial_date and final_date:
        filters_dict['dia__range'] = [initial_date, final_date]

    return filters_dict


def retrieve_current_date_and_time():
    """
    Returns the current time and day, in Time and Date formats respectively.

    #Returns:
        current_date (Date): Current time, in datetime Time format.
        current_time (Time): Current date, in datetime date format.
    """
    current_date = datetime.date.today()
    current_time = datetime.time(hour=datetime.datetime.utcnow().hour, minute=datetime.datetime.utcnow().minute)

    return current_date, current_time


def remove_invalid_horario_from_list(
        retrieved_agendas_list: list,
        existent_consultas_list: list,
        current_time: datetime.time,
        current_date: datetime.date,
        user_id: int
):
    """
    Removes times considered invalid for listing Agenda's, such as past times and days, as well as times already filled.

    #Parameters:
        retrieved_agendas_list (list): List of existing Agenda type objects.
        existent_consultas_list (list): List of existing Consulta type objects.
        current_time (Time): Current time, in Time format.
        current_date (Date): Current date, in Date format.
        user_id (int): Unique identifier of the user responsible for the request.

    #Returns:
        filtered_agenda_list (list): List of objects of type Agenda, mapped only with the available and future times.
    """
    filtered_agenda_list = []
    for current_agenda in retrieved_agendas_list:
        horario_list = []
        for current_consulta in existent_consultas_list:
            # Removes doctors' schedules already filled by other customers.
            if current_consulta.horario in current_agenda.horarios \
                    and current_consulta.dia == current_agenda.dia \
                    and current_consulta.medico == current_agenda.medico:
                current_agenda.horarios.remove(current_consulta.horario)

            # Removes customer hours already filled by other Consultas.
            if current_consulta.horario in current_agenda.horarios \
                    and current_consulta.dia == current_agenda.dia \
                    and current_consulta.created_by_user == user_id:
                current_agenda.horarios.remove(current_consulta.horario)

        # Removes past times.
        if current_date == current_agenda.dia:
            for current_horario in current_agenda.horarios:
                if current_horario > current_time:
                    horario_list.append(current_horario)
            current_agenda.horarios = horario_list

            # If all times on an Agenda are already filled, the Agenda is not listed.
            if len(horario_list) == 0:
                retrieved_agendas_list = retrieved_agendas_list.exclude(id=current_agenda.id)
            else:
                filtered_agenda_list.append(current_agenda)
        elif len(current_agenda.horarios) > 0:
            # If all times on an Agenda are already filled, the Agenda is not listed.
            filtered_agenda_list.append(current_agenda)

    return filtered_agenda_list
