from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from TechSekai.forms import *
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from allauth.account.views import SignupView
import json

# Imports for Django
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from TechSekai.serializers import *
######################


global_products = []


# ########################################### REST ENDPOINTS ###########################################################

# GENERAL USE ENDPOINTS

@api_view(['GET'])
def get_prods_hotdeals(request):
    products = Product.objects.all().order_by("-qty_sold")[0:10]  # Only {10} most sold
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_prods_newarrivals(request):
    products = Product.objects.all().order_by("id")[0:10]  # Only {10} most recent
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# CLIENT USER ENDPOINTS

@api_view(['POST'])
def sign_up(request):
    serializer = RegistrationSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        # Save DjangoAuth User
        django_user = serializer.save()

        # Save App User
        user = User()
        user.django_user = django_user
        cart = Cart(user=user)
        wishlist = WishList(user=user)
        user.save()
        cart.save()
        wishlist.save()

        # Gen Response
        data = {'response': "Successfully registered the new user.", 'email': user.django_user.email,
                'username': user.django_user.username, 'token': Token.objects.get(user=django_user).key}

        return Response(data, status.HTTP_201_CREATED)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request):
    isShop = request.user.groups.filter(name='shops').exists()
    return Response({'isShop': isShop , 'username' : request.user.username, 'userId':request.user.id}
                    , status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = User.objects.get(django_user=request.user)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    serializer = UpdateProfileSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(django_user=request.user)
        user.django_user.email = serializer.data.get('email')
        user.django_user.username = serializer.data.get('username')
        print(serializer.data)
        if serializer.data.get('gender') is not None:
            user.gender = serializer.data.get('gender')
        if serializer.data.get('phone_number') is not None:
            user.phone_number = serializer.data.get('phone_number')
        if serializer.data.get('first_name') is not None:
            user.django_user.first_name = serializer.data.get('first_name')
        if serializer.data.get('last_name') is not None:
            user.django_user.last_name = serializer.data.get('last_name')
        if serializer.data.get('age') is not None:
            user.age = serializer.data.get('age')

        user.django_user.save()
        user.save()
        print(user.django_user.first_name)

        return Response("Updated successfully", status=status.HTTP_200_OK)

    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    user = User.objects.get(django_user=request.user)
    orders = Order.objects.all().filter(user=user)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_address_add(request):
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        print("valid address!")
        user = User.objects.get(django_user=request.user)
        serializer.save()
        user.address = json.loads(json.dumps(serializer.data), object_hook=lambda d: Address(**d))
        user.save()
        return Response("Address added successfully.", status=status.HTTP_201_CREATED)

    print(serializer.errors)
    print("aaaaa")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_address_update(request):
    user = User.objects.get(django_user=request.user)

    if user.address is None:
        return Response("This User does not have an address yet. ", status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(user.address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response("Address updated successfully.", status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_address_rem(request):
    user = User.objects.get(django_user=request.user)

    if user.address is not None:
        user.address.delete()
        return Response("Address removed successfully.", status=status.HTTP_204_NO_CONTENT)

    return Response("This User does not have an address yet. ", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user = User.objects.get(django_user=request.user)
    cart_user = Cart.objects.get(user=user)
    cart_items = Cart_Item.objects.filter(cart=cart_user).order_by('id')
    serializer = CartItemSerializer(cart_items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    user = User.objects.get(django_user=request.user)
    user_wishlist = WishList.objects.get(user=user)
    wishlist_items = user_wishlist.prods.all()
    serializer = ProductSerializer(wishlist_items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_add(request):
    print("called")
    # Check if product exists
    try:
        prod = Product.objects.get(id=request.data['prod_id'])
    except Product.DoesNotExist:
        return Response("The product with id=" + request.data['prod_id'] + " does not exist.",
                        status.HTTP_404_NOT_FOUND)

    # Save Product in Wishlist
    user = User.objects.get(django_user=request.user)
    user_wishlist = WishList.objects.get(user=user)
    if prod not in user_wishlist.prods.all():
        user_wishlist.prods.add(prod)
        return Response(prod.name + " was added to your wishlist successfully.", status.HTTP_201_CREATED)

    return Response(prod.name + " is already in your wishlist.", status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def wishlist_remove(request, prod_id):
    # Check if product exists
    try:
        prod = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        return Response("The product with id=" + prod_id + " does not exist.", status.HTTP_404_NOT_FOUND)

    # Remove Product from Wishlist
    user = User.objects.get(django_user=request.user)
    user_wishlist = WishList.objects.get(user=user)
    if prod in user_wishlist.prods.all():
        user_wishlist.prods.remove(prod)
        return Response(prod.name + " was successfully removed from your wishlist.", status.HTTP_204_NO_CONTENT)

    return Response("There is no " + prod.name + " in your wishlist.", status.HTTP_200_OK)


@api_view(['GET'])
def list_categories(request):
    cats = Category.objects.all()
    serializer = CategorySerializer(cats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_brands(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_prods(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        p = Product.objects.filter(creator=loggedShop)
        if 'num' in request.GET:
            num = int(request.GET['num'])
            p = p[:num]
        serializer = ProductSerializer(p, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Must login with a shop account to list products", status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            prod = serializer.save()
            prod.creator = loggedShop

            if prod.image is None:
                prod.image = 'images/logo.png'

            if prod.brand.name == 'Other':
                new_brand = request.data.get("new_brand")
                if new_brand is not None:
                    b = Brand(name=new_brand)
                    b.save()
                    prod.brand = b
                else:
                    Product.objects.get(id=prod.id).delete()
                    return Response("New brand not created because no new_brand was defined",
                                    status=status.HTTP_400_BAD_REQUEST)

            if prod.category.name == 'Other':
                new_cat = request.data.get("new_cat")
                if new_cat is not None:
                    c = Category(name=new_cat, totDevices=1)
                    c.save()
                    prod.category = c
                else:
                    Product.objects.get(id=prod.id).delete()
                    return Response("New category not created because no new_category was defined",
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                prod.category.totDevices += 1

            try:
                price = request.data.get("price")
                i = Item(product=prod, price=price, shop=loggedShop)
                i.price = price
                i.save()
                if i.price < prod.lowest_price:
                    prod.lowest_price = i.price

            except:
                Product.objects.get(id=prod.id).delete()
                return Response("Something went wrong: check if you defined the product price",
                                status=status.HTTP_400_BAD_REQUEST)

            prod.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response("You must login with a shop account!", status=status.HTTP_403_FORBIDDEN)

# TODO: VER IMAGENS https://www.trell.se/blog/file-uploads-json-apis-django-rest-framework/


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pid):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        if Item.objects.filter(product_id=pid).count() > 1:
            return Response('You don\'t have permissions to edit this product anymore, other shops depend on it',
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            p = Product.objects.get(id=pid)
            if p.creator != loggedShop:
                return Response('You arent the creator of this product, so you can\'t edit it. ',
                                status=status.HTTP_403_FORBIDDEN)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(p, data=request.data)

        if serializer.is_valid():
            p = serializer.save()
            p.creator = loggedShop

            price = request.data.get("price")
            if price is not None:
                try:
                    i = Item.objects.get(product=p)
                    i.price = price
                    i.save()
                    if i.price < p.lowest_price:
                        p.lowest_price = i.price
                        p.save()

                except:
                    return Response("Something went wrong: product price not updated",
                                    status=status.HTTP_400_BAD_REQUEST)

            print(p.image)
            if p.image is None:
                print('hereeeeeeeeeeeeeee')
                image = 'images/logo.png'
                p.image = image
                p.save()

            if p.category.name == 'Other':
                new_cat = request.data.get("new_cat")
                if new_cat is not None:
                    c = Category(name=new_cat, totDevices=1)
                    c.save()
                    p.category = c
                    p.save()
                else:
                    return Response("New category not created because no new_category was defined",
                                    status=status.HTTP_400_BAD_REQUEST)

            if p.brand.name == 'Other':
                new_brand = request.data.get("new_brand")
                if new_brand is not None:
                    b = Brand(name=new_brand)
                    b.save()
                    p.brand = b
                    p.save()
                else:
                    return Response("New brand not created because no new_brand was defined",
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response("Must login with a shop account to edit products", status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def see_product(request, pid):
    try:
        prod = Product.objects.get(id=pid)
    except Product.DoesNotExist:
        return Response('Product not found', status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(prod)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_prod(request, pid):
    if request.user.groups.filter(name='shops').exists():
        if Item.objects.filter(product_id=pid).count() > 1:
            return Response('You don\'t have permissions to delete this product anymore, other shops depend on it. Maybe you should delete the corresponding item instead',
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        Product.objects.get(id=pid).delete()
        return Response('Product deleted successfully', status=status.HTTP_204_NO_CONTENT)
    return Response("Must login with a shop account to delete products", status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_shops_list(request):
    shops = Shop.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        shops = shops[:num]
    serializer = ShopSerializer(shops, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_shop(request, sid):
    try:
        shop = Shop.objects.get(id=sid)
    except Shop.DoesNotExist:
        return Response('Shop not found', status=status.HTTP_404_NOT_FOUND)
    serializer = ShopSerializer(shop)
    return Response(serializer.data, status=status.HTTP_200_OK)


## TODO: FEITO IG
@api_view(['POST'])
def create_shop(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        # Save DjangoAuth User
        django_user = serializer.save()

        shopName = request.data.get("shopName")
        if shopName is not None:
            # Save App User
            u = User()
            u.django_user = django_user

            s = Shop(owner=django_user, name=shopName, image='images/logo.png')
            s.save()

            my_group = Group.objects.get(name='shops')
            my_group.user_set.add(django_user)

        else:
            return Response("Something went wrong: shop name not defined",status=status.HTTP_400_BAD_REQUEST)

        return Response({'response': "Successfully registered the new shop.", 'email': u.django_user.email,
                         'username': u.django_user.username, 'token': Token.objects.get(user=django_user).key},
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
#NOT WORKING
@permission_classes([IsAuthenticated])
def shop_delete(request):
    if request.user.groups.filter(name='shops').exists():
        Shop.objects.get(owner__email=request.user.email).delete()
        return Response('Account deleted successfully', status=status.HTTP_204_NO_CONTENT)
    return Response('You don\'t have permissions to delete this account', status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def get_list_items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

'''

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_list_items(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        items = Item.objects.filter(shop=loggedShop)
        if 'num' in request.GET:
            num = int(request.GET['num'])
            items = items[:num]
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('You don\'t have permissions to list items, login with shop account in order to do that',
                    status=status.HTTP_406_NOT_ACCEPTABLE)
'''

@api_view(['GET'])
def see_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response('Item not found', status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        serializer = ItemSerializer(data=request.data)

        if serializer.is_valid():
            item = serializer.save()
            item.shop = loggedShop

            if item.price < item.product.lowest_price:
                item.product.lowest_price = item.price
                item.product.save()

            item.product.lowest_price = min([x.product.lowest_price for x in Item.objects.filter(product=item.product)])

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response('You don\'t have permissions to list items, login with shop account in order to do that',
                    status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_item(request, id):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)

        try:
            i = Item.objects.get(id=id)
            if i.shop != loggedShop:
                return Response('You arent the creator of this item, so you can\'t edit it. ',
                                status=status.HTTP_403_FORBIDDEN)
        except Item.DoesNotExist:
            return Response("Item not found", status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(i, data=request.data)

        if serializer.is_valid():
            item = serializer.save()

            if item.price < item.product.lowest_price:
                item.product.lowest_price = item.price
                item.product.save()

            item.product.lowest_price = min([x.product.lowest_price for x in Item.objects.filter(product=item.product)])

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response('You don\'t have permissions to list items, login with shop account in order to do that',
                    status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def item_delete(request, id):
    if request.user.groups.filter(name='shops').exists():
        Item.objects.get(id=id).delete()
        return Response('Item deleted successfully', status=status.HTTP_204_NO_CONTENT)
    return Response('You don\'t have permissions to delete this item', status=status.HTTP_406_NOT_ACCEPTABLE)

# ######################################################################################################################

# Create your views here.
def home(request):
    content = home_content(request)
    return render(request, 'home.html', content)


def login_view(request):  ########
    register_error = False
    login_error = False
    if request.method == "POST":
        print("entered")
        if 'sign_in' in request.POST:
            login_form = LoginDjangoUserForm(data=request.POST)
            register_form = RegisterDjangoUserForm()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return render(request, 'home.html')
            else:
                print("User does not exist")
                login_error = True
        elif 'sign_up' in request.POST:
            register_form = RegisterDjangoUserForm(data=request.POST)
            login_form = LoginDjangoUserForm()
            if register_form.is_valid():
                print("valid")
                user = User()
                django_user = register_form.save()
                django_user.set_password(django_user.password)
                django_user.save()
                user.django_user = django_user
                cart = Cart(user=user)
                wishlist = WishList(user=user)
                user.save()
                cart.save()
                wishlist.save()
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                return render(request, 'home.html')

            else:
                print(register_form.errors)
                register_error = True

    else:
        register_form = RegisterDjangoUserForm()
        login_form = LoginDjangoUserForm()
    content = {'user_form': register_form, 'login_form': login_form, 'register_error': register_error,
               'login_error': login_error}
    return render(request, 'login.html', content)


def new_arrivals(request):  ########
    products = Product.objects.all().order_by("id")[0:20]

    content = {
        'products': products,
        'page': 'New Arrivals'
    }
    return render(request, 'new_hot_items.html', content)


def hot_deals(request):  #########
    products = Product.objects.all().order_by("-qty_sold")[0:20]  # Apenas os {20} Produtos + vendidos
    content = {
        'products': products,
        'page': 'Hot Deals'
    }
    return render(request, 'new_hot_items.html', content)


@api_view(['GET'])
def search(request):  ##########
    if 'name' in request.GET:
        name = request.GET['name']
    else:
        name = ""

    if 'category' in request.GET:
        category = request.GET['category']
    else:
        category = "all"

    global global_products

    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        items = Item.objects.filter(shop=loggedShop)

        if category == 'all':
            global_products = [i.product for i in items if str(name).lower() in i.product.name.lower()]
        else:
            global_products = [i.product for i in items if str(name).lower() in i.product.name.lower() or str(
                category).lower() in i.product.category.name.lower()]
    else:
        if category == 'all':
            global_products = Product.objects.filter(name__icontains=name)
        else:
            global_products = Product.objects.filter(name__icontains=name, category__name__icontains=category)

    page = request.GET.get('page')
    paginator = Paginator(global_products, 12)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    #This is returning with the paginator... Idk if this works well...
    #If errors => (return global_products and do the pagination in angular)
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def search2(request, filter, value):  ######
    if filter == 'category':
        f_products = Product.objects.filter(category__name__icontains=value)
    elif filter == 'brand':
        f_products = Product.objects.filter(brand__name__icontains=value)
    elif filter == 'shop':
        f_products = Product.objects.filter(item__shop__name__icontains=value)

    paginator = Paginator(f_products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    # This is returning with the paginator... Idk if this works well...
    # If errors => (return f_products and do the pagination in angular)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def account_page(request):  #######
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        orders_list = Order.objects.filter(user=user).order_by("-id")
        user_form, address_form = loadAccountPageForms(user)
        updated_user_form = False
        updated_address_form = False
        show_dashboard = False
        show_address = False
        show_edit_account = False

        if request.method == "POST":
            if 'account_edit' in request.POST:
                user_form = EditUserForm(request.POST)
                updated_user_form = process_account_edit(user_form, user, updated_user_form)
                show_edit_account = True
            elif 'address_create' in request.POST:
                address_form = AddAddressForm(request.POST)
                updated_address_form = process_address_create(address_form, user, updated_user_form)
                show_address = True
            elif 'address_edit' in request.POST:
                address_form = EditAddressForm(request.POST)
                updated_address_form = process_address_edit(address_form, user, updated_user_form)
                show_address = True
        else:
            show_dashboard = True

        return render(request, 'dashboard.html',
                      {'extra_user_form': user_form, 'address_form': address_form,
                       'updated_user_form': updated_user_form, 'updated_address_form': updated_address_form,
                       'show_dashboard': show_dashboard, 'show_address': show_address,
                       'show_edit_account': show_edit_account, 'orders_list': orders_list})
    else:
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def loadAccountPageForms(user):
    user_form = EditUserForm(initial={'username': user.django_user.username,
                                      'email': user.django_user.email,
                                      'phone_number': user.phone_number,
                                      'age': user.age,
                                      'gender': user.gender})
    if user.address:
        address_form = EditAddressForm(initial={'country': user.address.country,
                                                'city': user.address.city,
                                                'zip_code': user.address.zip_code,
                                                'street': user.address.street,
                                                'door': user.address.door,
                                                'floor': user.address.floor})
    else:
        address_form = AddAddressForm()
    return user_form, address_form


def process_account_edit(user_form, user, updated):
    if user_form.is_valid():
        # Update All Fields
        user.django_user.username = user_form.cleaned_data['username']
        user.django_user.email = user_form.cleaned_data['email']
        user.phone_number = user_form.cleaned_data['phone_number']
        user.age = user_form.cleaned_data['age']
        user.gender = user_form.cleaned_data['gender']
        user.django_user.save()
        user.save()
        updated = True
    else:
        print(user_form.errors)
    return updated


def process_address_create(address_form, user, updated):
    if address_form.is_valid():
        # Load All Fields
        country = address_form.cleaned_data['country']
        city = address_form.cleaned_data['city']
        street = address_form.cleaned_data['street']
        zip_code = address_form.cleaned_data['zip_code']
        floor = address_form.cleaned_data['floor']
        door = address_form.cleaned_data['door']

        # Save Adress
        new_address = Address(country=country, city=city, street=street, zip_code=zip_code, floor=floor, door=door)
        new_address.save()
        user.address = new_address
        user.save()
        updated = True
    else:
        print(address_form.errors)
    return updated


def process_address_edit(address_form, user, updated):
    if address_form.is_valid():
        # Update All Fields
        user.address.country = address_form.cleaned_data['country']
        user.address.city = address_form.cleaned_data['city']
        user.address.street = address_form.cleaned_data['street']
        user.address.zip_code = address_form.cleaned_data['zip_code']
        user.address.floor = address_form.cleaned_data['floor']
        user.address.door = address_form.cleaned_data['door']
        user.save()
        updated = True
    else:
        print(address_form.errors)
    return updated


def add_product(request):  ######
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        if request.method == 'POST':
            form = AddProductForm(request.POST, request.FILES)

            if form.is_valid():
                reference_number = form.cleaned_data['reference_num']
                name = form.cleaned_data['name']
                details = form.cleaned_data['details']
                warehouse = form.cleaned_data['warehouse']
                price = form.cleaned_data['price']
                image = form.cleaned_data['image']
                category = form.cleaned_data['category']
                brand = form.cleaned_data['brand']

                if image is None:
                    image = 'images/logo.png'

                if category.name == 'Other':
                    new_cat = request.POST['new_cat']
                    category = Category(name=new_cat, totDevices=0)
                    category.save()

                if brand.name == 'Other':
                    new_brand = request.POST['new_brand']
                    brand = Brand(name=new_brand)
                    brand.save()

                try:
                    p = Product(qty_sold=0, lowest_price=price, reference_number=reference_number, name=name,
                                details=details, warehouse=warehouse, image=image, category=category, brand=brand,
                                creator=loggedShop)
                    p.save()

                    c = Category.objects.get(name=category)
                    c.totDevices += 1
                    c.save()

                    i = Item(price=price, shop=loggedShop, product=p, stock=1)
                    i.save()
                except:
                    return render(request, 'productForm.html',
                                  {'msgErr': ' Product not inserted, try again later!', 'page': 'Add',
                                   'obj': 'Product'})
                return render(request, 'productForm.html',
                              {'msg': ' Product ' + p.name + ' inserted successfully!', 'page': 'Add',
                               'obj': 'Product'})
        else:
            form = AddProductForm()
            return render(request, 'productForm.html', {'form': form, 'page': 'Add', 'obj': 'Product'})
    else:
        return render(request, 'error.html')


def add_item(request):  ######
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        if request.method == 'POST':
            form = AddItem(request.POST)

            if form.is_valid():
                prod = form.cleaned_data['product']
                stock = form.cleaned_data['stock']
                price = form.cleaned_data['price']

                try:
                    i = Item(product=prod, shop=loggedShop, stock=stock, price=price)
                    i.save()

                    if i.price < prod.lowest_price:
                        prod.lowest_price = i.price
                        prod.save()

                except:
                    return render(request, 'productForm.html')
                return render(request, 'productForm.html',
                              {'msg': ' Item inserted successfully!', 'page': 'Add', 'obj': 'Item'})
        else:
            form = AddItem()
            return render(request, 'productForm.html', {'form': form, 'page': 'Add', 'obj': 'Item'})
    else:
        return render(request, 'error.html')


def edit_item(request, id):  #######
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        if request.method == 'POST':
            i = Item.objects.get(id=id)
            form = EditItem(request.POST, instance=i)

            if form.is_valid():
                form.save()
                price = form.cleaned_data['price']

                try:
                    if price < i.product.lowest_price:
                        i.product.lowest_price = price
                        i.product.save()

                except:
                    return render(request, 'productForm.html',
                                  {'msgErr': ' Error while updating, try again!', 'page': 'Edit', 'obj': 'Item'})
                return render(request, 'productForm.html',
                              {'msg': ' Item updated successfully!', 'page': 'Edit', 'obj': 'Item'})
        else:
            form = EditItem(instance=Item.objects.get(id=id))
            return render(request, 'productForm.html', {'form': form, 'page': 'Edit', 'obj': 'Item', 'id': id})
    else:
        return render(request, 'error.html')


def list_items(request):  #####
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        items = Item.objects.filter(shop=loggedShop)
        return render(request, 'items_list.html', {'items': items})
    else:
        return render(request, 'error.html')


def delete_item(request, id):  #####
    if request.user.groups.filter(name='shops').exists():
        Item.objects.get(id=id).delete()
        return redirect('items')
    return render(request, 'error.html')


def edit_product(request, pid):  #####
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        if Item.objects.filter(product_id=pid).count() > 1:
            return render(request, 'productForm.html', {
                'msgErr': 'You don\'t have permissions to edit this product anymore, other shops depend on it',
                'page': 'Edit', 'obj': 'Product'})
        if request.method == 'POST':
            p = Product.objects.get(id=pid)
            form = EditProductForm(request.POST, request.FILES, instance=p)

            if form.is_valid():
                i = Item.objects.get(product=p)
                i.price = form.cleaned_data['price']
                i.save()
                i.save()

                form.save()
                if form.cleaned_data['image'] is None:
                    image = 'images/logo.png'
                    p.image = image
                    p.save()

                if form.cleaned_data['category'].name == 'Other':
                    new_cat = request.POST['new_cat']
                    c = Category(name=new_cat, totDevices=1)
                    c.save()
                    p.category = c
                    p.save()

                if form.cleaned_data['brand'].name == 'Other':
                    new_brand = request.POST['new_brand']
                    b = Brand(name=new_brand)
                    b.save()
                    p.brand = b
                    p.save()
                return render(request, 'productForm.html',
                              {'msg': 'Product ' + p.name + ' updated successfully!', 'page': 'Edit', 'obj': 'Product'})
        else:
            p = Product.objects.get(id=pid)
            form = EditProductForm(instance=p)
            form.fields['price'].initial = Item.objects.get(product=p).price
            return render(request, 'productForm.html', {'form': form, 'page': 'Edit', 'obj': 'Product', 'id': pid})
    return render(request, 'error.html')


def delete_product(request, pid):  ######
    if request.user.groups.filter(name='shops').exists():
        if Item.objects.filter(product_id=pid).count() > 1:
            return render(request, 'productForm.html', {
                'msgErr': 'You don\'t have permissions to delete this product anymore, other shops depend on it',
                'page': 'Edit', 'obj': 'Product'})
        Product.objects.get(id=pid).delete()
        return redirect('products')
    return render(request, 'error.html')


def list_products(request):  #########
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        p = Product.objects.filter(creator=loggedShop)
        return render(request, 'prodsList.html', {'products': p})
    else:
        return render(request, 'error.html')


def list_shops(request):  ######
    shops = Shop.objects.all()
    return render(request, 'shopsList.html', {'shops': shops})


def see_shop(request, sid):  ######
    shop = Shop.objects.get(id=sid)
    return render(request, 'shopDetails.html', {'shop': shop})


def add_shop(request):  #######
    if request.method == 'POST':
        register_form = RegisterDjangoUserForm(request.POST)
        form = AddShopForm(request.POST)

        if register_form.is_valid():
            django_user = register_form.save()
            django_user.set_password(django_user.password)
            django_user.save()
        else:
            return render(request, 'shopRegister.html', {'forms': [form, register_form]})

        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone_number']
        else:
            return render(request, 'shopRegister.html', {'forms': [form, register_form]})

        try:
            s = Shop(owner=django_user, phone_number=phone, name=name, image='images/logo.png')
            s.save()

        except:
            return render(request, 'shopRegister.html', {'msgErr': ' Error while creating shop, try again!'})

        my_group = Group.objects.get(name='shops')
        my_group.user_set.add(django_user)

        return render(request, 'shopRegister.html', {'msg': 'Shop registered, please login now!'})
    else:
        return render(request, 'shopRegister.html', {'forms': [AddShopForm(), RegisterDjangoUserForm()]})


def edit_shop(request):
    if request.user.groups.filter(name='shops').exists():
        if request.method == 'POST':
            s = Shop.objects.get(owner=request.user)
            form = EditShopForm(request.POST, request.FILES, instance=s)
            if s.address is None:
                formA = AddAddressForm(request.POST)
            else:
                formA = EditAddressForm(request.POST, instance=s.address)

            formO = EditDjangoUserForm(request.POST, instance=request.user)

            if formO.is_valid():
                formO.save()
                print('Passou owner')

            if formA.is_valid():
                if s.address is None:
                    country = formA.cleaned_data['country']
                    city = formA.cleaned_data['city']
                    street = formA.cleaned_data['street']
                    zip_code = formA.cleaned_data['zip_code']
                    floor = formA.cleaned_data['floor']
                    door = formA.cleaned_data['door']

                    # Save Adress
                    new_address = Address(country=country, city=city, street=street, zip_code=zip_code, floor=floor,
                                          door=door)
                    new_address.save()
                    s.address = new_address
                else:
                    formA.save()
                print('Passou address')

            if form.is_valid():
                form.save()
                print('Passou shop')

                if form.cleaned_data['image'] is None:
                    image = 'images/logo.png'
                    s.image = image
                    s.save()

                return render(request, 'shopForm.html',
                              {'msg': 'Shop ' + s.name + ' updated successfully!', 'page': 'Edit'})
            else:
                return render(request, 'shopForm.html', {'msgErr': 'Error while updating!', 'page': 'Edit'})
        else:
            s = Shop.objects.get(owner=request.user)
            form = EditShopForm(instance=s)
            if s.address is None:
                formA = AddAddressForm()
            else:
                formA = EditAddressForm(instance=s.address)
            formO = EditDjangoUserForm(instance=request.user)

            return render(request, 'shopForm.html', {'forms': [form, formA, formO], 'page': 'Edit'})
    else:
        return render(request, 'error.html')


def delete_shop(request):
    if request.user.groups.filter(name='shops').exists():
        Shop.objects.get(email=request.user.email).delete()
        return redirect('logout')
    return render(request, 'error.html')


@api_view(['GET'])
def home_content(request):
    brands_list = cache.get('brands_list')
    hot_deals = cache.get('hot_deals')
    new_arrivals = cache.get('new_arrivals')
    categories = cache.get('categories')
    shops = cache.get('shops')

    if not (brands_list and hot_deals and new_arrivals and categories and shops):
        brands_list = Brand.objects.all().order_by('name')
        products = Product.objects.all()
        hot_deals = products.order_by("-qty_sold")[0:12]
        new_arrivals = products.order_by("id")[0:12]
        categories = Category.objects.all()
        shops = Shop.objects.all()

        cache.set('brands_list', brands_list)
        cache.set('products', products)
        cache.set('hot_deals', hot_deals)
        cache.set('new_arrivals', new_arrivals)
        cache.set('categories', categories)
        cache.set('shops', shops)

    serializer = BrandSerializer(brands_list.exclude(name='Other'), many=True)
    serializer2 = CategorySerializer(categories.order_by("-totDevices").exclude(name='Other')[0:6], many=True)
    serializer3 = ProductSerializer(hot_deals, many=True)
    serializer4 = ProductSerializer(new_arrivals, many=True)
    serializer5 = CategorySerializer(categories.exclude(name='Other'), many=True)
    serializer6 = ShopSerializer(shops, many=True)


    data = {
            'brands_list': serializer.data,
            'categories': serializer2.data,
            'hot_deals': serializer3.data,
            'new_arrivals': serializer4.data,
            'all_categories': serializer5.data,
            'shops': serializer6.data
            }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_shops(request, prod_id):
    product_in_wishlist = False
    product = Product.objects.get(id=prod_id)
    item_per_shop = Item.objects.filter(product=product)

    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_wishlist = WishList.objects.get(user=user)
        if product in user_wishlist.prods.all():
            product_in_wishlist = True

        if 'viewed' in request.session:
            if product.id not in request.session['viewed']:
                request.session['viewed'] += [product.id]
        else:
            request.session['viewed'] = [product.id]

    serializer = ProductSerializer(product, many=True)
    serializer2 = ItemSerializer(item_per_shop, many=True)

    #data = {
    #    'prod': serializer.data,
    #    'wishlist': product_in_wishlist,
    #    'prod_per_shop': serializer2.data
    #}

    return Response(serializer2.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def isWished(request, prod_id):
    product_in_wishlist = False
    product = Product.objects.get(id=prod_id)

    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_wishlist = WishList.objects.get(user=user)
        if product in user_wishlist.prods.all():
            product_in_wishlist = True

    return Response(product_in_wishlist, status=status.HTTP_200_OK)

@api_view(['GET'])
def order_product(request):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        cart_items = Cart_Item.objects.filter(cart=user_cart)
        for item in cart_items:
            proccess_order(user, item.item, item.qty, PAYMENT_METHOD[0][0])

        return Response("Order Successful!", status=status.HTTP_200_OK)
    else:
        return Response("You must login first to order a product", status=status.HTTP_403_FORBIDDEN)


def proccess_order(user, item, qty, payment_meth):
    success = error_qty = error_address = False
    if user.address:
        print(item.stock)
        print(qty)
        if item.stock >= qty:
            total_price = qty * item.price

            order = Order(quantity=qty, user=user, item=item,
                          total_price=total_price, order_state=ORDER_STATE[0][0], payment_meth=payment_meth)
            order.save()
            item.stock = item.stock - qty
            item.save()
            success = True

            # Remove from Cart if it was there
            user_cart = Cart.objects.get(user=user)
            cart_item = Cart_Item.objects.filter(cart=user_cart, item=item)
            if cart_item[0].item == item:
                cart_item[0].delete()
        else:
            error_qty = True
    else:
        error_address = True
    print(success)
    print(error_qty)
    print(error_address)
    return success, error_qty, error_address

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enoughQty(request):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        for cart_item in user_cart.cart_item_set.all():
            if cart_item.qty>cart_item.item.stock:
                print("bigger")
                return Response(cart_item.item.product.name, status=status.HTTP_200_OK)
        return Response("none", status=status.HTTP_200_OK)
    return Response("Log in first", status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSumCart(request):
    sum=0
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        for cart_item in user_cart.cart_item_set.all():
            sum += cart_item.item.price * cart_item.qty
        return Response(sum, status=status.HTTP_200_OK)
    return Response("Log in first", status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_to_Cart(request, item_id):
    print("hello")
    if request.user.is_authenticated:
        print("auth")
        user = User.objects.get(django_user=request.user)
        item = Item.objects.get(id=item_id)
        print(user)
        print(item)
        # Load User_Cart
        user_cart = Cart.objects.get(user=user)
        print(user_cart)
        # Save item in Cart
        duplicated_item = Cart_Item.objects.filter(cart=user_cart, item=item)
        print(duplicated_item)
        if duplicated_item:
            print("duplicated")
            duplicated_item[0].qty = duplicated_item[0].qty + 1
            duplicated_item[0].save()
        else:
            print("nope")
            cart_item = Cart_Item(cart=user_cart, item=item, qty=1)
            cart_item.save()

        # Update Total Price
        new_total = 0
        for cart_item in user_cart.cart_item_set.all():
            new_total += cart_item.item.price * cart_item.qty

        print(new_total)
        user_cart.total_price = new_total
        user_cart.save()

        return Response("Added item(s) to cart", status=status.HTTP_200_OK)
    else:
        return Response("You must login first to add to cart", status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def rem_from_Cart(request, item_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        item = Item.objects.get(id=item_id)

        cart_items = Cart_Item.objects.filter(cart=user_cart, item=item)
        if len(cart_items) > 0:
            if cart_items[0].qty==1:
                cart_items[0].delete()
            else:
                cart_items[0].qty-=1
                cart_items[0].save()
        return Response("Removed item(s) from the cart", status=status.HTTP_200_OK)
    else:
        return Response("You must login first to use the cart", status=status.HTTP_403_FORBIDDEN)


def add_to_Wishlist(request, prod_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        prod = Product.objects.get(id=prod_id)

        # Load User_Wishlist
        user_wishlist = WishList.objects.get(user=user)

        # Save Product in Cart
        if prod not in user_wishlist.prods.all():
            print("product that will be added:")
            print(prod)
            user_wishlist.prods.add(prod)
        else:
            print("already have this product")

        return redirect(request.META['HTTP_REFERER'])  # redirect to previous url
    else:
        # Maybe later, save cart items in cache when not authenticated?
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def rem_from_Wishlist(request, prod_id):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        prod = Product.objects.get(id=prod_id)
        user_wishlist = WishList.objects.get(user=user)

        if prod in user_wishlist.prods.all():
            user_wishlist.prods.remove(prod)
        return redirect(request.META['HTTP_REFERER'])  # redirect to previous url
    else:
        # Maybe later, save cart items in cache when not authenticated?
        return redirect(request.META['HTTP_REFERER'])  # Redirect to previous url


def cart(request):
    if request.user.is_authenticated:
        success = False
        error_qty_items = 0
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        user_cart_items = Cart_Item.objects.filter(cart=user_cart).order_by('id')
        payment_meth_form = CartBuyForm()

        if request.method == "POST":
            print(request.POST)
            user = User.objects.get(django_user=request.user)
            payment_meth = request.POST['payment_meth']
            ids = request.POST.getlist('item_id[]')
            qtys = request.POST.getlist('qty[]')

            # Buy All Products
            for x in range(len(ids)):
                item_id = ids[x]
                qty = qtys[x]
                item = Item.objects.get(id=item_id)

                # Update cart_item qty
                cart_item = Cart_Item.objects.get(item=item)
                cart_item.qty = qty
                cart_item.save()

                # Verifications & Purchase
                success2, error_qty, error_address = proccess_order(user, item, int(qty), payment_meth)

                # If no address, return immediately
                if error_address:
                    return render(request, 'cart.html',
                                  {'user_cart_items': user_cart_items, 'payment_meth_form': payment_meth_form,
                                   'error_address': error_address})

                # Count the products that don't have enough stock
                if error_qty:
                    error_qty_items = error_qty_items + 1

            if error_qty_items == 0:
                success = True

        return render(request, 'cart.html',
                      {'user_cart_items': user_cart_items, 'payment_meth_form': payment_meth_form,
                       'success': success, 'error_qty_items': error_qty_items})
    else:
        return HttpResponseRedirect('/login')

@api_view(['GET'])
def prod_stock(request):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_wishlist = WishList.objects.get(user=user)
        _wishlist = user_wishlist.prods.all()
        prod_stock = {}
        # Verify if it has stock or not in any of the shops
        for prod in _wishlist:
            has_stock = False
            items = Item.objects.filter(product=prod)
            qtys = [item.stock for item in items]

            if qtys and max(qtys) > 0:
                has_stock = True
            else:
                has_stock = False

            if prod.name not in prod_stock:
                prod_stock[prod.name] = has_stock
        print(prod_stock)
        return Response(prod_stock, status=status.HTTP_200_OK)
    else:
        return Response("You must login first to use the cart", status=status.HTTP_403_FORBIDDEN)

def wishlist(request):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_wishlist = WishList.objects.get(user=user)
        _wishlist = user_wishlist.prods.all()
        prod_stock = {}

        # Verify if it has stock or not in any of the shops
        for prod in _wishlist:
            has_stock = False
            items = Item.objects.filter(product=prod)
            qtys = [item.stock for item in items]

            if qtys and max(qtys) > 0:
                has_stock = True
            else:
                has_stock = False

            if prod.name not in prod_stock:
                prod_stock[prod.name] = has_stock

        return render(request, 'wishlist.html', {'wishlist': _wishlist, 'prod_stock': prod_stock})
    else:
        return HttpResponseRedirect('/login')


class AccountSignupView(SignupView):
    template_name = "login.html"


account_signup_view = AccountSignupView.as_view()


