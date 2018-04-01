from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class password_reset_mail_tests_c(TestCase):
    def setUp(self):
        User.objects.create_user(username='user1', email='user1@test.local', password='123')
        self.response = self.client.post(reverse('accounts:pass_reset'), { 'email': 'user1@test.local' })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[art_int_blog] Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('accounts:pass_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('user1', self.email.body)
        self.assertIn('user1@test.local', self.email.body)

    def test_email_to(self):
        self.assertEqual(['user1@test.local',], self.email.to)
