from django.urls import path
from .views import ListFood, RetereiveUserOrder, CreateUserOrder, showorders

urlpatterns = [
    path('', ListFood.as_view()),
    # for getting user order
    path('user_order/<int:pk>/', RetereiveUserOrder.as_view()),
    path('user_order/order/', CreateUserOrder.as_view()),  # for creating order
]
