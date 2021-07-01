export class Address {
  id: number | undefined;
  country : string;
  city : string;
  zip_code: string;
  street: string;
  door : number;
  floor: number;


  constructor( country: string, city: string, zip_code: string, street: string, door: number, floor: number = 0) {
    this.country = country;
    this.city = city;
    this.zip_code = zip_code;
    this.street = street;
    this.door = door;
    this.floor = floor;
  }
}
