from rest_framework.exceptions import APIException


class AlreadyExistentConsulta(APIException):
    status_code = 400
    default_detail = "An Consulta with this information already exists. Please schedule a new Consulta at" \
                     " another time or day.."
    default_code = "already_existent_consulta"


class IncorrectQueryParams(APIException):
    status_code = 400
    default_detail = "The fields passed in the query params are invalid. The only possible field is 'search' as" \
                     " the key and the name of a specialty as the value."
    default_code = "incorrect_query_params"


class MissingRequiredFields(APIException):
    status_code = 400
    default_detail = "Missing required field. " \
                     "Please send all the necessary fields, including name, description and card status."
    default_code = "missing_required_field"


class InvalidFieldType(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect type of one of the fields in the request."
    default_code = "incorrect_field_type"


class InvalidFieldValue(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect value of one of the fields in the request."
    default_code = "incorrect_field_value"


class CardNotFound(APIException):
    status_code = 404
    default_detail = "This card doesnt exist."
    default_code = "card_not_found"
