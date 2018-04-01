from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from accounts.views import password_change_view_c


class password_change_tests_c(TestCase):
    def setUp(self):
        username = 'user1'
        password = 'secret123'
        user = User.objects.create_user(username=username, email='user1@test.local', password=password)
        url = reverse('accounts:pass_changing')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

#skip
    def test_url_resolves_correct_view(self):
        view = resolve('/accounts/pass_changing/')
        self.assertEquals(view.func.view_class, password_change_view_c)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)

#skip
class login_required_password_change_tests_c(TestCase):
    def test_redirection(self):
        url = reverse('accounts:pass_changing')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class password_change_test_case_c(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='user1', email='user1@test.local', password='old_password')
        self.url = reverse('accounts:pass_changing')
        self.client.login(username='user1', password='old_password')
        self.response = self.client.post(self.url, data)


class successful_password_change_tests_c(password_change_test_case_c):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('accounts:pass_changed'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class invalid_password_change_tests_c(password_change_test_case_c):
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertIsNotNone(form)
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
