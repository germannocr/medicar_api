import datetime

from medicar_api.mappers import retrieve_current_date_and_time, remove_invalid_horario_from_list
from medicar_api.models import (
    Especialidade, Medico, Consulta, Agenda
)


def delete_retrieved_consulta(retrieved_consulta: Consulta):
    retrieved_consulta.delete()

    return


def retrieve_consulta(consulta_id: int, user_id: int):
    current_date, current_time = retrieve_current_date_and_time()
    retrieved_consulta = Consulta.objects.filter(
        id=consulta_id,
        created_by_user=user_id,
        dia__gte=current_date,
        horario__gte=current_time
    ).first()

    return retrieved_consulta


def create_consulta(request_body: dict, retrieved_agenda: Agenda, user_id: int):

    created_consulta = Consulta.objects.create(
        horario=request_body.get('horario'),
        dia=retrieved_agenda.dia,
        medico=retrieved_agenda.medico,
        created_by_user=user_id
    )

    return created_consulta


def retrieve_especialidades_list(query_params: dict = None):
    retrieved_especialidades_list = Especialidade.objects.filter(**query_params).all()

    return retrieved_especialidades_list


def retrieve_medicos_list(query_params: dict = None):
    if "especialidade" in query_params:
        retrieved_medicos_list = Medico.objects.filter(
            especialidade__id__in=query_params.pop("especialidade"),
            **query_params
        ).all()
    else:
        retrieved_medicos_list = Medico.objects.filter(**query_params).all()

    return retrieved_medicos_list


def retrieve_agendas_list(user_id: int, query_params: dict = None):
    current_date, current_time = retrieve_current_date_and_time()

    retrieved_agendas_list = Agenda.objects.filter(dia__gte=current_date, **query_params).all().order_by("dia")

    existent_consultas_list = Consulta.objects.filter(dia__gte=current_date, horario__gte=current_time).all()

    retrieved_agendas_list = remove_invalid_horario_from_list(
        retrieved_agendas_list=retrieved_agendas_list,
        existent_consultas_list=existent_consultas_list,
        current_time=current_time,
        current_date=current_date,
        user_id=user_id
    )

    return retrieved_agendas_list


def retrieve_consultas_list(user_id: int):
    current_date, current_time = retrieve_current_date_and_time()
    retrieved_consultas_list = Consulta.objects.filter(
        dia__gte=current_date,
        horario__gte=current_time,
        created_by_user=user_id
    ).order_by("dia", "horario").all()

    return retrieved_consultas_list
