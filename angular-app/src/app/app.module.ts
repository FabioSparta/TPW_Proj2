import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import { NavbarComponent } from './_common/navbar/navbar.component';
import { UserProfileComponent } from './clientside/user-profile/user-profile.component';
import { BrandsComponent } from './clientside/brands/brands.component';
import { CategoriesComponent } from './clientside/categories/categories.component';
import { ProductsComponent } from './shopside/products/products.component';
import { ItemsComponent } from './shopside/items/items.component';
import { CartItemsComponent } from './clientside/cart-items/cart-items.component';
import { OrdersComponent } from './clientside/orders/orders.component';
import {FooterComponent} from "./_common/footer/footer.component";
import { HotdealsComponent } from './clientside/hotdeals/hotdeals.component';
import { NewarrivalsComponent } from './clientside/newarrivals/newarrivals.component';
import { SignInComponent } from './clientside/sign-in/sign-in.component';
import { HomeComponent } from './clientside/home/home.component';
import { ShopsCarouselComponent } from './clientside/shops-carousel/shops-carousel.component';
import { CarouselModule } from 'ngx-owl-carousel-o';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ShopsListComponent } from './clientside/shops-list/shops-list.component';
import { ShopDetailsComponent } from './clientside/shop-details/shop-details.component';
import {AuthHeaderInterceptor} from "./_common/interceptor/auth-header-interceptor.interceptor";
import { SignUpComponent } from './clientside/sign-up/sign-up.component';
import { ItemDetailsComponent } from './shopside/item-details/item-details.component';
import { ProductDetailsComponent } from './shopside/product-details/product-details.component';
import { CreateProductComponent } from './shopside/create-product/create-product.component';
import { ListProductsComponent } from './clientside/list-products/list-products.component';
import { MyProductDetailsComponent } from './clientside/my-product-details/my-product-details.component';
import { CreateItemComponent } from './shopside/create-item/create-item.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    UserProfileComponent,
    BrandsComponent,
    CategoriesComponent,
    ProductsComponent,
    ItemsComponent,
    CartItemsComponent,
    OrdersComponent,
    HotdealsComponent,
    NewarrivalsComponent,
    SignInComponent,
    HomeComponent,
    ShopsCarouselComponent,
    ShopsListComponent,
    ShopDetailsComponent,
    SignUpComponent,
    ItemDetailsComponent,
    ProductDetailsComponent,
    CreateProductComponent,
    ListProductsComponent,
    MyProductDetailsComponent,
    CreateItemComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    CarouselModule,
    BrowserAnimationsModule
  ],
  providers: [
  {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthHeaderInterceptor,
    multi:true
  }

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
