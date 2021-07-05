from django.conf import settings
from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

User = get_user_model()

# serializer for data creating user


class CreateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[UnicodeUsernameValidator(), ]
    )
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(
        style={
            'input_type': 'password',
        },
        write_only=True
    )

    def create(self, validated_data):
        # create method for saving data and encrypted password
        try:
            user = User.objects.create_user(**validated_data)
            user.groups.add(Group.objects.get_or_create(name='Buyers')[0].id)
            user.save()
            return user
        except IntegrityError:
            try:
                user = User.objects.get(
                    email=validated_data.get('email')
                )
                raise exceptions.ValidationError(
                    {'detail': 'user with email already exist, please try login'}
                )
            except User.DoesNotExist:
                pass
            try:
                user = User.objects.get(
                    username=validated_data.get('username')
                )
                raise exceptions.ValidationError(
                    {'detail': 'user with this username alreday exist, please choose diffrent username'}
                )
            except User.DoesNotExist:
                pass

# get user data


class ReterieveUpdateDeleteUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[UnicodeUsernameValidator(), ]
    )
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_active = serializers.BooleanField()

    def update(self, instance, validated_data):
        # update method for updating user model
        try:
            instance.username = validated_data.get('username')
            instance.email = validated_data.get('email')
            instance.first_name = validated_data.get('first_name')
            instance.last_name = validated_data.get('last_name')
            instance.is_active = validated_data.get('is_active')
            instance.save()
            return instance
        except IntegrityError:
            if User.objects.get(email=validated_data.get('email')):
                raise exceptions.ValidationError(
                    {'detail': 'user with email already exist, please enter correct email'}
                )
            elif User.objects.get(username=validated_data.get('username')):
                raise exceptions.ValidationError(
                    {'detail': 'user with this username alreday exist, please choose diffrent username'}
                )

# creating auth token when any user registers


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
