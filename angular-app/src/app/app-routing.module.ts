import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HotdealsComponent} from "./hotdeals/hotdeals.component";
import {NewarrivalsComponent} from "./newarrivals/newarrivals.component";
import {HomeComponent} from "./home/home.component";
import {SignInUpComponent} from "./sign-in-up/sign-in-up.component";

const routes: Routes = [
  {path: '', component:HomeComponent},
  {path: 'home', component:HomeComponent},
  {path: 'login', component: SignInUpComponent},
  {path: 'hotdeals', component: HotdealsComponent},
  {path: 'newarrivals', component: NewarrivalsComponent}
  //{path: 'authors', component:AuthorsComponent},
  //{path: 'overview', component:OverviewComponent},
 // {path: 'authordetails/:id', component:AuthorDetailsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
