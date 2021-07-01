import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HotdealsComponent} from "./clientside/hotdeals/hotdeals.component";
import {NewarrivalsComponent} from "./clientside/newarrivals/newarrivals.component";
import {HomeComponent} from "./clientside/home/home.component";
import {SignInUpComponent} from "./clientside/sign-in-up/sign-in-up.component";
import {ItemDetailsComponent} from "./shopside/item-details/item-details.component";
import {ItemsComponent} from "./shopside/items/items.component";
import {ProductDetailsComponent} from "./shopside/product-details/product-details.component";
import {ProductsComponent} from "./shopside/products/products.component";
import {CreateProductComponent} from "./shopside/create-product/create-product.component";
import {ListProductsComponent} from "./clientside/list-products/list-products.component";
import {MyProductDetailsComponent} from "./clientside/my-product-details/my-product-details.component";
import {CartItemsComponent} from "./clientside/cart-items/cart-items.component";

const routes: Routes = [
  {path: '', component:HomeComponent},
  {path: 'home', component:HomeComponent},
  {path: 'login', component: SignInUpComponent},
  {path: 'hotdeals', component: HotdealsComponent},
  {path: 'newarrivals', component: NewarrivalsComponent},
  {path: 'items', component:ItemsComponent},
  {path: 'items/:id', component:ItemDetailsComponent},
  {path: 'products', component:ProductsComponent},
  {path: 'products/add', component:CreateProductComponent},
  {path: 'products/:id', component:ProductDetailsComponent},
  {path: 'search/:key/:cat', component: ListProductsComponent}, //Key and Cat
  {path: 'search/:cat', component: ListProductsComponent}, //Cat
  {path: 'search', component: ListProductsComponent}, //No Key and No Cat
  {path: 'products/details/:id', component: MyProductDetailsComponent},
  {path: 'account/cart', component: CartItemsComponent},

  //{path: 'authors', component:AuthorsComponent},
  //{path: 'overview', component:OverviewComponent},
 // {path: 'authordetails/:id', component:AuthorDetailsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
