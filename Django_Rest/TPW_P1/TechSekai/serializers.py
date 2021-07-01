from django.core.validators import RegexValidator

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


class UpdateProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    gender = serializers.ChoiceField(label="Gender", choices=GENDER, required=False, allow_null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = serializers.IntegerField(validators=[phone_regex], label="Contact", required=False,allow_null=True)
    age = serializers.IntegerField(required=False,allow_null=True)
    avatar = serializers.ImageField(required=False)


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
        read_only_fields = ['id']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    creator = ShopSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'image']

    def create(self, cat, brand, creator):
        name = self.validated_data['name']
        details = self.validated_data['details']
        reference_number = self.validated_data['reference_number']
        warehouse = self.validated_data['warehouse']
        lowest_price = self.validated_data['lowest_price']
        prod = Product.objects.create(category=cat,brand=brand,image='images/logo.png',creator=creator,reference_number=reference_number,name=name, details=details,warehouse=warehouse,qty_sold=0,lowest_price=lowest_price)
        return prod

    def update(self, instance,brand,cat):
        instance.brand = brand
        instance.category = cat
        instance.name = self.validated_data['name']
        instance.details = self.validated_data['details']
        instance.reference_number = self.validated_data['reference_number']
        instance.warehouse = self.validated_data['warehouse']
        instance.qty_sold = self.validated_data['qty_sold']
        instance.lowest_price = self.validated_data['lowest_price']

        return instance.save()


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, prod, shop):
        item = Item.objects.create(price=self.validated_data['price'], stock=self.validated_data['stock'],product=prod ,shop=shop )
        return item

    def update(self, instance):
        instance.price = self.validated_data['price']
        instance.stock = self.validated_data['stock']
        instance.save()


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    cart = CartSerializer()
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
