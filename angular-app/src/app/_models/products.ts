import {Category} from "./category";
import {Brand} from "./brand";
import {Shop} from "./shop";

export class Product{
  id?: number;
  reference_number: number;
  name: string;
  details: string;
  warehouse: string;
  qty_sold: number;
  image?: string
  category: Category;
  brand: Brand;
  lowest_price: number;
  creator?:Shop;
  shopId?: string | null;

  constructor(reference:number, name:string, warehouse: string, details: string,cat: Category, brand: Brand) {
    this.reference_number = reference;
    this.name = name;
    this.warehouse = warehouse;
    this.details = details;
    this.qty_sold = 0;
    this.category  = cat;
    this.brand = brand;
    this.lowest_price = 1000000;
  }
}
