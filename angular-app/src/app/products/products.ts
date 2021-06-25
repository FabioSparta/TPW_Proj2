import {Category} from "../categories/category";
import {Brand} from "../brands/brand";
import {Shop} from "../shops/shop";

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
