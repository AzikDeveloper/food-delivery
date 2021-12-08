from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, Category, Order, SubOrder, Banner
from site_auth.models import User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']
        ordering_fields = ['id', 'name', 'price', 'category']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SubOrderSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SubOrder
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    receiver = UserSerializer()
    suborders = SubOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'receiver', 'location', 'suborders', 'accepted', 'date_created']


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'name', 'photo']
