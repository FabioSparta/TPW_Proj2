import {User} from "./user";
import {Item} from "./items";

export class Order{
  quantity: number | undefined;
  user: User | undefined;
  item: Item | undefined;
  total_price: number | undefined;
  order_state: string | undefined;
  payment_meth: string | undefined;


}
