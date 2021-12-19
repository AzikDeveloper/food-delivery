from rest_framework.serializers import ValidationError, ModelSerializer, SerializerMethodField, CharField
from .models import Product, Category, Order, SubOrder, Banner, Filial, Address, About, Contact
from site_auth.models import User
from django.core.exceptions import BadRequest
from django.contrib.auth import password_validation
from rest_framework.response import Response


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'photo', 'description', 'price', 'category']


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'home_number', 'street', 'district', 'lat', 'long']


class UserSerializer(ModelSerializer):
    phone_number = CharField(source='username')
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'address', 'username']
        extra_kwargs = {'username': {'write_only': True}}


class SubOrderSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SubOrder
        fields = ['id', 'product', 'quantity']


class CreateSubOrderSerializer(ModelSerializer):
    class Meta:
        model = SubOrder
        fields = ['id', 'product', 'quantity']


class OrderSerializer(ModelSerializer):
    receiver = UserSerializer()
    suborders = SubOrderSerializer(many=True)
    address = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'receiver', 'address', 'suborders', 'accepted', 'date_created']

    def get_address(self, order):
        if order.address:
            address = AddressSerializer(order.address)
        else:
            address = AddressSerializer(order.receiver.address)
        return address.data


class CreateAddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'home_number', 'street', 'district', 'lat', 'long']


class CreateOrderSerializer(ModelSerializer):
    address = CreateAddressSerializer()
    suborders = CreateSubOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'receiver', 'address', 'suborders', 'accepted', 'date_created']

    def create(self, validated_data):
        address = Address.objects.create(**validated_data.pop('address'))
        suborder_serializer = CreateSubOrderSerializer(data=self.initial_data.get('suborders'), many=True)
        if suborder_serializer.is_valid():
            suborders = suborder_serializer.save()
        else:
            raise BadRequest
        order = Order.objects.create(
            receiver=validated_data.pop('receiver'),
            address=address
        )
        order.suborders.set(suborders)
        order.save()
        return order


class MyOrderSerializer(ModelSerializer):
    suborders = SubOrderSerializer(many=True)
    address = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'address', 'suborders', 'accepted', 'date_created']

    def get_address(self, order):
        if order.address:
            address = AddressSerializer(order.address)
        else:
            address = AddressSerializer(order.receiver.address)
        return address.data


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'name', 'photo']


class FilialSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Filial
        fields = ['id', 'name', 'open_times', 'phone_number', 'address', 'orienter']

    def create(self, validated_data):
        address = Address.objects.create(**validated_data.get('address'))
        validated_data['address'] = address
        filial = Filial.objects.create(**validated_data)
        return filial

    def update(self, instance: Filial, validated_data):
        if 'address' in validated_data:
            address = instance.address
            serializer = AddressSerializer(instance=address, data=validated_data.get('address'), partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                raise BadRequest
            validated_data.pop('address')
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance


class AboutSerializer(ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'title', 'banner', 'context']


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'title', 'address']
