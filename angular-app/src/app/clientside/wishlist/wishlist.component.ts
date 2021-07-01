import { Component, OnInit } from '@angular/core';
import {WishlistService} from "../../_services/wishlist.service";
import {ActivatedRoute} from "@angular/router";
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";

@Component({
  selector: 'app-wishlist',
  templateUrl: './wishlist.component.html',
  styleUrls: ['./wishlist.component.css']
})
export class WishlistComponent implements OnInit {
  wishL: Product[] | undefined;
  prod_stock: any | undefined;
  constructor(private wishService:WishlistService,private route: ActivatedRoute, private prodService:ProductsService ) { }

  ngOnInit(): void {
    this.getWishList();
    this.all_stock();
  }

  getWishList():void{
    this.wishService.getWishList().subscribe(wishL=>{
      this.wishL=wishL;
    });
  }

  all_stock():void{
    this.prodService.prod_stock().subscribe(prod_Stock=>{
      this.prod_stock=prod_Stock;
    })
  }

  remWishList(id:any){
    // @ts-ignore
    this.wishService.remWishList(eval(id)).subscribe(()=>{location.reload()});
  }

  searchDict(key:string):boolean{
    return this.prod_stock[key];
  }

}
