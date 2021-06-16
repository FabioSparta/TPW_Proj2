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

    # User
    path('api/account/signup',                     views.sign_up),
    path('api/account/login',                      obtain_auth_token),
    path('api/account/info',                       views.get_user_info),
    path('api/account/address/add',                views.user_address_add),
    path('api/account/address/update',             views.user_address_update),
    path('api/account/address/rem',                views.user_address_rem),

    path('api/account/cart',                       views.get_cart),
    path('api/account/wishlist',                   views.get_wishlist),
    path('api/account/wishlist/add',               views.wishlist_add),
    path('api/account/wishlist/rem/<int:prod_id>', views.wishlist_remove),


    # Shops

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