from django.urls import path
from .views import CreateUser, ReterieveUpdateDeleteUser
from rest_framework.authtoken import views

class Token(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    # for creating user api end point url register
    path('auth/', CreateUser.as_view()),
    # api-end point for get user data
    path('auth/<str:username>/', ReterieveUpdateDeleteUser.as_view()),
    path('auth-token/', Token.as_view()),  # api end point for login
]
