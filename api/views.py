from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from .models import Product, Order, Category, Banner
from .serializers import ProductSerializer, OrderSerializer, CategorySerializer, BannerSerializer
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, FieldError
from math import ceil


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homeView(request):
    return Response({'ok': True})


@api_view(['GET'])
def productsView(request):
    page = 1
    per_page = 200
    order_list = []
    products = Product.objects.all()

    query = request.GET

    if 'sort' in query:
        for attr in query['sort'].split(','):
            order_list.append(attr.replace('-', '__'))
    if 'page' in query:
        if query['page'].isdigit():
            page = int(query['page'])
    if 'per_page' in query:
        if query['per_page'].isdigit():
            per_page = int(query['per_page'])

    try:
        products = products.order_by(*order_list)
    except FieldError:
        return Response(data={'detail': 'failed to process &sort= parameter'}, status=400)
    paginator = Paginator(products, per_page)
    num_pages = paginator.num_pages

    if page <= num_pages:
        products = paginator.page(page)
    else:
        page = num_pages
        products = paginator.page(num_pages)

    product_serializer = ProductSerializer(products, many=True)

    data = {
        'pagination': {
            'page': page,
            'per_page': per_page,
            'num_pages': num_pages
        },
        'products': product_serializer.data
    }
    if 'exclude' in query:
        for attr in query['exclude'].split(','):
            if attr in data:
                data.pop(attr)

    return Response(data=data)


@api_view(['GET'])
def productView(request, p_id):
    product = Product.objects.get(id=p_id)
    serializer = ProductSerializer(product)

    return Response(data=serializer.data)


@api_view(['GET'])
def ordersView(request):
    orders = Order.objects.all()
    order_serializer = OrderSerializer(orders, many=True)
    return Response(data=order_serializer.data)


@api_view(['GET'])
def categoriesView(request):
    categories = Category.objects.all()
    category_serializer = CategorySerializer(categories, many=True)
    return Response(data=category_serializer.data)


@api_view(['GET'])
def bannersView(request):
    banners = Banner.objects.all()
    banner_serializer = BannerSerializer(banners, many=True)
    return Response(data=banner_serializer.data)


@api_view(['GET'])
def productsByCategoryView(request, cat_id):
    try:
        category = Category.objects.get(id=cat_id)
    except ObjectDoesNotExist:
        return Response(data={
            'ok': False,
            'detail': 'category not found'
        }, status=404)
    products_in_category = category.products.all()
    product_serializer = ProductSerializer(products_in_category, many=True)
    return Response(data=product_serializer.data)
