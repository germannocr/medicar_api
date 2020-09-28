from datetime import datetime

from django.db.models import Q
from django.http import QueryDict

from medicar_api.exceptions import (
    MissingRequiredFields,
    InvalidFieldType,
    InvalidFieldValue, IncorrectQueryParams, AlreadyExistentConsulta,
)
from medicar_api.mappers import retrieve_current_date_and_time
from medicar_api.models import Agenda, Consulta


def validate_consulta_post_body(request_body: dict):
    """
    Validates the JSON dictionary sent by the user when creating an Especialidade.

    #Parameters:
        request_body (dict): Dictionary in JSON format sent by the user with the fields to create an Especialidade.

    #Returns:
    """
    agenda_id = request_body.get('agenda_id')
    horario = request_body.get('horario')
    required_fields = [
        'agenda_id',
        'horario'
    ]

    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields(code=400)

    if not isinstance(agenda_id, int):
        raise InvalidFieldType(code=400)

    if not isinstance(horario, str):
        raise InvalidFieldType(code=400)

    current_date, current_time = retrieve_current_date_and_time()

    retrieved_agenda = Agenda.objects.filter(id=agenda_id, dia__gte=current_date).first()

    if retrieved_agenda:
        horario = datetime.strptime(horario, '%H:%M').time()

        if horario < current_time:
            raise InvalidFieldValue(code=400)

        if horario not in retrieved_agenda.horarios:
            raise InvalidFieldValue(code=400)

    else:
        raise InvalidFieldValue(code=400)

    return retrieved_agenda


def validate_already_existent_consulta(request_body: dict, retrieved_agenda: Agenda, user_id: int):
    retrieved_consulta = Consulta.objects.filter(
        Q(horario=request_body.get('horario'),
          dia=retrieved_agenda.dia,
          medico=retrieved_agenda.medico) |
        Q(horario=request_body.get('horario'),
          dia=retrieved_agenda.dia,
          created_by_user=user_id)
    ).first()

    if retrieved_consulta:
        raise AlreadyExistentConsulta(code=400)

    return


def validate_consulta_identifier(consulta_id: int):
    if not isinstance(consulta_id, int) or consulta_id <= 0:
        raise InvalidFieldValue(code=400)

    return


def validate_card_patch_body(request_body: dict):
    """
    Validates the JSON dictionary sent by the user when updating an Especialidade.

    #Parameters:
        request_body (dict): Dictionary in JSON format sent by the user with the fields to update an Especialidade.

    #Returns:
    """

    possible_status = [
        'todo',
        'doing',
        'done'
    ]

    if request_body.get('name') and not isinstance(request_body.get('name'), str):
        raise InvalidFieldType(code=400)

    if request_body.get('description') and not isinstance(request_body.get('description'), str):
        raise InvalidFieldType(code=400)

    if  request_body.get('status') and not isinstance(request_body.get('status'), str):
        raise InvalidFieldType(code=400)

    if request_body.get('status') not in possible_status:
        raise InvalidFieldValue(code=400)

    return


def validate_especialidade_query_params(query_params: QueryDict):
    possible_fields = ["search"]

    query_params_keys = query_params.keys()

    for current_query_param in query_params_keys:
        if current_query_param not in possible_fields:
            raise IncorrectQueryParams(code=400)

        if not isinstance(query_params.get(current_query_param), str):
            raise IncorrectQueryParams(code=400)

    query_params_filter = query_params.dict()
    if "search" in query_params_keys:
        query_params_filter["nome"] = query_params_filter.pop('search')

    return query_params_filter


def validate_medico_query_params(query_params: QueryDict):
    possible_fields = ["search", "especialidade"]

    query_params_keys = query_params.keys()

    for current_query_param in query_params_keys:
        if current_query_param not in possible_fields:
            raise IncorrectQueryParams(code=400)

    query_params_filter = query_params.dict()
    if "search" in query_params_keys:
        query_params_filter["nome"] = query_params_filter.pop('search')
    if "especialidade" in query_params_keys:
        query_params_filter["especialidade"] = query_params.getlist("especialidade")

    return query_params_filter


def validate_request_query_params(query_params: dict):
    possible_fields = ['medico', 'especialidade', 'data_inicio', 'data_final']

    query_params_keys = query_params.keys()

    for current_query_param in query_params_keys:
        if current_query_param not in possible_fields:
            raise IncorrectQueryParams(code=400)

    if 'data_inicio' in query_params_keys and 'data_final' not in query_params_keys:
        raise IncorrectQueryParams(code=400)

    if query_params.get('data_inicio') and query_params.get('data_final'):
        if not isinstance(query_params.get('data_inicio'), str) and isinstance(query_params.get('data_final'), str):
            raise IncorrectQueryParams(code=400)

        try:
            datetime.strptime(query_params.get('data_inicio'), '%Y-%m-%d')
            datetime.strptime(query_params.get('data_final'), '%Y-%m-%d')
        except TypeError:
            raise IncorrectQueryParams(code=400)

    return

