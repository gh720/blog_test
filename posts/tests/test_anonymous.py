from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, RegexURLPattern

import blog
from posts import common
from posts.models import Post


class post_view_tests_c(TestCase):
    post1=None
    post2=None

    free_access_urls=[
        reverse('accounts:login')
        , reverse('accounts:logout')
        , reverse('home')
    ]

    def assert_status(self,url,code):
        response = self.client.get(url)
        self.assertEquals(response.status_code, code)

    def setUp(self):
        User.objects.create(username='user1', email='user1@asdf.com', password='user1pw')
        self.post1=Post.objects.create(message='msg1 from user1', title='post1 title')

    def test_free_access_200(self):
        for url in self.free_access_urls:
            self.assert_status(url,200)

    def test_new_post_403(self):
        self.assert_status(reverse('new_post'), 40)

    def test_403(self):
        entry:RegexURLPattern
        for entry in common.get_all_url_entries():
            if entry.regex.groupindex.get('post_pk') and len(entry.regex.groupindex)==1:
                url = reverse(entry.name, dict(post_pk=self.post1.pk))
            elif len(entry.regex.groupindex)==0:
                url = reverse(entry.name)
            if url in self.free_access_urls:
                self.assert_status(url, 200)
            else:
                self.assert_status(url, 403)




