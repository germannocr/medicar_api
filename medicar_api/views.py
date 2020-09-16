import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from medicar_api.exceptions import CardNotFound
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from medicar_api.serializers import (
    EspecialidadeSerializer, MedicoSerializer
)
from medicar_api.validations import (
    validate_card_post_body,
    validate_card_patch_body, validate_especialidade_query_params
)
from medicar_api.persistency import (
    create_card,
    retrieve_card_by_id,
    delete_retrieved_card,
    update_retrieved_card,
    retrieve_especialidades_list,
    retrieve_medicos_list,
    retrieve_done_cards_list
)
from medicar_api.mappers import (
    map_post_card_response,
    map_delete_response,
    map_update_response,
    map_get_especialidade_response, map_get_medico_response
)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_card(request, card_id: int):
    """
    Delete an existent Especialidade, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to delete the object and about the user
                               who made the request.

    #Returns:
        [NO CONTENT]
    """
    user = request.user
    try:
        retrieved_card = retrieve_card_by_id(card_id=card_id, user_id=user.id)
        if retrieved_card:
            delete_retrieved_card(retrieved_card)
            response = map_delete_response()

            return response
        else:
            raise CardNotFound()

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



@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_card(request, card_id: int):
    """
    Update an existent Especialidade, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to update the object and about the user
                               who made the request.

    #Returns:
        [NO CONTENT]
    """
    request_body = json.loads(request.body)
    user = request.user
    try:
        validate_card_patch_body(request_body=request_body)
        retrieved_card = retrieve_card_by_id(card_id=card_id, user_id=user.id)
        if retrieved_card:
            update_retrieved_card(retrieved_card=retrieved_card, request_body=request_body)
            response = map_update_response()
            return response
        else:
            raise CardNotFound()

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
def add_card(request):
    """
    Creates a new Especialidade, performing all necessary validations.

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
        validate_card_post_body(request_body=request_body)
        new_card = create_card(request_body=request_body,
                               request_user=user)
        serializer_response = EspecialidadeSerializer(new_card)
        mapped_response = map_post_card_response(serializer_response)
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
    Retrieve existent Especialidade with 'todo' status, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the card objects list

    #Returns:
        [NO CONTENT]
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
    Retrieve existent Especialidade with 'doing' status, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the card objects list and about the user
                               who made the request.

    #Returns:
        [NO CONTENT]
    """
    try:
        retrieved_medicos_list = retrieve_medicos_list()
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
def retrieve_done_cards(request):
    """
    Retrieve existent Especialidade with 'done' status, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the card objects list and about the user
                               who made the request.

    #Returns:
        [NO CONTENT]
    """
    user = request.user
    try:
        retrieved_cards_list = retrieve_done_cards_list(user_id=user.id)
        serialized_response = EspecialidadeSerializer(retrieved_cards_list, many=True)
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
