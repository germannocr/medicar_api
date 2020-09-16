
from medicar_api.exceptions import (
    MissingRequiredFields,
    InvalidFieldType,
    InvalidFieldValue, IncorrectQueryParams,
)


def validate_card_post_body(request_body: dict):
    """
    Validates the JSON dictionary sent by the user when creating an Especialidade.

    #Parameters:
        request_body (dict): Dictionary in JSON format sent by the user with the fields to create an Especialidade.

    #Returns:
    """
    required_fields = [
        'name',
        'description',
        'status'
    ]

    possible_status = [
        'todo',
        'doing',
        'done'
    ]

    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields(code=400)

    if not isinstance(request_body.get('name'), str):
        raise InvalidFieldType(code=400)

    if not isinstance(request_body.get('description'), str):
        raise InvalidFieldType(code=400)

    if not isinstance(request_body.get('status'), str):
        raise InvalidFieldType(code=400)

    if request_body.get('status') not in possible_status:
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


def validate_especialidade_query_params(query_params: dict):
    possible_fields = ["search"]

    query_params_keys = query_params.keys()

    for current_query_param in query_params_keys:
        if current_query_param not in possible_fields:
            raise IncorrectQueryParams(code=400)

        if not isinstance(query_params.get(current_query_param), str):
            raise IncorrectQueryParams(code=400)

    query_params_filter = dict(query_params)
    if "search" in query_params_keys:
        query_params_filter["name"] = query_params.pop('search')

    return query_params_filter
