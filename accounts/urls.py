from django.conf.urls import url, include
from posts import views as posts_views, gen_views
from accounts import views as account_views
from django.contrib.auth import views as auth_views
import accounts.views as account_views

app_name='accounts'

urlpatterns = [
url(r'^login/$', account_views.login_view_c.as_view(template_name='login.html'), name='login'),
url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
url(r'^signup/$', account_views.signup, name='signup'),

url(r'^profile/(?P<profile_pk>\d+)/edit/$', account_views.profile_edit_view_c.as_view(), name='edit_profile'),
url(r'^profile/(?P<user_pk>\d+)/$', account_views.profile_view_c.as_view(), name='profile'),
url(r'^pass_changing/$', account_views.password_change_view_c.as_view(template_name='pass_changing.html'),
    name='pass_changing'),
url(r'^pass_changed/$', account_views.password_change_view_done_c.as_view(template_name='pass_changed.html'),
    name='pass_changed'),
url(r'^pass_reset/$', account_views.password_reset_view_c.as_view(template_name='pass_reset.html'),
    name='pass_reset'),
url(r'^pass_reset/done/$'
    , account_views.password_reset_done_view_c.as_view(template_name='pass_reset_done.html'), name='pass_reset_done'),
url(r'^pass_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$'
    , account_views.password_reset_confirm_view_c.as_view(template_name='pass_reset_confirm.html'),
    name='pass_reset_confirm'),
url(r'^pass_reset/complete/$'
    , account_views.password_reset_complete_view_c.as_view(template_name='pass_reset_complete.html'),
    name='pass_reset_complete'),
]