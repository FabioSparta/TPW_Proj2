from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from TPW_P1 import settings
from TechSekai import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),

    ########## REST ENDPOINTS #############

    # General
    #path('api/prods/all',                        views.get_prods_all),
    path('api/prods/hotdeals',                    views.get_prods_hotdeals),
    path('api/prods/newarrivals',                 views.get_prods_newarrivals),
    path('api/prods/search', views.search),
    path('api/prods/search2/<str:filter>/<str:value>', views.search2),

    # User
    path('api/account/signup',                     views.sign_up),
    path('api/account/login',                      obtain_auth_token),
    path('api/account/role',                       views.get_user_role),
    path('api/account/info',                       views.get_user_info),
    path('api/account/info/update',                views.update_user_info),
    path('api/account/orders',                     views.get_user_orders),
    path('api/account/address/add',                views.user_address_add),
    path('api/account/address/update',             views.user_address_update),
    path('api/account/address/rem',                views.user_address_rem),

    path('api/account/cart',                       views.get_cart),
    path('api/account/wishlist',                   views.get_wishlist),
    path('api/account/wishlist/add',               views.wishlist_add),
    path('api/account/wishlist/rem/<int:prod_id>', views.wishlist_remove),
    path('api/account/order', views.order_product),    #Maybe tweak this to allow buy from here
    path('api/account/cart/add/<int:item_id>', views.add_to_Cart),   #test
    path('api/account/cart/rem/<int:item_id>', views.rem_from_Cart), #test

    #products
    path('api/products/', views.list_prods),
    path('api/products/create', views.create_product),
    path('api/products/edit/<int:pid>', views.update_product),
    path('api/products/<int:pid>', views.see_product),
    path('api/products/delete/<int:pid>', views.delete_prod),

    #items
    path('api/items/', views.get_list_items),
    path('api/items/create', views.create_item),
    path('api/items/<int:id>', views.see_item),
    path('api/items/edit/<int:id>', views.update_item),
    path('api/items/delete/<int:id>', views.item_delete),

    #brands and categories
    path('api/brands/', views.list_brands),
    path('api/categories/', views.list_categories),

    # Shops
    path('api/shops/', views.get_shops_list),
    path('api/shops/<int:sid>', views.get_shop),
    path('api/shops/create', views.create_shop), #POR IMPLEMENTAR
    path('api/shops/delete', views.shop_delete),
    path('api/shops/edit', views.edit_shop), #POR IMPLEMENTAR

    path('api/home', views.home_content),
    path('api/shop/products/<int:prod_id>', views.product_shops), #Use? Test

    ################################





    # GENERAL PAGES
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/<str:filter>/<str:value>/', views.search2, name='search2'),
    path('hot_deals/', views.hot_deals, name='hot_deals'),
    path('new_arrivals/', views.new_arrivals, name='new_arrivals'),


    # ACCOUNT RELATED
    path('login/', views.login_view, name='login'),
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', views.account_signup_view),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', views.account_page, name='account'),

    # PRODUCT RELATED
    path('product/<int:prod_id>/', views.product_shops, name='product_shops'),
    path('do_order/<int:item_id>/', views.order_product, name='order_product'),
    path('add_to_cart/<int:item_id>/', views.add_to_Cart, name='add_to_cart'),
    path('rem_from_cart/<int:item_id>', views.rem_from_Cart, name='rem_from_cart'),
    path('add_to_wishlist/<int:prod_id>/', views.add_to_Wishlist, name='add_to_wishlist'),
    path('rem_from_wishlist/<int:prod_id>', views.rem_from_Wishlist, name='rem_from_wishlist'),


    ##PRODUCTS-SHOP
    path('products/add/', views.add_product, name='add_product'),
    path('products/', views.list_products, name='products'),
    path('products/edit/<int:pid>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pid>/', views.delete_product, name='delete_product'),
    path('items/', views.list_items, name='items'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/delete/<int:id>/', views.delete_item, name='delete_item'),
    path('items/edit/<int:id>/', views.edit_item, name='edit_item'),

    ## FAZER COMPRAS
    path('account/shoppingcart/', views.cart, name='cart'),
    path('account/wishlist', views.wishlist, name='wishlist'),

    ## GESTAO DAS LOJAS
    path('shops/add/', views.add_shop, name='add_shop'),
    path('shops/', views.list_shops, name='list_shops'),
    path('shops/<int:sid>/', views.see_shop, name='see_shop'),
    path('shop/account/', views.edit_shop, name='edit_shop'),
    path('shops/delete/', views.delete_shop, name='delete_shop'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)