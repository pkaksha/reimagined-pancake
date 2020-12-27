# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class AddIngredientView(APIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = AddIngredientSerializer
    permission_classes = [
        IsAdminUser,
        TokenHasReadWriteScope,
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():

            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class AddItemInventoryView(APIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = AddInventoryItemSerializer
    permission_classes = [
        IsAdminUser,
        TokenHasReadWriteScope,
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():

            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateItemInventoryView(generics.UpdateAPIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = UpdateInventorySerializer
    permission_classes = [
        IsAdminUser,
        TokenHasReadWriteScope,
    ]

    queryset = IngredientInventoryModel.objects.all()


class CookItemView(APIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = CookItemSerializer
    permission_classes = [
        IsAdminUser,
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


class GetBakeryItemView(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = GetBakeryItemSerializer
    permission_classes = [
        IsAdminUser,
        TokenHasReadWriteScope,
    ]

    def get_queryset(self):
        queryset = BakeryItems.objects.values('Bakery_Item_Name', 'IngredientComposition', 'Item_quantity',
                                              'Cost_price', 'Sell_price')
        df = pd.DataFrame(queryset)
        df = df.to_dict(orient='records')

        return df


# BONUS POINT 2
# GET HOT SELLING/POPULAR ITEMS
class GetPopularItemView(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication]
    serializer_class = GetPopularItemSerializer
    permission_classes = [
        IsAdminUser,
        TokenHasReadWriteScope,
    ]

    def get_queryset(self):
        queryset = BakeryItems.objects.values('Bakery_Item_Name', 'Sold_count')
        df = pd.DataFrame(queryset)
        df_top_3 = df.nlargest(3, 'Sold_count')
        df_top_3 = df_top_3.to_dict(orient='records')

        return df_top_3