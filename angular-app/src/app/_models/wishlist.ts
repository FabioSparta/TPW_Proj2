import {User} from "./user";
import {Product} from "./products";

export class Wishlist{
  user?:User;
  prods:Product[];

  constructor(user:User,prods:Product[]) {
    this.user=user;
    this.prods=prods;
  }
}
