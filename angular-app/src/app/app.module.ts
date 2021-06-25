import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HttpClientModule} from "@angular/common/http";
import { NavbarComponent } from './_common/navbar/navbar.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { ShopsComponent } from './shops/shops.component';
import { BrandsComponent } from './brands/brands.component';
import { CategoriesComponent } from './categories/categories.component';
import { ProductsComponent } from './products/products.component';
import { ItemsComponent } from './items/items.component';
import { CartItemsComponent } from './cart-items/cart-items.component';
import { OrdersComponent } from './orders/orders.component';
import {FooterComponent} from "./_common/footer/footer.component";
import { HotdealsComponent } from './hotdeals/hotdeals.component';
import { NewarrivalsComponent } from './newarrivals/newarrivals.component';
import { SignInUpComponent } from './sign-in-up/sign-in-up.component';
import { HomeComponent } from './home/home.component';

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
    HomeComponent
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
