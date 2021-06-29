import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HttpClientModule} from "@angular/common/http";
import { NavbarComponent } from './_common/navbar/navbar.component';
import { UserProfileComponent } from './clientside/user-profile/user-profile.component';
import { ShopsComponent } from './_models/shops.component';
import { BrandsComponent } from './clientside/brands/brands.component';
import { CategoriesComponent } from './clientside/categories/categories.component';
import { ProductsComponent } from './clientside/products/products.component';
import { ItemsComponent } from './clientside/items/items.component';
import { CartItemsComponent } from './clientside/cart-items/cart-items.component';
import { OrdersComponent } from './clientside/orders/orders.component';
import {FooterComponent} from "./_common/footer/footer.component";
import { HotdealsComponent } from './clientside/hotdeals/hotdeals.component';
import { NewarrivalsComponent } from './clientside/newarrivals/newarrivals.component';
import { SignInUpComponent } from './clientside/sign-in-up/sign-in-up.component';
import { HomeComponent } from './clientside/home/home.component';
import { ShopsCarouselComponent } from './clientside/shops-carousel/shops-carousel.component';
import { AlertComponent } from './_common/alert/alert.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    UserProfileComponent,
    ShopsComponent,
    BrandsComponent,
    CategoriesComponent,
    ProductsComponent,
    ItemsComponent,
    CartItemsComponent,
    OrdersComponent,
    HotdealsComponent,
    NewarrivalsComponent,
    SignInUpComponent,
    HomeComponent,
    ShopsCarouselComponent,
    AlertComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
