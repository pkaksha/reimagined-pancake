"""bakeryapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^o/', include(('oauth2_provider.urls', 'oauth2_provider'), namespace='oauth2_provider')),
    url(r'^api/', include(('registerlogin.urls', 'registerlogin_app'), namespace='registerlogin_app')),
    url(r'^api/', include(('bakeryadmin.urls', 'bakeryadmin_app'), namespace='bakeryadmin_app')),
    url(r'^api/', include(('customerapp.urls', 'customerapp_app'), namespace='customerapp_app')),

]
