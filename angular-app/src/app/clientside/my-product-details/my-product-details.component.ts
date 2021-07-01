import { Component, OnInit } from '@angular/core';
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";
import {ActivatedRoute} from "@angular/router";
import {Item} from "../../_models/items";
import {ItemsService} from "../../_services/items.service";
import {WishlistService} from "../../_services/wishlist.service";
import {CartService} from "../../_services/cart.service";
import {CartItem} from "../../_models/cartItem";

@Component({
  selector: 'app-my-product-details',
  templateUrl: './my-product-details.component.html',
  styleUrls: ['./my-product-details.component.css']
})
export class MyProductDetailsComponent implements OnInit {
  prod: Product | undefined;
  prod_per_shop: Item[] | undefined;
  wishlist: boolean | undefined;
  feedback: string | undefined;
  constructor(private productService: ProductsService, private itemService: ItemsService,private wishService: WishlistService ,private route: ActivatedRoute, private cartService: CartService) { }

  ngOnInit(): void {
    this.getProduct();
  }

  getProduct(){
      let id = this.route.snapshot.paramMap.get('id');
      if(id==null){
        id="-1";
      }
      this.productService.getProduct(eval(id)).subscribe(prod=> {
        this.prod = prod;
      });
      this.getShops(eval(id));
      this.isWished(eval(id));
  }

  getShops(id:number){
    this.itemService.itemPerShop(id).subscribe(prod_per_shop=> {
        this.prod_per_shop = prod_per_shop;
      });
  }

  isWished(id:number){
    this.wishService.isWished(id).subscribe(wishlist=> {
        this.wishlist = wishlist;
        console.log(wishlist);
      });
  }

  addWishList(){
    // @ts-ignore
    this.wishService.addWishList(this.prod.id).subscribe(
      data => {
            location.reload();
        },
      error => {
            window.location.href="/login";
        });
  }

  remWishList(){
    // @ts-ignore
    this.wishService.remWishList(this.prod.id).subscribe(()=>{location.reload()});
  }

  addCart(id:number){
    this.cartService.addCart(id).subscribe(
      data => {
            location.reload();
        },
        error => {
            window.location.href="/login";
        });

  }

}
