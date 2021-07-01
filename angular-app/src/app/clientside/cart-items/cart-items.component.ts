import { Component, OnInit } from '@angular/core';
import {CartService} from "../../_services/cart.service";
import {ActivatedRoute} from "@angular/router";
import {CartItem} from "../../_models/cartItem";
import {UserService} from "../../_services/user.service";
import {User} from "../../_models/user";
import {ProductsService} from "../../_services/products.service";


@Component({
  selector: 'app-cart-items',
  templateUrl: './cart-items.component.html',
  styleUrls: ['./cart-items.component.css']
})
export class CartItemsComponent implements OnInit {
  user_cart_items: CartItem[] | undefined;
  user: User | undefined;
  test: string | undefined;
  sum: number | undefined;

  constructor(private cartService: CartService, private route: ActivatedRoute, private userService: UserService, private productService:ProductsService) {
  }

  ngOnInit(): void {
    this.getCart();
    this.userInfo();
    this.enoughQty();
    this.sumCart();
  }

  private getCart(): void {
    this.cartService.getCart().subscribe(user_cart_items => {
      this.user_cart_items = user_cart_items;
    });
  }

   remCart(id:any):void{
    this.cartService.remCart(eval(id)).subscribe(()=>{location.reload()});
  }

  private userInfo():void{
    this.userService.getUserInfo().subscribe(user=>{
      this.user=user;
    })
  }

  enoughQty():void{
    this.productService.enoughQty().subscribe(test=>{
      this.test=test;
    })
  }

  rowSum(num1:any,num2:any){
    return eval(num1)*eval(num2);
  }

  sumCart():void{
    this.productService.getSum().subscribe(sum=>{
      this.sum=sum;
    })
  }

}
