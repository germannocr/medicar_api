import json
import os
from datetime import time, date
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.test import (
    TestCase,
    Client
)

from medicar_api.models import Agenda, Medico, Especialidade

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

client = Client()
API_URL = os.environ.get('API_URL', 'http://localhost:8000/')


def create_new_medico():
    created_especialidade = Especialidade.objects.create(
        nome="Pediatria"
    )

    created_medico = Medico.objects.create(
        nome="Bruno Barreto",
        crm=56456141,
        email="bruno@intmed.com",
        telefone="66666666",
        especialidade=created_especialidade
    )

    return created_medico


class RetrieveAgenda(TestCase):
    def setUp(self):
        especialidade_test = Especialidade.objects.create(
            nome="Clinico geral"
        )
        medico_test = Medico.objects.create(
            nome="Glairton Santos",
            crm=1534862,
            email="glairton@intmed.com",
            telefone="999999999",
            especialidade=especialidade_test
        )
        agenda_test = Agenda.objects.create(
            medico=medico_test,
            dia=date(year=2020, month=12, day=30),
            horarios=[time(hour=14, minute=00)],
        )
        user_payload = {
            "username": "fabio",
            "password1": "senhadeteste",
            "password2": "senhadeteste"
        }
        response = client.post(
            f"{API_URL}registration/",
            data=json.dumps(user_payload),
            content_type='application/json'
        )

        self.token = json.loads(response.content)["token"]

    def test_get_agendas(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}retrieve_agendas/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('id'), 3)
        self.assertEqual(response.get('medico').get('id'), 3)
        self.assertEqual(response.get('medico').get('nome'), "Glairton Santos")
        self.assertEqual(response.get('medico').get('crm'), 1534862)
        self.assertEqual(response.get('medico').get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "999999999")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 3)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Clinico geral")
        self.assertEqual(response.get('horarios'), ["14:00"])
        self.assertEqual(response.get('dia'), "2020-12-30")

        created_medico = create_new_medico()

        Agenda.objects.create(
            medico=created_medico,
            dia=date(year=2020, month=12, day=20),
            horarios=[time(hour=14, minute=00)]
        )

        response = client.get(
            f"{API_URL}retrieve_agendas/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('medico').get('id'), 4)
        self.assertEqual(response.get('medico').get('nome'), "Bruno Barreto")
        self.assertEqual(response.get('medico').get('crm'), 56456141)
        self.assertEqual(response.get('medico').get('email'), "bruno@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "66666666")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 4)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Pediatria")
        self.assertEqual(response.get('horarios'), ["14:00"])
        self.assertEqual(response.get('dia'), "2020-12-20")

    def test_get_agendas_with_query_parameters(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}retrieve_agendas/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('id'), 5)
        self.assertEqual(response.get('medico').get('id'), 5)
        self.assertEqual(response.get('medico').get('nome'), "Glairton Santos")
        self.assertEqual(response.get('medico').get('crm'), 1534862)
        self.assertEqual(response.get('medico').get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "999999999")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 5)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Clinico geral")
        self.assertEqual(response.get('horarios'), ["14:00"])
        self.assertEqual(response.get('dia'), "2020-12-30")

        created_medico = create_new_medico()

        Agenda.objects.create(
            medico=created_medico,
            dia=date(year=2020, month=12, day=20),
            horarios=[time(hour=14, minute=00)]
        )

        response = client.get(
            f"{API_URL}retrieve_agendas/?medico=5",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('id'), 5)
        self.assertEqual(response.get('medico').get('id'), 5)
        self.assertEqual(response.get('medico').get('nome'), "Glairton Santos")
        self.assertEqual(response.get('medico').get('crm'), 1534862)
        self.assertEqual(response.get('medico').get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "999999999")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 5)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Clinico geral")
        self.assertEqual(response.get('horarios'), ["14:00"])
        self.assertEqual(response.get('dia'), "2020-12-30")

        response = client.get(
            f"{API_URL}retrieve_agendas/?medico=6",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('medico').get('id'), 6)
        self.assertEqual(response.get('medico').get('nome'), "Bruno Barreto")
        self.assertEqual(response.get('medico').get('crm'), 56456141)
        self.assertEqual(response.get('medico').get('email'), "bruno@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "66666666")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 6)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Pediatria")
        self.assertEqual(response.get('horarios'), ["14:00"])
        self.assertEqual(response.get('dia'), "2020-12-20")

        response = client.get(
            f"{API_URL}retrieve_agendas/?data_inicio=2020-11-28&data_final=2020-11-28",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response, [])


class RetrieveMedico(TestCase):
    def setUp(self):
        especialidade_test = Especialidade.objects.create(
            nome="Clinico geral"
        )
        medico_test = Medico.objects.create(
            nome="Glairton Santos",
            crm=1534862,
            email="glairton@intmed.com",
            telefone="999999999",
            especialidade=especialidade_test
        )
        user_payload = {
            "username": "fabio",
            "password1": "senhadeteste",
            "password2": "senhadeteste"
        }
        response = client.post(
            f"{API_URL}registration/",
            data=json.dumps(user_payload),
            content_type='application/json'
        )

        self.token = json.loads(response.content)["token"]

    def test_get_medicos(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}retrieve_medicos/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('id'), 7)
        self.assertEqual(response.get('nome'), "Glairton Santos")
        self.assertEqual(response.get('crm'), 1534862)
        self.assertEqual(response.get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('telefone'), "999999999")
        self.assertEqual(response.get('especialidade').get('id'), 7)
        self.assertEqual(response.get('especialidade').get('nome'), "Clinico geral")

        create_new_medico()

        response = client.get(
            f"{API_URL}retrieve_medicos/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][1]
        self.assertEqual(response.get('id'), 8)
        self.assertEqual(response.get('nome'), "Bruno Barreto")
        self.assertEqual(response.get('crm'), 56456141)
        self.assertEqual(response.get('email'), "bruno@intmed.com")
        self.assertEqual(response.get('telefone'), "66666666")
        self.assertEqual(response.get('especialidade').get('id'), 8)
        self.assertEqual(response.get('especialidade').get('nome'), "Pediatria")


    def test_get_medicos_with_query_parameters(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}retrieve_medicos/?search=Glairton",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('id'), 9)
        self.assertEqual(response.get('nome'), "Glairton Santos")
        self.assertEqual(response.get('crm'), 1534862)
        self.assertEqual(response.get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('telefone'), "999999999")
        self.assertEqual(response.get('especialidade').get('id'), 9)
        self.assertEqual(response.get('especialidade').get('nome'), "Clinico geral")

        create_new_medico()

        response = client.get(
            f"{API_URL}retrieve_medicos/?especialidade=10",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('id'), 10)
        self.assertEqual(response.get('nome'), "Bruno Barreto")
        self.assertEqual(response.get('crm'), 56456141)
        self.assertEqual(response.get('email'), "bruno@intmed.com")
        self.assertEqual(response.get('telefone'), "66666666")
        self.assertEqual(response.get('especialidade').get('id'), 10)
        self.assertEqual(response.get('especialidade').get('nome'), "Pediatria")

        response = client.get(
            f"{API_URL}retrieve_medicos/?search=Sara",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response, [])


class CreateConsulta(TestCase):
    def setUp(self):
        especialidade_test = Especialidade.objects.create(
            nome="Clinico geral"
        )
        medico_test = Medico.objects.create(
            nome="Glairton Santos",
            crm=1534862,
            email="glairton@intmed.com",
            telefone="999999999",
            especialidade=especialidade_test
        )
        agenda_test = Agenda.objects.create(
            medico=medico_test,
            dia=date(year=2020, month=12, day=30),
            horarios=[time(hour=23, minute=00)],
        )
        user_payload = {
            "username": "fabio",
            "password1": "senhadeteste",
            "password2": "senhadeteste"
        }
        response = client.post(
            f"{API_URL}registration/",
            data=json.dumps(user_payload),
            content_type='application/json'
        )

        self.token = json.loads(response.content)["token"]

        self.valid_payload = {
            "agenda_id": agenda_test.id,
            "horario": "23:00"
        }

        self.invalid_payload = {
            "agenda_id": agenda_test.id,
            "horario": "05:00"
        }

    def test_create_consulta(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_consulta/",
            json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('id'), 1)
        self.assertEqual(response.get('medico').get('id'), 1)
        self.assertEqual(response.get('medico').get('nome'), "Glairton Santos")
        self.assertEqual(response.get('medico').get('crm'), 1534862)
        self.assertEqual(response.get('medico').get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "999999999")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 1)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Clinico geral")
        self.assertEqual(response.get('horario'), "23:00")
        self.assertEqual(response.get('dia'), "2020-12-30")

        response = client.post(
            f"{API_URL}create_consulta/",
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.get(
            f"{API_URL}retrieve_agendas/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response, [])


    def test_delete_consulta(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_consulta/",
            json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('id'), 2)
        self.assertEqual(response.get('medico').get('id'), 2)
        self.assertEqual(response.get('medico').get('nome'), "Glairton Santos")
        self.assertEqual(response.get('medico').get('crm'), 1534862)
        self.assertEqual(response.get('medico').get('email'), "glairton@intmed.com")
        self.assertEqual(response.get('medico').get('telefone'), "999999999")
        self.assertEqual(response.get('medico').get('especialidade').get('id'), 2)
        self.assertEqual(response.get('medico').get('especialidade').get('nome'), "Clinico geral")
        self.assertEqual(response.get('horario'), "23:00")
        self.assertEqual(response.get('dia'), "2020-12-30")

        response = client.delete(
            f"{API_URL}delete_consulta/{response.get('id')}/",
            **headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


