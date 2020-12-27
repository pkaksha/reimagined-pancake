from django.conf.urls import url

from .views import *

app_name = 'login_app'

urlpatterns = [
    url(r'^user_create/$', UserCreateView.as_view(), name='usercreate'),
    url(r'^user_activate/$', UserActivationView.as_view(), name='useractivation'),
    url(r'^user_login/$', UserLogin.as_view(), name='userlogin'),

]