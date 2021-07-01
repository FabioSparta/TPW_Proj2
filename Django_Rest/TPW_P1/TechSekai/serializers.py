from TechSekai.models import *
from rest_framework import serializers
from django.contrib.auth import models as auth_models


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = auth_models.User(email=self.validated_data['email'],
                                username=self.validated_data['username'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.User
        fields = ('email', 'username', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    django_user = DjangoUserSerializer()

    class Meta:
        model = User
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    owner = DjangoUserSerializer()

    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ['id', 'owner']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', ] #'creator'
        print(Product.name)


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Item
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = Order
        fields = '__all__'
