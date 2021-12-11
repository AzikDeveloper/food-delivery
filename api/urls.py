from django.urls import path
from .views import homeView, productsView, productView, ordersView, categoriesView, bannersView, productsByCategoryView, \
    FilialsView, FilialView, UsersView, UserView, UsersMeView, AboutView, ContactsView, RegisterView, \
    RegisterConfirmView, LoginView, LoginConfirmView

urlpatterns = [
    path('test', homeView),

    path('register', RegisterView.as_view()),
    path('confirm-register', RegisterConfirmView.as_view()),
    path('login', LoginView.as_view()),
    path('confirm-login', LoginConfirmView.as_view()),

    path('banners', bannersView),
    path('products', productsView),
    path('products/<int:p_id>', productView),
    path('orders', ordersView),
    path('categories', categoriesView),
    path('categories/<int:cat_id>/products', productsByCategoryView),
    path('users', UsersView.as_view()),
    path('users/<int:user_id>', UserView.as_view()),
    path('users/me', UsersMeView.as_view()),
    path('company/filials', FilialsView.as_view()),
    path('company/filials/<int:filial_id>', FilialView.as_view()),
    path('company/about', AboutView.as_view()),
    path('company/contacts', ContactsView.as_view())
]
