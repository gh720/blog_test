from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from accounts.forms import sign_up_form_c
from accounts.views import signup


class sign_up_tests_c(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, sign_up_form_c)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class sign_up_form_test_c(TestCase):
    def test_form_has_fields(self):
        form = sign_up_form_c()
        expected = ['username', 'email', 'password1', 'password2', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class successful_sign_up_tests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'user1',
            'email': 'user1@test.local',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')


    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the home page
        '''
        self.assertRedirects(self.response, self.home_url)


    def test_user_creation(self):
        self.assertTrue(User.objects.exists())


    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class invalid_sign_up_tests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
