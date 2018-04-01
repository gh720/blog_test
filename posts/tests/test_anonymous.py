import re
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, RegexURLPattern

import blog
from blog import urls
from posts import common
from posts.models import Post, Tag

from  posts.common import response_decode as dec

class post_view_tests_c(TestCase):
    post1=None
    post2=None

    free_access_urls=[
        reverse('accounts:login')
        , reverse('accounts:signup')
        , reverse('accounts:pass_reset')
        , reverse('home')
        , reverse('tags')
        , reverse('lightning_logo')
        , reverse('admin:login')
        , re.compile(r'^/posts/\d+/details/$')
        , re.compile(r'^/tags/\d+/$')
    ]

    def anon_status(self,_url):
        for url in self.free_access_urls:
            if type(url)==str:
                if _url==url:
                    return 200
            elif type(url)==re._pattern_type:
                if re.search(url, _url):
                    return 200
            else:
                raise(Exception("unknown url type"))
        return 302

    def assert_status(self,url,code,msg=None):
        response = self.client.get(url)
        self.assertEquals(response.status_code, code, msg=msg)

    def setUp(self):
        self.pass1='user1pw'
        self.user1=User.objects.create_user(username='user1', email='user1@asdf.com', password=self.pass1)
        self.post1=Post.objects.create(created_by=self.user1, message='msg1 from user1', title='post1 title')
        self.tag1 = Tag.objects.create(tag='done___tag')
        self.post1.tags.add(self.tag1)

    def test_403(self):
        entry:RegexURLPattern
        for entry,namespace,depth in common.get_all_url_entries(urls.urlpatterns):
            if namespace=='admin' and depth>=2:
                continue
            full_entry_name = entry.name if namespace==None else namespace+":"+entry.name
            try:
                if entry.regex.groupindex.get('post_pk') and len(entry.regex.groupindex)==1:
                    url = reverse(full_entry_name, kwargs=dict(post_pk=self.post1.pk))
                elif entry.regex.groupindex.get('tag_pk') and len(entry.regex.groupindex) == 1:
                    url = reverse(full_entry_name, namespace=entry.namespace, kwargs=dict(tag_pk=self.tag1.pk))
                elif len(entry.regex.groupindex)==0:
                    url = reverse(full_entry_name)
            except:
                debug=1
                pass
            status = self.anon_status(url)
            try:
                response = self.client.get(url)
            except:
                debug=1
            self.assertEqual(response.status_code, status, msg=url)

    def test_edit_pv(self):
        url=reverse('edit_post_pv', kwargs=dict(post_pk=self.post1.pk))
        response= self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('accounts:login'), url))

    def test_edit_not_own(self):
        url = reverse('edit_post', kwargs={'post_pk': self.post1.pk})
        response=self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('accounts:login'),  url))


