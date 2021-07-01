import { Injectable } from '@angular/core';
import {Product} from "../_models/products";
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";

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
    const url = this.baseURL
    return this.http.get<Product[]>(url);
  }

  getProduct(id: number):Observable<Product> {
    const url = this.baseURL + id;
    return this.http.get<Product>(url);
  }

  createProduct(prod:Product):Observable<any>{
    const url = this.baseURL + "create";
    return this.http.post(url,prod,httpOptions); // ver a situacao do price
  }

  updateProduct(prod: Product):Observable<any>{
    const url = this.baseURL + "edit/"+prod.id;
    return this.http.put(url,prod,httpOptions);
  }

  deleteProduct(prod: Product):Observable<any>{
    const url = this.baseURL + "delete/"+prod.id;
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

}
