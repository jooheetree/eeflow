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
        data = {'startDate': '2020-01-20', 'endDate': '2020-01-20'}
        response: Response = self.drf_client.get('/erp/voucher_list/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_payment_list(self):
        data = {'startDate': '2020-01-20', 'endDate': '2020-01-20'}
        response: Response = self.drf_client.get('/erp/payment_list/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_invoice_list(self):
        data = {'startDate': '2020-01-20', 'endDate': '2020-01-20'}
        response: Response = self.drf_client.get('/erp/invoice_list/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_receipt_list(self):
        data = {'startDate': '2020-01-20', 'endDate': '2020-01-20'}
        response: Response = self.drf_client.get('/erp/receipt_list/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_nacct_list(self):
        data = {'startDate': '2020-01-20', 'endDate': '2020-01-20'}
        response: Response = self.drf_client.get('/erp/nacct_list/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_get_erp_invoices_todo_count(self):
        data = {'startDate': '2020-01-20', 'endDate': '2020-01-20'}
        response: Response = self.drf_client.get('/erp/get_todo_count/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
