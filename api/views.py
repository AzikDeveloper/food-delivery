from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from .models import Product, Order, Category, Banner, Filial, About, Contact
from site_auth.models import User, SMSCode
from site_auth.permissions import IsAdmin, IsAdminOrCreateOnly
from .serializers import ProductSerializer, OrderSerializer, CreateOrderSerializer, AddressSerializer, \
    SubOrderSerializer, \
    CreateSubOrderSerializer, MyOrderSerializer, \
    CategorySerializer, \
    BannerSerializer, \
    UserSerializer, \
    FilialSerializer, AboutSerializer, ContactSerializer
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from math import ceil
from .tools import SMS
from rest_framework import generics


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homeView(request):
    return Response({'detail': 'congrats'})


class ProductView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product
    serializer_class = ProductSerializer


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [IsAuthenticated]
    queryset = Order
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        request.data['receiver'] = request.user
        return self.create(request, *args, **kwargs)


class MyOrdersView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(receiver=self.request.user)
        return queryset


class CategoryView(generics.ListCreateAPIView):
    queryset = Category
    serializer_class = CategorySerializer


class BannersView(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        banner_serializer = BannerSerializer(banners, many=True)
        return Response(data=banner_serializer.data)


class ProductsByCategoryView(APIView):
    def get(self, request, cat_id):
        category = get_object_or_404(Category, id=cat_id)
        products_in_category = category.products.all()
        serializer = ProductSerializer(products_in_category, many=True)
        return Response(data=serializer.data)


class FilialsView(APIView):
    def get(self, request):
        filials = Filial.objects.all()
        serializer = FilialSerializer(filials, many=True)
        return Response(data=serializer.data)

    def post(self, request):
        serializer = FilialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data={
                'detail': 'Failed to create filial'
            }, status=400)

    def delete(self, request):
        Filial.objects.all().delete()
        return Response(data={
            'detail': 'Filials are deleted'
        })


class FilialDetailView(APIView):
    def get(self, request, filial_id):
        filial = get_object_or_404(Filial, id=filial_id)
        serializer = FilialSerializer(filial)
        return Response(serializer.data)

    def put(self, request, filial_id):
        filial = get_object_or_404(Filial, id=filial_id)
        serializer = FilialSerializer(instance=filial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data={
                'detail': 'Failed to update the filial!'
            }, status=400)

    def delete(self, request, filial_id):
        filial = get_object_or_404(Filial, id=filial_id)
        filial.delete()
        return Response(status=200)


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response()


class UsersMeView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class AboutView(APIView):
    def get(self, request):
        about = About.objects.first()
        serializer = AboutSerializer(about)
        return Response(data=serializer.data)


class ContactsView(AboutView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(data=serializer.data)


class RegisterView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user = User.objects.filter(username=phone_number)
        if not user:
            sms = SMS(phone_number)
            while True:
                sms_code, created = SMSCode.objects.get_or_create(code=sms.code,
                                                                  defaults={'phone_number': phone_number})
                if not created:
                    if sms_code.is_expired():
                        sms_code.delete()
                    else:
                        sms.generate_code()
                else:
                    sms.send_sms()
                    break

            return Response(status=200)
        else:
            return Response(status=409)


class RegisterConfirmView(APIView):
    def post(self, request):
        code = request.data.get('code')
        phone_number = request.data.get('phone_number')

        sms_code = SMSCode.objects.filter(code=code, phone_number=phone_number)
        if sms_code:
            if sms_code.last().is_expired():
                sms_code.delete()
                return Response(status=410)
            user = User.objects.filter(username=phone_number)
            if not user:
                user = User.objects.create_user(
                    username=sms_code[0].phone_number,
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name')
                )
                token = Token.objects.create(user=user)
                serializer = UserSerializer(user)
                response = serializer.data
                response['token'] = token.key

                sms_code[0].delete()
                return Response(data=response)
            else:
                return Response(status=400)
        return Response(status=400)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        user = User.objects.filter(username=phone_number)
        if user:
            sms = SMS(phone_number)
            while True:
                sms_code, created = SMSCode.objects.get_or_create(code=sms.code,
                                                                  defaults={'phone_number': phone_number,
                                                                            'code': sms.code})
                if not created:
                    if sms_code.is_expired():
                        sms_code.delete()
                    else:
                        sms.generate_code()
                else:
                    print(sms_code.phone_number, sms_code.code)
                    sms.send_sms()
                    break

            return Response(status=200)
        else:
            return Response(status=401)


class LoginConfirmView(APIView):
    def post(self, request):
        code = request.data.get('code')
        phone_number = request.data.get('phone_number')

        sms_code = SMSCode.objects.filter(code=code, phone_number=phone_number)
        if sms_code:
            if sms_code.last().is_expired():
                sms_code.delete()
                return Response(status=410)

            user = User.objects.filter(username=phone_number)
            if user:
                token, created = Token.objects.get_or_create(user=user[0])
                serializer = UserSerializer(user[0])
                response = serializer.data
                response['token'] = token.key

                sms_code[0].delete()
                return Response(data=response)
            return Response(status=404)
        return Response(status=400)
