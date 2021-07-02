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

    # Products
    path('api/products/', views.list_prods),
    path('api/products/create', views.create_product),
    path('api/products/edit/<int:pid>', views.update_product),
    path('api/products/<int:pid>', views.see_product),
    path('api/products/delete/<int:pid>', views.delete_prod),
    path('api/products/hotdeals',                    views.get_prods_hotdeals),
    path('api/products/newarrivals',                 views.get_prods_newarrivals),
    path('api/products/search', views.search),
    path('api/products/search2/<str:filter>/<str:value>', views.search2),

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
    path('api/account/order', views.order_product),
    path('api/account/cart/add/<int:item_id>', views.add_to_Cart),
    path('api/account/cart/rem/<int:item_id>', views.rem_from_Cart),

    # Items
    path('api/items/', views.get_list_items),
    path('api/items/create', views.create_item),
    path('api/items/<int:id>', views.see_item),
    path('api/items/edit/<int:id>', views.update_item),
    path('api/items/delete/<int:id>', views.item_delete),

    # Brands and Categories
    path('api/brands/', views.list_brands),
    path('api/categories/', views.list_categories),

    # Shops
    path('api/shops/', views.get_shops_list),
    path('api/shops/<int:sid>', views.get_shop),
    path('api/shops/create', views.create_shop),
    path('api/shops/delete', views.shop_delete),

    path('api/home', views.home_content),
    path('api/shop/products/<int:prod_id>', views.product_shops),
    path('api/shop/products/wished/<int:prod_id>', views.isWished),

    # Cart
    path('api/cart/enoughQty', views.enoughQty),
    path('api/cart/sum', views.getSumCart),
    path('api/products/stock', views.prod_stock),

    ################################

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)