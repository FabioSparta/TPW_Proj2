import {Address} from "./address";

export class User{
  id: number;
  address?: Address;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  gender?:string;
  age?: number;
  phone_number?: bigint;

  constructor(id: number, email: string, username: string) {
    this.id = id;
    this.email = email;
    this.username = username;
  }

}
