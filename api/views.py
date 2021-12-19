from copy import copy
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from site_auth.models import SMSCode
from site_auth.permissions import IsAdminUser, IsAdminOrCreateOnly, IsAdminOrGetOnly
from .serializers import *
from .models import *
from .tools import SMS
from rest_framework import generics


class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrCreateOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        request.data['receiver_id'] = request.user.id
        return self.create(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class MyOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(receiver=self.request.user)
        return queryset


class CategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrGetOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BannerView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class BannerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Banner
    serializer_class = BannerSerializer


class FilialView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer


class FilialDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer


class UserView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        if self.get_object() == request.user:
            return self.update(request, *args, **kwargs)


class UserMeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AboutView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class AboutDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class ContactView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrGetOnly]
    queryset = Contact
    serializer_class = ContactSerializer


class RegisterView(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        print(phone_number)
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
