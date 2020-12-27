from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from .activation_token import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import *


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'phone_number', 'role_type']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    role_type = serializers.CharField(required=True)

    class Meta:
        model = UserProfileModel
        fields = ['password', 'is_superuser', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'phone_number', 'role_type', 'activation_link',
                  'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_active'] = False
        if validated_data['role_type'] == 'bakery_admin':
            validated_data['is_superuser'] = True
            validated_data['is_staff'] = True

        user = UserProfileModel.objects.create(**validated_data)
        domain = settings.DOMAIN
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        user.activation_link = '%s/?uidb64=%s&token=%s/' % (domain, uid,
                                                            token)
        UserProfileModel.objects.filter(
            username=validated_data['username']).update(activation_link=user.activation_link)

        try:
            mail_subject = 'Activate your ZBaked account.'
            message = render_to_string(
                'account_activate.html', {
                    'user': user,
                    'domain': settings.DOMAIN,
                    'uid': uid,
                    'token': token,
                    # 'activation_link': user.activation_link
                })
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
            return {"Response":"User Created, Please check your email for Account Activation Instruction"}
        except Exception as e:
            print(str(e))


class UserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        try:
            uid = force_text(urlsafe_base64_decode(validated_data['uid']))
            user = UserProfileModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                UserProfileModel.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(
                user, validated_data['token']):
            UserProfileModel.objects.filter(pk=uid).update(
                is_active=True,
                password=make_password(validated_data['password']))
            return validated_data
        else:
            raise serializers.ValidationError(0)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
