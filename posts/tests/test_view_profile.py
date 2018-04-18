import re
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse


class post_view_tests_c(TestCase):
    pass

    def setUp(self):
        self.pass1='user1pw'
        self.user1=User.objects.create_user(username='user1', email='user1@asdf.com', password=self.pass1)
        self.logged_in = self.client.login(username=self.user1.username, password=self.pass1)
        return

    def test_view_profile(self):
        url = reverse('accounts:profile', kwargs={'user_pk': self.user1.pk})
        response = self.client.get(url)
        #self.user1.refresh_from_db()
        edit_url = reverse('accounts:edit_profile', kwargs={'profile_pk': self.user1.profile.pk})
        self.assertContains(response, 'href="{0}"'.format(edit_url))
        self.assertContains(response, 'class="profile_user_name">{0}'.format(self.user1.username))

    def test_edit_profile(self):
        url = reverse('accounts:profile', kwargs={'user_pk': self.user1.pk})
        # instantiating profile
        response = self.client.get(url)
        # refreshing the user object
        #self.user1.refresh_from_db()
        url = reverse('accounts:edit_profile', kwargs={'profile_pk': self.user1.profile.pk})
        response = self.client.get(url)
        self.assertContains(response, 'class="profile_user_name">{0}'.format(self.user1.username))
        form = response.context.get('form')
        self.assertIsInstance(form, ModelForm)

        dec = response.content.decode()
        self.assertTrue(re.search(r'<button[^>]*class="[^"]*\bbtn_save_profile\b"', dec))
