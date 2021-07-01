import { Injectable } from '@angular/core';
import {Product} from "../_models/products";
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {Item} from "../_models/items";

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class ProductsService {
  private baseURL= REST_API_BASE_URL + "/products/"

  constructor(private http:HttpClient) { }

  getProducts():Observable<Product[]> {
    const url = this.baseURL + "?all"
    return this.http.get<Product[]>(url);
  }

  getShopProducts():Observable<Product[]> {
    const url = this.baseURL
    return this.http.get<Product[]>(url);
  }

  getProduct(id: number):Observable<Product> {
    const url = this.baseURL + id;
    return this.http.get<Product>(url);
  }

  createProduct(prod:Product):Observable<any>{
    const url = this.baseURL + "create";
    console.log(prod)
    return this.http.post(url,prod,httpOptions);
  }

  updateProduct(prod: Product):Observable<any>{
    const url = this.baseURL + "edit/"+prod.id;
    return this.http.put(url,prod,httpOptions);
  }

  deleteProduct(id: number):Observable<any>{
    const url = this.baseURL + "delete/"+id;
    return this.http.delete(url,httpOptions);
  }

  getHotDeals():Observable<Product[]> {
    const url = this.baseURL + "hotdeals";
    return this.http.get<Product[]>(url);
  }

  getNewArrivals():Observable<Product[]> {
    const url = this.baseURL + "newarrivals";
    return this.http.get<Product[]>(url);
  }

  searchProductsByCat(cat:string):Observable<Product[]>{
    const url = this.baseURL + "search?category="+cat;
    return this.http.get<Product[]>(url);
  }

  searchProductsByKeyAndCat(key:string,cat:string):Observable<Product[]>{
    const url = this.baseURL + "search?name="+key+"&category="+cat;
    return this.http.get<Product[]>(url);
  }

  searchAllProducts():Observable<Product[]>{
    const url = this.baseURL + "search";
    return this.http.get<Product[]>(url);
  }
}
