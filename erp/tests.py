from django.test import TestCase
from django.urls import resolve
from requests import Response

from erp.views import voucher_list


class ErpTest(TestCase):

    def test_voucher_view(self):
        response: Response = self.client.get('/erp/voucher_list/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        # found = resolve('/erp/voucher/')
        # self.assertEqual(found.func, voucher)
    #
    # def test_home_page_returns_correct_html(self):
    #     response = self.client.get('/')
    #     self.assertTemplateUsed(response, 'home.html')
    #
    # def test_can_save_a_POST_request(self):
    #     response = self.client.post('/', data={'item_text': 'A new list item'})
    #     # self.assertIn('A new list item', response.content.decode())
    #     # self.assertTemplateUsed(response, 'home.html')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response['location'], '/')
    #
    # def test_only_saves_items_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)
    #
    # def test_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #
    #     response = self.client.get('/')
    #
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())
    #
