import {Category} from "./category";
import {Brand} from "./brand";
import {Shop} from "./shop";

export class Product{
  id: number;
  reference_number: number;
  name: string;
  details: string;
  warehouse: string;
  qty_sold: number;
  image?: string
  category: Category;
  brand: Brand;
  lowest_price: number;
  creator:Shop;

  constructor(id:number ,reference:number, name:string, warehouse: string, details: string,creator: Shop, cat: Category, brand: Brand, qty_sold: number = 0,lowest: number = 10000 ) {
    this.reference_number = reference;
    this.id = id;
    this.name = name;
    this.warehouse = warehouse;
    this.details = details;
    this.qty_sold = qty_sold;
    this.creator = creator;
    this.category  = cat;
    this.brand = brand;
    this.lowest_price = lowest;
  }
}
