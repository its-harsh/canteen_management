from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import generics, permissions, authentication, pagination
from .models import Food, TotalFoodOrder, UserFoodOrder, UserOrder
from .serializers import ListFoodSerializer, GetUserOrderSerializer, CreateUserOrderSerializer

# api for listing all food items available


class ListFood(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = ListFoodSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

# api for getting ordered food data


class RetereiveUserOrder(generics.RetrieveAPIView):
    queryset = UserOrder.objects.all()
    serializer_class = GetUserOrderSerializer
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]

# creating api for ordering food


class CreateUserOrder(generics.CreateAPIView):
    queryset = UserOrder.objects.all()
    serializer_class = CreateUserOrderSerializer
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]

# this decorator says so that login is required for show all orders
# this says that only staff of canteen can login


@login_required
@user_passes_test(lambda user_: user_.is_staff)
def showorders(request):
    return render(request, 'index.html', {'orders': TotalFoodOrder.objects.all()})
