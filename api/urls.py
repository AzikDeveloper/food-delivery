from django.urls import path
from .views import homeView, ProductsView, ProductDetailView, OrdersView, MyOrdersView, CategoriesView, BannersView, \
    ProductsByCategoryView, \
    FilialsView, FilialDetailView, UsersView, UserView, UsersMeView, AboutView, ContactsView, RegisterView, \
    RegisterConfirmView, LoginView, LoginConfirmView

urlpatterns = [
    path('test', homeView),

    path('register', RegisterView.as_view()),
    path('confirm-register', RegisterConfirmView.as_view()),
    path('login', LoginView.as_view()),
    path('confirm-login', LoginConfirmView.as_view()),

    path('banners', BannersView.as_view()),
    path('products', ProductsView.as_view()),
    path('products/<int:p_id>', ProductDetailView.as_view()),
    path('orders', OrdersView.as_view()),
    path('categories', CategoriesView.as_view()),
    path('categories/<int:cat_id>/products', ProductsByCategoryView.as_view()),
    path('users', UsersView.as_view()),
    path('users/<int:user_id>', UserView.as_view()),
    path('users/me', UsersMeView.as_view()),
    path('users/me/orders', MyOrdersView.as_view()),
    path('company/filials', FilialsView.as_view()),
    path('company/filials/<int:filial_id>', FilialDetailView.as_view()),
    path('company/about', AboutView.as_view()),
    path('company/contacts', ContactsView.as_view())
]
