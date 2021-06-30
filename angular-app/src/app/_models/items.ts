import {Shop} from "./shop";
import {Product} from "./products";

export class Item {
  id: number;
  price: number;
  shop?: Shop;
  product?: Product;
  stock: number;

  constructor(id:number ,price:number, stock:number, product: Product, shop: Shop) {
    this.price = price;
    this.id = id;
    this.stock = stock;
    this.product = product;
    this.shop = shop;
  }
}
