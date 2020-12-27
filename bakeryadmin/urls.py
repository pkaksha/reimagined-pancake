from django.conf.urls import url

from .views import *

app_name = 'bakeryadmin_app'

urlpatterns = [
    url(r'^add_ingredient/$', AddIngredientView.as_view(), name='add_ingredient'),
    url(r'^inventory_add/$', AddItemInventoryView.as_view(), name='inventory_add'),
    url(r'^inventory_update/(?P<pk>\d+)/$', UpdateItemInventoryView.as_view(), name='inventory_update'),
    url(r'^bakeryitemcook/$', CookItemView.as_view(), name='bakeryitemcook'),
    url(r'^bakeryitemget/$', GetBakeryItemView.as_view(), name='bakeryitemget'),
    url(r'^getpopularproducts/$', GetPopularItemView.as_view(), name='getpopularproducts'),

]
