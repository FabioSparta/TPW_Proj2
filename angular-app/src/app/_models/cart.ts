import {User} from "./user";

export class Cart{
  id: number;
  user?: User;
  total_price: number;

  constructor(id:number,user:User,total_price:number) {
    this.id=id;
    this.user=user;
    this.total_price=total_price;
  }
}
