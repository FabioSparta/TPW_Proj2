export class Address {
  id:  number;
  country : string;
  city : string;
  zip_code: string;
  street: string;
  door : number;
  floor: number;


  constructor(id: number, country: string, city: string, zip_code: string, street: string, door: number, floor: number = 0) {
    this.id = id;
    this.country = country;
    this.city = city;
    this.zip_code = zip_code;
    this.street = street;
    this.door = door;
    this.floor = floor;
  }
}
