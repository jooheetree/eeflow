import json

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.test import APIClient

from employee.models import Position, Department, Employee, POSITION_ORDER, DEPARTMENT_ORDER
from .models import Push, Document, Attachment, Sign, DefaulSignList, SIGN_TYPE
from pywebpush import webpush

# class HomePageTest(TestCase):
#
#     def test_root_url_resolves_to_home_page_view(self):
#         found = resolve('/')
#         self.assertEqual(found.func, home_page)
#
#     def test_home_page_returns_correct_html(self):
#         response = self.client.get('/')
#         self.assertTemplateUsed(response, 'home.html')
#
#     def test_can_save_a_POST_request(self):
#         response = self.client.post('/', data={'item_text': 'A new list item'})
#         # self.assertIn('A new list item', response.content.decode())
#         # self.assertTemplateUsed(response, 'home.html')
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response['location'], '/')
#
#     def test_only_saves_items_when_necessary(self):
#         self.client.get('/')
#         self.assertEqual(Item.objects.count(), 0)
#
#     def test_displays_all_list_items(self):
#         Item.objects.create(text='itemey 1')
#         Item.objects.create(text='itemey 2')
#
#         response = self.client.get('/')
#
#         self.assertIn('itemey 1', response.content.decode())
#         self.assertIn('itemey 2', response.content.decode())
#

ENDPOINT = 'https://fcm.googleapis.com/fcm/send/eqwmBSui0z0:APA91bH7ejT77FRQxjlXcxKdwMp3H7_vM2Ybj2jO1Fk5' \
           'xXTOyZ7pTkfgQa5eUKl651VtMklqeSlCmXGRzbroaXTPXyg0sQdcU0qaR5br5QF8l316rjc8kndJdV0knJB77cw5q99' \
           'fcoD3'
P256dh = 'BG15pJmeP6bZ1uEk1mFTyazB-wb8sgwRstPbXYeTaBWTtNHw5cHU1MBcx2P_5oJ1Ii_4uk-Jjh--XRxneUJi9po'
AUTH = 'pd-7EmXSFy_6Y72NaK5aCA'


class InitData:
    def create_push_data(self, user: User) -> Push:
        return Push.objects.create(
            user=user,
            endpoint=ENDPOINT,
            p256dh=P256dh,
            auth=AUTH
        )

    def user_create(self, username: str, password: str, first_name: str,
                    department: str = '', position: str = '') -> User:
        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name
        )
        user.employee.position = Position.objects.first()
        user.employee.department = Department.objects.first()
        user.save()
        self.create_push_data(user)
        return user

    def login(self, client) -> str:
        response = client.post('/rest-auth/login/', data={
            "username": "swl21803",
            "password": "swl21803",
        })
        return response.data['key']

    def position_create(self):
        for position in POSITION_ORDER:
            Position(**position).save()

    def department_create(self):
        for department in DEPARTMENT_ORDER:
            Department(**department).save()


class PushTest(InitData, TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='testuser',
            password='testuser'
        )
        self.client.force_login(self.user)
        self.endpoint = ENDPOINT
        self.p256dh = P256dh
        self.auth = AUTH
        self.push = self.create_push_data(self.user)

    def test_saving_data(self):
        self.assertEqual(self.push.user, self.user)
        self.assertEqual(self.push.endpoint, self.endpoint)
        self.assertEqual(self.push.p256dh, self.p256dh)
        self.assertEqual(self.push.auth, self.auth)

    def test_view(self):
        response = self.client.post('/ea/push/')
        self.assertEqual(response.status_code, 200)


class EaTest(InitData, TestCase):
    """
    사용자 결재 상신 시 사용되는 Model(Document, Attachment, Sign) 테스트
    """

    def setUp(self) -> None:
        self.position_create()
        self.department_create()

        self.user = self.user_create('swl21803', 'swl21803', '이승우')
        self.user.set_password('swl21803')
        self.user.save()

        self.supervisor1 = self.user_create('cyl20509', 'cyl20509', '이철용')
        self.supervisor2 = self.user_create('jyy20510', 'jyy20510', '윤주영')
        self.supervisor3 = self.user_create('hck18106', 'hck18106', '김희철')

        self.client.force_login(self.user)

        self.document_create()

        self.attachment_create('test1', 20, '/attachment/test1.jpg')
        self.attachment_create('test2', 20, '/attachment/test2.jpg')

        self.sign_create(self.supervisor1, 0)
        self.sign_create(self.supervisor2, 1)
        self.sign_create(self.supervisor3, 2)

        self.defaulsignlist_create(self.user, self.supervisor1.employee, 0, 0)
        self.defaulsignlist_create(self.user, self.supervisor2.employee, 0, 1)
        self.defaulsignlist_create(self.user, self.supervisor3.employee, 0, 2)

        token: str = self.login(self.client)
        self.drf_client = APIClient()
        self.drf_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def document_create(self) -> None:
        self.title = '업무종결보고서'
        self.sign_list = '이철용->윤주영'
        self.batch_number = 1111
        return Document.objects.create(
            author=self.user,
            title=self.title,
            sign_list=self.sign_list,
            batch_number=self.batch_number
        )

    def attachment_create(self, title: str, size: int, path: str) -> None:
        return Attachment.objects.create(
            document=Document.objects.first(),
            title=title,
            size=size,
            path=settings.MEDIA_URL + path
        )

    def sign_create(self, user: User, seq: int) -> None:
        result = Sign.get_result_type_by_seq(seq)
        return Sign.objects.create(
            user=user,
            document=Document.objects.first(),
            seq=seq,
            result=result
        )

    def defaulsignlist_create(self, user: User, approver: Employee, type, order: int) -> None:
        return DefaulSignList.objects.create(
            user=user,
            approver=approver,
            type=type,
            order=order
        )

    def test_document_create(self):
        document = Document.objects.first()
        self.assertEqual(document.title, self.title)
        self.assertEqual(document.sign_list, self.sign_list)
        self.assertEqual(document.get_doc_status_display(), '결재대기중')

    def test_attachment_create(self):
        document = Document.objects.first()
        attachments = Attachment.objects.all()

        for attachment in attachments:
            self.assertEqual(document, attachment.document)

        self.assertCountEqual(document.attachments.all(), attachments)

    def test_sign_create(self):
        document = Document.objects.first()
        sign = Sign.objects.first()

        self.assertEqual(sign.document, document)
        self.assertEqual(sign.get_result_display(), '대기중')
        self.assertEqual(sign.get_type_display(), '결재')
        self.assertIsInstance(sign.user, User)

    def test_defaulsignlist_create(self):
        for defaulSignList in DefaulSignList.objects.all():
            self.assertEqual(defaulSignList.user, self.user)

    def test_sign_after_approve(self):
        sign = self.approve_sign(Sign.objects.get(seq=1))
        self.assertEqual(sign.get_result_display(), '승인')
        self.assertEqual(sign.comment, '승인합니다')

    def test_sign_after_deny(self):
        sign = self.deny_sign(Sign.objects.get(seq=2))
        self.assertEqual(sign.get_result_display(), '반려')
        self.assertEqual(sign.comment, '반려합니다')
        self.assertEqual(sign.document.get_doc_status_display(), '반려')

    def approve_sign(self, sign: Sign) -> Sign:
        sign.approve()
        sign.comment = "승인합니다"
        sign.sign_date = timezone.now()
        next_sign = sign.get_next_sign()
        if next_sign:
            next_sign.notify_next_user('결재가있씁니다')

        return sign

    def deny_sign(self, sign: Sign) -> Sign:
        sign.deny()
        sign.comment = "반려합니다"
        sign.sign_date = timezone.now()
        sign.document.finish_deny('[push] 반려요!')
        return sign

    def test_create_document_view(self):
        """
        create Document View Test
        """
        image1 = settings.MEDIA_ROOT + "/test/3.png"
        pdf1 = settings.MEDIA_ROOT + "/test/test.pdf"
        upload_img1 = SimpleUploadedFile("test1.png", content=open(image1, "rb").read())
        upload_pdf1 = SimpleUploadedFile("pdf1.pdf", content=open(pdf1, "rb").read())
        approvers = [
            {"id": "cyl20509", "type": 0},
            {"id": "jyy20510", "type": 0},
            {"id": "hck18106", "type": 0},
        ]
        data = {
            "author": "swl21803",
            "batch_number": 3333,
            "title": "비료사업부 12월 고용보험료/7",
            "attachments": [upload_img1, upload_pdf1],
            "approvers": json.dumps(approvers)
        }

        response: Response = self.drf_client.post('/ea/create_document/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_get_defaultUsers_view(self):
        response: Response = self.drf_client.get('/ea/get_defaultUsers/' + self.user.username)
        self.assertGreaterEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_get_departmentUsers_view(self):
        response: Response = self.drf_client.get('/ea/get_departmentUsers/' + self.user.employee.department.name)
        self.assertGreaterEqual(len(response.data), 3)
        self.assertEqual(response.status_code, 200)

    def test_written_document_view(self):
        response: Response = self.drf_client.get('/ea/written_document/' + self.user.username)
        self.assertEqual(response.status_code, 200)
