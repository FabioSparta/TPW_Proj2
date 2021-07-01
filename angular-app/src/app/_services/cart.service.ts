import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {CartItem} from "../_models/cartItem";

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private baseURL= REST_API_BASE_URL + "/products"

  constructor(private http:HttpClient) { }

  addCart(id:number):Observable<any>{
    console.log("I was called");
    const url = REST_API_BASE_URL + "/account/cart/add/"+id;
    console.log(url);
    return this.http.get<any>(url);
  }

  remCart(id:number):Observable<any>{
    const url = REST_API_BASE_URL + "/account/cart/rem/"+id;
    return this.http.get<any>(url);
  }

  buyCart(id:number):Observable<any>{
    const url = REST_API_BASE_URL + "/account/cart/rem/"+id;
    return this.http.get<any>(url);
  }

  getCart():Observable<CartItem[]>{
    const url = REST_API_BASE_URL + "/account/cart";
    return this.http.get<CartItem[]>(url);
  }
}
