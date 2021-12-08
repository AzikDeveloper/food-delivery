from django.urls import path
from .views import homeView, productsView, productView, ordersView, categoriesView, bannersView, productsByCategoryView, \
    createUserView

urlpatterns = [
    path('test', homeView),
    path('banners', bannersView),
    path('products', productsView),
    path('products/<int:p_id>', productView),
    path('orders', ordersView),
    path('categories', categoriesView),
    path('categories/<int:cat_id>/products', productsByCategoryView),
    path('users', createUserView)
]
