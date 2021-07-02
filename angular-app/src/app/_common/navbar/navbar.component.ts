import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../_services/auth.service";
import {Router} from "@angular/router";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Category} from "../../_models/category";
import {CategoriesService} from "../../_services/categories.service";
import {CartItem} from "../../_models/cartItem";
import {CartService} from "../../_services/cart.service";
import {WishlistService} from "../../_services/wishlist.service";
import {Product} from "../../_models/products";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isShop: string;
  isAuthenticated : boolean
  username: string;
  categories : Category[] | undefined;
  searchForm: FormGroup;
  searchKey:string;
  searchCat:string;
  user_cart_items: CartItem[] | undefined;
  wishList: Product[] | undefined;
  counter:number | undefined;
  counter2:number | undefined;

  constructor(private authService: AuthService,private router: Router,private formBuilder:FormBuilder, private categoriesService:CategoriesService, private cartService: CartService, private wishService:WishlistService) {
    this.isShop="false";
    this.isAuthenticated=false;
    this.username= "User";
    this.searchKey="";
    this.searchCat="all";
    this.searchForm = formBuilder.group({
        searchVal: ['', Validators.required],
        searchCat: ['all', Validators.required]
      })
  }

  ngOnInit(): void {
    let username = this.authService.getUsername()
    if (username != "") this.username = username;

    let isShop = this.authService.isShop();
    if (isShop != null) this.isShop = <string>isShop;

    this.isAuthenticated = this.authService.isAuthenticated()
    this.getCategories();
    // @ts-ignore
    if (!eval(this.authService.isShop())){
      this.getCart();
      this.getWishL();
    }
  }

  logout():void{
    this.authService.logout();
    window.location.href = "/home";
  }

  updateKey() {
    this.searchKey=this.searchForm.get('searchVal')?.value;
  }

  updateCat() {
    this.searchCat=this.searchForm.get('searchCat')?.value;
    console.log(this.searchCat);
  }

  getCategories(){
    this.categoriesService.getCategories().subscribe(categories=> {
      this.categories = categories;
    });
  }

  getCart():void{
    this.cartService.getCart().subscribe(user_cart_items => {
      this.user_cart_items = user_cart_items;
      this.updateCounter();
    });
  }

  getWishL():void{
    this.wishService.getWishList().subscribe(wishList => {
      this.wishList = wishList;
      this.updateCounter2();
    });
  }

  updateCounter():void{
    this.counter=0;
    if(this.user_cart_items != null) {
      for (let a in this.user_cart_items) {
        // @ts-ignore
        this.counter += this.user_cart_items[a].qty;
      }
    }
  }

  updateCounter2():void{
    this.counter2=0;
    if(this.wishList != null) {
      this.counter2 = this.wishList.length;
    }
  }

  simClick() {
    console.log("entered");
    window.location.replace("/search/"+this.searchKey+"/"+this.searchCat);
  }
}

