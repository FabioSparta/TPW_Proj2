import {User} from "../user-profile/user";

export class Shop {
  name?: string ;
  owner?: User;
  phone_number?: string;
  address?: string;
  website?: string;
  opening_hours?: string;

  image?: File; // string for url..File for input element

}
