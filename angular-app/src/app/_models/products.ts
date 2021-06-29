import {Category} from "./category";
import {Brand} from "../clientside/brands/brand";
import {Shop} from "./shop";

export class Product{
  id?: number;
  reference_number?: number;
  name?: string;
  details?:string;
  warehouse?:string;
  qty_sold?:number;
  image?:string // string for url ?
  category?:Category
  brand?:Brand;
  lowest_price?: number;
  creator?:Shop;
}
