import json
import os
import socket
from datetime import datetime
from decimal import Decimal
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.test import (
    TestCase,
    Client
)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

client = Client()
API_URL = os.environ.get('API_URL', 'http://localhost:8000/')


class CardCreation(TestCase):
    def setUp(self):
        user_payload = {
            "username": "germannocorreia",
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
            "name": "criar planilha",
            "description": "Criar planilha para gerência de custos mensais",
            "status": "todo",
        }
        self.invalid_payload = {
            "name": -30000.0,
            "description": True
        }

    def test_create_card(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'todo')

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_todo_card(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'todo')

    def test_create_doing_card(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        card_body = {
            "name": "criar planilha",
            "description": "Criar planilha para gerência de custos mensais",
            "status": "doing",
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(card_body),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}doing_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'doing')

    def test_create_done_card(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        card_body = {
            "name": "criar planilha",
            "description": "Criar planilha para gerência de custos mensais",
            "status": "done",
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(card_body),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}done_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'done')


class CardUpdate(TestCase):
    def setUp(self):
        user_payload = {
            "username": "germannocorreia",
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
            "name": "criar planilha",
            "description": "Criar planilha para gerência de custos mensais",
            "status": "todo",
        }
        self.invalid_payload = {
            "name": -30000.0,
            "description": True
        }

    def test_create_todo_card_update_to_doing(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'todo')

        card_id = response.get('id')

        card_update_body = {
            "status": "doing"
        }

        response = client.patch(
            f"{API_URL}update_card/{card_id}/",
            data=json.dumps(card_update_body),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response, [])

        response = client.get(
            f"{API_URL}doing_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'doing')

    def test_create_todo_card_update_to_done(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'todo')

        card_id = response.get('id')

        card_update_body = {
            "status": "done"
        }

        response = client.patch(
            f"{API_URL}update_card/{card_id}/",
            data=json.dumps(card_update_body),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response, [])

        response = client.get(
            f"{API_URL}done_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'done')


class CardDelete(TestCase):
    def setUp(self):
        user_payload = {
            "username": "germannocorreia",
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
            "name": "criar planilha",
            "description": "Criar planilha para gerência de custos mensais",
            "status": "todo",
        }
        self.invalid_payload = {
            "name": -30000.0,
            "description": True
        }

    def test_create_todo_card_delete(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}create_card/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'criar planilha')
        self.assertEqual(response.get('description'), 'Criar planilha para gerência de custos mensais')
        self.assertEqual(response.get('status'), 'todo')

        card_id = response.get('id')

        response = client.delete(
            f"{API_URL}delete_card/{card_id}/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = client.get(
            f"{API_URL}todo_cards/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response, [])
