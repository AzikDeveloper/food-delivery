
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings


def redirect_to_admin(request):
    return redirect('admin')


urlpatterns = [
    path('', redirect_to_admin),
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include('api.urls')),
    path('auth/', include('site_auth.urls'))
]
