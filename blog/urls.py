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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from blog import settings
from posts import views as posts_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', posts_views.PostListView.as_view(),name="home"),
    url(r'^posts/(?P<post_pk>\d+)/details/$', posts_views.PostDetailsView.as_view(), name='post_details'),
    url(r'^login/$', posts_views.login_view_c.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', account_views.signup, name='signup'),
    url(r'^posts/(?P<post_pk>\d+)/edit/$', posts_views.PostEditView.as_view(), name='edit_post'),
    url(r'^posts/new_post/$', posts_views.post_create_view_c.as_view(), name='new_post'),
    url(r'^posts/(?P<post_pk>\d+)/delete/$', posts_views.remove_post, name='remove_post'),
    # url(r'^posts/(?P<post_pk>\d+)/new_comment/$', posts_views.PostDetailsView.as_view(), name='new_comment'),
    url(r'^posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/delete/$', posts_views.remove_comment, name='remove_comment'),
    url(r'^tags/$', posts_views.get_tags, name='tags'),
    url(r'^profile/(?P<profile_pk>\d+)/edit/$', account_views.profile_edit_view_c.as_view(), name='edit_profile'),
    url(r'^profile/(?P<user_pk>\d+)/$', account_views.profile_view_c.as_view(), name='profile'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
