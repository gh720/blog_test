from time import sleep

import re
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse

from posts.models import Post, Tag

from  posts.common import response_decode as dec


class post_view_tests_c(TestCase):
    post1=None
    post2=None

    def setUp(self):
        self.pass1='user1pw'
        self.pass2='user2pw'
        self.user1=User.objects.create_user(username='user1', email='user1@asdf.com', password=self.pass1)
        self.user2=User.objects.create_user(username='user2', email='user2@asdf.com', password=self.pass2)
        self.post1=Post.objects.create(created_by=self.user1, message='msg1 from user1', title='post1 title')
        self.post2=Post.objects.create(created_by=self.user2, message='msg2 from user2', title='post2 title')
        self.test_tag='done___tag'
        self.tag = Tag.objects.create(tag=self.test_tag)
        self.post2.tags.add(self.tag)

        self.logged_in = self.client.login(username=self.user2.username, password=self.pass2)
        return

    def assert_status(self,url,code):
        self.assertTrue(self.logged_in, msg="The user is not logged in")
        response = self.client.get(url)
        self.assertEquals(response.status_code, code)

    def test_setup_check(self):
        self.assertTrue(self.user1)
        self.assertTrue(self.user2)
        self.assertTrue(self.post1)
        self.assertTrue(self.post2)
        self.assertTrue(self.user2.is_authenticated)

    def test_new_post_200(self):
        url=reverse('new_post')
        self.assert_status(url, 200)

    def test_edit_own(self):
        url = reverse('edit_post', kwargs={'post_pk': self.post2.pk})
        self.assert_status(url, 200)

    def test_edit_not_own(self):
        url = reverse('edit_post', kwargs={'post_pk': self.post1.pk})
        response=self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('accounts:login'),  url))

    def test_edit_non_existing(self):
        url = reverse('edit_post', kwargs={'post_pk': 99})
        self.assert_status(url, 404)

    def test_edit_has_tag(self):
        url = reverse('edit_post', kwargs={'post_pk': self.post2.pk})
        response = self.client.get(url)
        text = dec(response)
        self.assertEqual(1, len(re.findall(r'data-current_tags="[^"]*\b%s' % ( self.test_tag ), text)))

    def test_details_has_controls(self):
        url = reverse('post_details', kwargs={'post_pk': self.post2.pk})
        response = self.client.get(url)
        t = dec(response)
        self.assertEqual(1,len(re.findall(r'<a class="[^"]*\bbtn_edit_post\b', t)))
        self.assertEqual(1,len(re.findall(r'<a class="[^"]*\bbtn_remove_post\b', t)))

    def edit_is_a_form(self):
        url = reverse('edit_post', kwargs={'post_pk': self.post2.pk})
        response = self.client.get(url)
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

        dec = response.content.decode()
        self.assertInHTML('<a class="btn_edit_post">', dec)
        self.assertInHTML('<a class="btn_remove_post">', dec)

    def test_csrf(self):
        url = reverse('new_post')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_valid_posting(self):
        url = reverse('new_post')
        data = {
            'title': 'Test title',
            'message': 'test message',
        }
        response = self.client.post(url, data)
        self.assertEqual(Post.objects.count(), 3)
        self.assertRedirects(response, (reverse('home')))

    def test_invalid_posting(self):
        url = reverse('new_post')
        data = {
            'title': '',
            'message': '',
        }
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)




###### new post


    # def test_edit_own_post_200(self):
    #     url=reverse('edit_post', kwargs=dict(post_pk=)