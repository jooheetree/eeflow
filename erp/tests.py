from django.test import TestCase
from django.urls import resolve
from requests import Response
from rest_framework.test import APIClient

from ea.tests import InitData
from erp.views import voucher_list


class ErpTest(InitData, TestCase):

    def setUp(self) -> None:
        self.position_create()
        self.department_create()

        self.user = self.user_create('swl21803', 'swl21803', '이승우')
        self.user.set_password('swl21803')
        self.user.save()

        token: str = self.login(self.client)
        self.drf_client = APIClient()
        self.drf_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_voucher_view(self):
        response: Response = self.drf_client.get('/erp/voucher_list/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_voucher_batch_number_view(self):
        response: Response = self.drf_client.get(f'/erp/voucher_list/{4181}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

