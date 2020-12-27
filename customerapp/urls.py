from django.conf.urls import url

from .views import *

app_name = 'customer_app'

urlpatterns = [
    url(r'^available_products/$', GetBakeryAvailableProductsView.as_view(), name='available_products'),
    url(r'^add_address/$', CreateAddressDetailsView.as_view(), name='add_address'),
    url(r'^get_address/$', GetAddressesView.as_view(), name='get_address'),
    url(r'^place_order/$', PlaceOrderview.as_view(), name='place_order'),
    url(r'^order_bill/$', GetOrderBillView.as_view(), name='order_bill'),
]