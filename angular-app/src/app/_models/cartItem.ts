import {Item} from "./items";
import {Cart} from "./cart";

export class CartItem{
  id:number;
  item?: Item;
  qty: number;
  cart?: Cart;

  constructor(id:number, item:Item, qty:number, cart:Cart) {
    this.id=id;
    this.item=item;
    this.qty=qty;
    this.cart=cart;
  }
}
