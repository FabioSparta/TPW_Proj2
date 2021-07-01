import { Component, OnInit } from '@angular/core';
import {CartService} from "../../_services/cart.service";
import {ActivatedRoute} from "@angular/router";
import {Product} from "../../_models/products";
import {CartItem} from "../../_models/cartItem";

@Component({
  selector: 'app-cart-items',
  templateUrl: './cart-items.component.html',
  styleUrls: ['./cart-items.component.css']
})
export class CartItemsComponent implements OnInit {
  user_cart_items: CartItem[] | undefined;

  constructor(private cartService: CartService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.getCart();
  }

  private getCart(): void {
    this.cartService.getCart().subscribe(user_cart_items => {
      this.user_cart_items = user_cart_items;
    });
  }
}
