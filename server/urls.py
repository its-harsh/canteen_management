from django.contrib import admin  # importing admin for prebuilt adminitration urls
from django.urls import path, include
from django.shortcuts import redirect
from modelapp.views import showorders

def redirect_home(request):
    # redirect homepage to api/show/
    return redirect('admin/login/?next=/show/', permanent=True)


urlpatterns = [
    # registering admin prebuilt urls
    path('admin/', admin.site.urls),
    # registering authentication api
    path('api-auth/', include('authentication.urls')),
    # registering food ordering api
    path('api/', include('modelapp.urls')),
    path('', redirect_home),
    path('show/', showorders),  # for getting all order to be prepared by chef
]
