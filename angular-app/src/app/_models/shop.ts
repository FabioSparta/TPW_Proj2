import {User} from "./user";
import {Address} from "./address";
import {Time} from "@angular/common";

export class Shop {
  id: number;
  name: string ;
  owner: User;
  phone_number?: bigint;
  address?: Address;
  website?: string;
  opening_hours?: Time;
  image?: File; //maybe string

  constructor(id:number ,name:string, owner:User) {
    this.id = id;
    this.name = name;
    this.owner = owner;
  }
}
