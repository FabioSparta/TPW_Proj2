import {Shop} from "./shop";
import {Product} from "./products";

export class Item {
  id: number;
  price: number;
  shop?: Shop;
  product?: Product;
  stock: number;
  shopId?: string | null;

  constructor(price:number, stock:number, product: Product) {
    this.price = price;
    this.stock = stock;
    this.product =  product;
    this.id = 0
  }
}
