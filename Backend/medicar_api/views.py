import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from medicar_api.exceptions import ConsultaNotFound
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from medicar_api.serializers import (
    EspecialidadeSerializer, MedicoSerializer, ConsultaSerializer, AgendaSerializer
)
from medicar_api.validations import (
    validate_especialidade_query_params, validate_medico_query_params,
    validate_request_query_params, validate_consulta_post_body, validate_already_existent_consulta,
    validate_consulta_identifier
)
from medicar_api.persistency import (
    retrieve_especialidades_list,
    retrieve_medicos_list,
    retrieve_consultas_list, retrieve_agendas_list, create_consulta, retrieve_consulta, delete_retrieved_consulta
)
from medicar_api.mappers import (
    map_get_especialidade_response, map_get_medico_response, map_get_consulta_response, map_agenda_query_params,
    map_get_agenda_response, map_post_consulta_response, map_delete_response
)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_consulta(request, consulta_id: int):
    """
    Delete an existent Consulta, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to delete the object and about the user
                               who made the request.
        consulta_id (int): Consulta object unique identifier.

    #Returns:
        [NO CONTENT]
    """
    user = request.user
    try:
        validate_consulta_identifier(consulta_id=consulta_id)
        retrieved_consulta = retrieve_consulta(consulta_id=consulta_id, user_id=user.id)
        if retrieved_consulta:
            delete_retrieved_consulta(retrieved_consulta)
            response = map_delete_response()

            return response
        else:
            raise ConsultaNotFound()

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_consulta(request):
    """
    Creates a new Consulta, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to create the object and about the user
                               who made the request.

    #Returns:
        mapped_response (JSON Response): Response, in JSON format, with the information of the created object.
    """
    request_body = json.loads(request.body)
    user = request.user
    try:
        retrieved_agenda = validate_consulta_post_body(request_body=request_body)
        validate_already_existent_consulta(
            request_body=request_body,
            retrieved_agenda=retrieved_agenda,
            user_id=user.id)
        new_consulta = create_consulta(
            request_body=request_body,
            retrieved_agenda=retrieved_agenda,
            user_id=user.id
        )
        serializer_response = ConsultaSerializer(new_consulta)
        mapped_response = map_post_consulta_response(serializer_response)
        return mapped_response

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_especialidades(request):
    """
    Retrieve all existent Especialidade objects, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the Especialidade objects list

    #Returns:
        response (JSON Response): Response, in JSON format, with the information of the Especialidade objects list.
    """
    query_params_filters = request.query_params
    query_params_filters = validate_especialidade_query_params(query_params_filters)
    try:
        retrieved_especialidades_list = retrieve_especialidades_list(query_params=query_params_filters)
        serialized_response = EspecialidadeSerializer(retrieved_especialidades_list, many=True)
        response = map_get_especialidade_response(serialized_response=serialized_response)
        return response

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_medicos(request):
    """
    Retrieve all existent Medico objects, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the Medico objects list

    #Returns:
        response (JSON Response): Response, in JSON format, with the information of the Medico objects list.
    """
    query_params_filters = request.query_params
    query_params_filters = validate_medico_query_params(query_params_filters)
    try:
        retrieved_medicos_list = retrieve_medicos_list(query_params=query_params_filters)
        serialized_response = MedicoSerializer(retrieved_medicos_list, many=True)
        response = map_get_medico_response(serialized_response=serialized_response)
        return response

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_consultas(request):
    """
    Retrieve all existent Consulta objects, performing all necessary validations related to scheduled and past day and
     time.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                                passing necessary information to retrieve the Consulta objects list

    #Returns:
        response (JSON Response): Response, in JSON format, with the information of the Consulta objects list.
    """
    user = request.user
    try:
        retrieved_consultas_list = retrieve_consultas_list(user_id=user.id)
        serialized_response = ConsultaSerializer(retrieved_consultas_list, many=True)
        response = map_get_consulta_response(serialized_response=serialized_response)
        return response

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_agendas(request):
    """
    Retrieve all existent Agenda objects, performing all necessary validations related to schedules and past days and
    time.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                                passing necessary information to retrieve the Agenda objects list

    #Returns:
        response (JSON Response): Response, in JSON format, with the information of the Agenda objects list.
    """
    user = request.user
    query_params = request.query_params
    validate_request_query_params(query_params=query_params)
    query_params_filters = map_agenda_query_params(query_params=query_params)
    try:
        retrieved_agendas_list = retrieve_agendas_list(query_params=query_params_filters, user_id=user.id)
        serialized_response = AgendaSerializer(retrieved_agendas_list, many=True)
        response = map_get_agenda_response(serialized_response=serialized_response)
        return response

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

