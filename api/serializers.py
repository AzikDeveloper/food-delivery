from rest_framework import serializers
from .models import Product, Category, Order, SubOrder, Banner, Filial, Address, About, Contact
from site_auth.models import User
from rest_framework.validators import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'photo', 'description', 'price', 'category', 'category_id']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'home_number', 'street', 'district', 'lat', 'long']


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='username')
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'address', 'username']
        extra_kwargs = {'username': {'write_only': True}}

    def update(self, instance, validated_data):
        address = validated_data.pop('address')
        address_serializer = AddressSerializer(data=address)
        if address_serializer.is_valid():
            address = address_serializer.save()
            if instance.address:
                instance.address.delete()
            instance.address = address
            instance.save()
            return instance
        else:
            raise ValidationError({'address': 'address is not valid'})


class SubOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SubOrder
        fields = ['id', 'product', 'quantity', 'product_id']


class OrderSerializer(serializers.ModelSerializer):
    receiver = UserSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    suborders = SubOrderSerializer(many=True)
    address = AddressSerializer(source='receiver.address', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'receiver', 'receiver_id', 'address', 'suborders', 'accepted', 'date_created']

    def create(self, validated_data):
        suborders_serializer = SubOrderSerializer(data=validated_data.pop('suborders'), many=True)
        if suborders_serializer.is_valid():
            suborders = suborders_serializer.save()
        else:
            return ValidationError({'suborders': 'invalid suborders'})
        order = Order.objects.create(**validated_data)
        order.suborders.set(suborders)
        order.save()
        return order


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'name', 'photo']


class FilialSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Filial
        fields = ['id', 'name', 'open_times', 'phone_number', 'address', 'orienter']


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'title', 'banner', 'context']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'title', 'address']
