from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test import Client
from django.utils import timezone

from .models import Push, Document, Attachment, Sign
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


def create_push_data(user: User) -> Push:
    return Push.objects.create(
        user=user,
        endpoint=ENDPOINT,
        p256dh=P256dh,
        auth=AUTH
    )


class PushTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='testuser',
            password='testuser'
        )
        self.client.force_login(self.user)

        self.endpoint = ENDPOINT
        self.p256dh = P256dh
        self.auth = AUTH
        self.push = create_push_data(self.user)

    def test_saving_data(self):
        self.assertEqual(self.push.user, self.user)
        self.assertEqual(self.push.endpoint, self.endpoint)
        self.assertEqual(self.push.p256dh, self.p256dh)
        self.assertEqual(self.push.auth, self.auth)

    def test_view(self):
        response = self.client.post('/ea/push/')
        self.assertEqual(response.status_code, 200)


class EaModelTest(TestCase):
    """
    사용자 결재 상신 시 사용되는 Model(Document, Attachment, Sign) 테스트
    """

    def setUp(self) -> None:
        self.group = Group.objects.create(
            name='전산팀'
        )
        self.user = self.user_create('testuser', 'testuser')
        self.supervisor1 = self.user_create('supervisor1', 'supervisor1')
        self.supervisor2 = self.user_create('supervisor2', 'supervisor2')
        self.supervisor3 = self.user_create('supervisor3', 'supervisor3')

        self.client.force_login(self.user)
        self.document_create()
        self.attachment_create('/attachment/test1.jpg')
        self.attachment_create('/attachment/test2.jpg')
        self.sign_create(self.supervisor1, 1)
        self.sign_create(self.supervisor2, 2)
        self.sign_create(self.supervisor3, 3)

    def document_create(self) -> None:
        self.title = '업무종결보고서'
        self.content = '최선을 다했습니다'
        self.sign_list = '이철용->윤주영'
        return Document.objects.create(
            author=self.user,
            group=self.group,
            title=self.title,
            content=self.content,
            sign_list=self.sign_list
        )

    def attachment_create(self, path: str) -> None:
        return Attachment.objects.create(
            document=Document.objects.first(),
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

    def user_create(self, username: str, password: str) -> User:
        user = User.objects.create(
            username=username,
            password=password,
        )

        create_push_data(user)
        return user

    def test_user_group(self):
        document = Document.objects.first()
        push_data = Push.objects.get(user=self.user)
        self.user.groups.add(self.group)
        self.assertEqual(self.user.groups.first(), self.group)
        self.assertEqual(self.user.document.first(), document)
        self.assertEqual(self.group.document.first(), document)
        self.assertEqual(self.user.push_data.first(), push_data)

    def test_document_create(self):
        document = Document.objects.first()
        self.assertEqual(document.title, self.title)
        self.assertEqual(document.content, self.content)
        self.assertEqual(document.sign_list, self.sign_list)
        self.assertEqual(document.get_doc_status_display(), '결재대기중')

    def test_attachment_create(self):
        document = Document.objects.first()
        attachments = Attachment.objects.all()

        for attachment in attachments:
            self.assertEqual(document, attachment.document)

        self.assertCountEqual(document.attachment.all(), attachments)

    def test_sign_create(self):
        document = Document.objects.first()
        sign = Sign.objects.first()

        self.assertEqual(sign.document, document)
        self.assertEqual(sign.get_result_display(), '대기중')
        self.assertEqual(sign.get_type_display(), '결재')
        self.assertIsInstance(sign.user, User)

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

