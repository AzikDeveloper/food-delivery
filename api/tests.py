# @api_view(['GET'])
# def productsView(request):
#     page = 1
#     per_page = 20
#     order_list = []
#     products = Product.objects.all()
#
#     query = request.GET
#
#     if 'sort' in query:
#         for attr in query['sort'].split(','):
#             order_list.append(attr)
#     if 'page' in query:
#         if query['page'].isdigit():
#             page = int(query['page'])
#     if 'per_page' in query:
#         if query['per_page'].isdigit():
#             per_page = int(query['per_page'])
#
#     products = products.order_by(*order_list)
#     paginator = Paginator(products, per_page)
#     num_pages = paginator.num_pages
#
#     if page <= num_pages:
#         products = paginator.page(page)
#     else:
#         page = num_pages
#         products = paginator.page(num_pages)
#
#     product_serializer = ProductSerializer(products, many=True)
#     data = {
#         'pagination': {
#             'page': page,
#             'per_page': per_page,
#             'num_pages': num_pages
#         },
#         'products': product_serializer.data
#     }
#     return Response(data=data)
