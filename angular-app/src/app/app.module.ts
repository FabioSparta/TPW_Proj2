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
import { ProductsComponent } from './clientside/products/products.component';
import { ItemsComponent } from './clientside/items/items.component';
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
    SignUpComponent
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
