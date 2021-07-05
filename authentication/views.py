from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from rest_framework import (
    generics, permissions, authentication, response, status, mixins
)
from .serializers import (
    CreateUserSerializer,
    ReterieveUpdateDeleteUserSerializer,
)


User = get_user_model()


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user != AnonymousUser()

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.filter(groups__name='Buyers')
    serializer_class = CreateUserSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.get(user=serializer.instance)
        return_data = serializer.data
        return_data['token'] = token.key
        return response.Response(return_data, status=status.HTTP_201_CREATED, headers=headers)


class ReterieveUpdateDeleteUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(groups__name='Buyers')
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    serializer_class = ReterieveUpdateDeleteUserSerializer
    lookup_field = 'username'
    permission_classes = [
        IsOwner,  # so that only users access only his data
        permissions.IsAuthenticated,
    ]
