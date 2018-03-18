"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth import views as auth_views

import accounts
from blog import settings
from posts import views as posts_views, gen_views
from accounts import views as account_views
from posts.forms import PostForm

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'admin/', include(admin.site.urls)),
    url(r'^$', posts_views.post_list_view_c.as_view(), name="home"),
    url(r'^posts/(?P<post_pk>\d+)/details/$', posts_views.post_details_view_c.as_view(), name='post_details'),
    url(r'^posts/(?P<post_pk>\d+)/edit_pv/$', posts_views.post_edit_form_preview_c(PostForm), name='edit_post_pv'),
    url(r'^posts/(?P<post_pk>\d+)/edit/$', posts_views.post_edit_view_c.as_view(), name='edit_post'),
    url(r'^posts/new_post/$', posts_views.post_create_view_c.as_view(), name='new_post'),
    url(r'^posts/(?P<post_pk>\d+)/delete/$', posts_views.remove_post, name='remove_post'),
    # url(r'^posts/(?P<post_pk>\d+)/new_comment/$', posts_views.PostDetailsView.as_view(), name='new_comment'),
    url(r'^posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/delete/$', posts_views.remove_comment, name='remove_comment'),
    url(r'^tags/$', posts_views.get_tags, name='tags'),

    url(r'^account/', include('accounts.urls',namespace='accounts')),
    url(r'^posts/logo_image/$', gen_views.lightning_logo_view_c.as_view(), name='lightning_logo'),
    url(r'^tags/(?P<tag_pk>\d+)/$', posts_views.tags_view_c.as_view(), name='posts_with_the_tag'),

    url(r'^posts/(?P<post_pk>\d+)/refresh_comments/$', posts_views.comment_refresh_json_c.as_view(), name='refresh_comments'),
    url(r'^posts/(?P<post_pk>\d+)/json_test/$', posts_views.comment_json_c.as_view(), name='json_test'),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 1 and settings.DEBUG:
    import debug_toolbar
    urlpatterns+=url(r'^__debug__/', include(debug_toolbar.urls)),

