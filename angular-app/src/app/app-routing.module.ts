import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HotdealsComponent} from "./clientside/hotdeals/hotdeals.component";
import {NewarrivalsComponent} from "./clientside/newarrivals/newarrivals.component";
import {HomeComponent} from "./clientside/home/home.component";
import {SignInComponent} from "./clientside/sign-in/sign-in.component";
import {ShopsListComponent} from "./clientside/shops-list/shops-list.component";
import {ShopDetailsComponent} from "./clientside/shop-details/shop-details.component";
import {SignUpComponent} from "./clientside/sign-up/sign-up.component";
import {UserProfileComponent} from "./clientside/user-profile/user-profile.component";

const routes: Routes = [
  {path: '', component:HomeComponent},
  {path: 'home', component:HomeComponent},
  {path: 'login', component: SignInComponent},
  {path: 'signup', component: SignUpComponent},
  {path: 'hotdeals', component: HotdealsComponent},
  {path: 'newarrivals', component: NewarrivalsComponent},
  {path: 'shops', component: ShopsListComponent},
  {path: 'shops/:id', component: ShopDetailsComponent},
  {path: 'userprofile', component: UserProfileComponent}


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
