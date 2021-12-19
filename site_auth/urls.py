from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import logoutView

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('api-token', obtain_auth_token, name='api_token_auth'),
    path('logout', logoutView),
    path('swagger', schema_view)
]
