# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class GetBakeryAvailableProductsView(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = GetBakeryAvailableProductsSerializer
    permission_classes = [
        IsAuthenticated,
        TokenHasReadWriteScope,
    ]

    def get_queryset(self):
        queryset = BakeryItems.objects.filter(Item_quantity__gte=1).values('Bakery_Item_Name', 'Item_quantity',
                                                                           'Sell_price')
        print(queryset)

        df = pd.DataFrame(queryset)
        df = df.to_dict(orient='records')

        return df


class CreateAddressDetailsView(APIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = CreateAddressDetailsSerializer
    permission_classes = [
        IsAuthenticated,
        TokenHasReadWriteScope,
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            data = serializer.save()

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class GetAddressesView(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = GetAddressSerializer
    permission_classes = [
        IsAuthenticated,
        TokenHasReadWriteScope,
    ]

    def get_queryset(self):
        cust_id = self.request.query_params.get("cust_id")
        queryset = CustomerAddressDetails.objects.filter(cust_id=cust_id).values('Street_Address', 'City', 'Pincode',
                                                                                 'State',
                                                                                 'phone_number', 'address_type')
        df = pd.DataFrame(queryset)
        df = df.to_dict(orient='records')

        return df


class PlaceOrderview(APIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = PlaceOrderSerializer
    permission_classes = [
        IsAuthenticated,
        TokenHasReadWriteScope,
    ]

    def post(self, request):

        print(request.data)

        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():

            data = serializer.save()

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class GetOrderBillView(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = GetOrderBillSerializer
    permission_classes = [
        IsAuthenticated,
        TokenHasReadWriteScope,
    ]

    # queryset = OrderParticularsModel.objects.all()

    def get_queryset(self):
        order_no = self.request.query_params.get("order_no")
        queryset = OrderParticularsModel.objects.filter(order_no=order_no).values('created', 'address_id', 'order_no',
                                                                                  'cust_id', 'Bakery_item_id',
                                                                                  'Ordered_Quantity', 'Total')

        bakery_item_id = [x['Bakery_item_id'] for x in queryset]
        address_id = [x['address_id'] for x in queryset]
        cust_id = [x['cust_id'] for x in queryset]

        print(bakery_item_id)
        print(address_id)
        print(cust_id)

        customer_first_name = list(UserProfileModel.objects.filter(id__in=cust_id).values('first_name'))[0][
            'first_name']
        customer_last_name = list(UserProfileModel.objects.filter(id__in=cust_id).values('last_name'))[0]['last_name']
        customer_phone_number = list(UserProfileModel.objects.filter(id__in=cust_id).values('phone_number'))[0][
            'phone_number']

        bakery_bakery_item_name = list(BakeryItems.objects.filter(id__in=bakery_item_id).values(
            'Bakery_Item_Name'))[0]['Bakery_Item_Name']

        address_street_address = list(CustomerAddressDetails.objects.filter(id__in=address_id).values(
            'Street_Address'))[0]['Street_Address']
        address_city = list(CustomerAddressDetails.objects.filter(id__in=address_id).values('City'))[0]['City']
        address_pincode = list(CustomerAddressDetails.objects.filter(id__in=address_id).values('Pincode'))[0]['Pincode']
        address_state = list(CustomerAddressDetails.objects.filter(id__in=address_id).values('State'))[0]['State']

        df = pd.DataFrame(queryset)

        df['first_name'] = customer_first_name
        df['last_name'] = customer_last_name
        df['phone_number'] = customer_phone_number
        df['Bakery_Item_Name'] = bakery_bakery_item_name
        df['Street_Address'] = address_street_address
        df['City'] = address_city
        df['Pincode'] = address_pincode
        df['State'] = address_state
        df['Total_Amount'] = (df['Total'].sum()).round(1)

        print(df)
        df = df.to_dict(orient='records')

        return df
