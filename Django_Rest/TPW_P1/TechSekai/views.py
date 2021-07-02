import json

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
# Imports for Django
from rest_framework.permissions import IsAuthenticated
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
    idShop = Shop.objects.get(owner=request.user).id if isShop else 0
    return Response({'isShop': isShop , 'username' : request.user.username, 'userId':request.user.id, 'shopId': idShop}
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

        return Response("Updated successfully", status=status.HTTP_200_OK)

    
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
        user = User.objects.get(django_user=request.user)
        serializer.save()
        user.address = json.loads(json.dumps(serializer.data), object_hook=lambda d: Address(**d))
        user.save()
        return Response("Address added successfully.", status=status.HTTP_201_CREATED)
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
    if 'all' not in request.GET and request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        p = Product.objects.filter(creator=loggedShop)
    else:
        p = Product.objects.all()
    if len(p) == 0:
        return Response("No products found", status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(p, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            p = serializer.create(Category.objects.get(name=request.data['category']['name']), Brand.objects.get(name=request.data['brand']['name']),loggedShop)

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
            else:
                p.category.totDevices += 1

            try:
                price = request.data.get("price")
                if price==None:
                    price = 10
                i = Item(product=p, price=price, shop=loggedShop)
                #i.price = price
                i.save()
                p.lowest_price = i.price

            except Exception as e:
                Product.objects.get(id=p.id).delete()
                return Response("Something went wrong: check if you defined the product price",
                                status=status.HTTP_400_BAD_REQUEST)

            p.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    return Response("You must login with a shop account!", status=status.HTTP_403_FORBIDDEN)


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
            img = request.data.get("image")
            if img is None:
                img = 'images/logo.png'
            serializer.update(p, Brand.objects.get(name=request.data['brand']['name']),Category.objects.get(name=request.data['category']['name']))
            p.image = img
            p.save()

            p.creator = loggedShop

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


@api_view(['POST'])
def create_shop(request):
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        shopName = request.data.get("shop_name")
        if shopName is not None:
            # Save DjangoAuth User
            django_user = serializer.save()
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
@permission_classes([IsAuthenticated])
def get_list_items(request):
    if request.user.groups.filter(name='shops').exists():
        loggedShop = Shop.objects.get(owner=request.user)
        items = Item.objects.filter(shop=loggedShop)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('You don\'t have permissions to list items, login with shop account in order to do that',
                    status=status.HTTP_406_NOT_ACCEPTABLE)


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
        request.data['shop'] = loggedShop.__dict__
        serializer = ItemSerializer(data=request.data)

        if serializer.is_valid():
            item = serializer.create(Product.objects.get(id=request.data['product']['id']),loggedShop)

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
            serializer.update(i)

            if i.price < i.product.lowest_price:
                i.product.lowest_price = i.price
                i.product.save()

            i.product.lowest_price = min([x.product.lowest_price for x in Item.objects.filter(product=i.product)])

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
    return success, error_qty, error_address

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def enoughQty(request):
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        user_cart = Cart.objects.get(user=user)
        for cart_item in user_cart.cart_item_set.all():
            if cart_item.qty>cart_item.item.stock:
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
    if request.user.is_authenticated:
        user = User.objects.get(django_user=request.user)
        item = Item.objects.get(id=item_id)
        # Load User_Cart
        user_cart = Cart.objects.get(user=user)
        # Save item in Cart
        duplicated_item = Cart_Item.objects.filter(cart=user_cart, item=item)
        if duplicated_item:
            duplicated_item[0].qty = duplicated_item[0].qty + 1
            duplicated_item[0].save()
        else:
            cart_item = Cart_Item(cart=user_cart, item=item, qty=1)
            cart_item.save()

        # Update Total Price
        new_total = 0
        for cart_item in user_cart.cart_item_set.all():
            new_total += cart_item.item.price * cart_item.qty
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
        return Response(prod_stock, status=status.HTTP_200_OK)
    else:
        return Response("You must login first to use the cart", status=status.HTTP_403_FORBIDDEN)



