# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import requests
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


# Create your views here.


class UserCreateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [
        AllowAny
    ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(APIView):
    serializer_class = UserActivationSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def get_queryset(request):
        uid = force_text(urlsafe_base64_decode(request['uid']))
        user = UserProfileModel.objects.get(pk=uid)
        return user

    def post(self, request):

        post_data = {
            'uid': request.data['uid'],
            'token': request.data['token'].split("/")[0],
            'password': request.data['password']
        }

        serializer = self.serializer_class(data=post_data,
                                           context={'request': request})
        # print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            data = UserDetailsSerializer(self.get_queryset(post_data)).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def get_queryset(request):
        UserProfileModel.objects.filter(username=request['username']).update(last_login=datetime.datetime.now())

        user_data = UserProfileModel.objects.get(username=request['username'])
        return user_data

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user_data = UserDetailsSerializer(self.get_queryset(request.data)).data
            r = requests.post(
                settings.BASE_URL + 'o/token/',
                data={
                    'grant_type': 'password',
                    'username': data['username'],
                    'password': data['password'],
                    'client_id': settings.CLIENT_ID,
                    'client_secret': settings.CLIENT_SECRET,
                },
                )
            print("status_code", r.status_code)
            # print("data",r.json())
            # if r.status_code == 200:
            if r.status_code == 200:
                return_data = r.json()
                return_data['user_info'] = user_data
                return Response(return_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

