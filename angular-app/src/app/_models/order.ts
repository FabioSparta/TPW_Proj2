import {User} from "./user";
import {Item} from "./items";

export class Order{
  quantity: number | undefined;
  user: User | undefined;
  item: Item | undefined;
  total_price: number | undefined;
  order_state: string | undefined;
  payment_meth: string | undefined;

  constructor(quantity:number,user:User,item:Item,total_price:number,order_state:string,payment_meth:string) {
    this.quantity=quantity;
    this.user=user;
    this.item=item;
    this.total_price=total_price;
    this.order_state=order_state;
    this.payment_meth=payment_meth;
  }
}
