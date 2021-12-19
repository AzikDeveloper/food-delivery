from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('confirm-register', views.RegisterConfirmView.as_view()),
    path('login', views.LoginView.as_view()),
    path('confirm-login', views.LoginConfirmView.as_view()),

    path('banners', views.BannerView.as_view()),
    path('banners/<int:pk>', views.BannerDetailView.as_view()),

    path('products', views.ProductView.as_view()),
    path('products/<int:pk>', views.ProductDetailView.as_view()),

    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),

    path('categories', views.CategoryView.as_view()),
    path('categories/<int:pk>', views.CategoryDetailView.as_view()),

    path('users', views.UserView.as_view()),
    path('users/<int:pk>', views.UserDetailView.as_view()),
    path('users/me', views.UserMeView.as_view()),
    path('users/me/orders', views.MyOrdersView.as_view()),

    path('company/filials', views.FilialView.as_view()),
    path('company/filials/<int:pk>', views.FilialDetailView.as_view()),

    path('company/about', views.AboutView.as_view()),
    path('company/about/<int:pk>', views.AboutDetailView.as_view()),

    path('company/contacts', views.ContactView.as_view()),
    path('company/contacts/<int:pk>', views.ContactDetailView.as_view())

]

urlpatterns += [
    path('swagger', TemplateView.as_view(template_name='api/swagger-ui.html',
                                         extra_context={'schema_url': 'openapi-schema'}
                                         ), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Metsenat",
        description="API for students contract sponsorship",
        version="1.0.0"
    ), name='openapi-schema'),
]
