import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {Wishlist} from "../_models/wishlist";
import {Product} from "../_models/products";


const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class WishlistService {

 private baseURL= REST_API_BASE_URL + "/products"

  constructor(private http:HttpClient) { }

  getWishList():Observable<Product[]>{
    const url = REST_API_BASE_URL + "/account/wishlist"
    return this.http.get<Product[]>(url);
  }

  addWishList(prod_id:number):Observable<any>{
    const url = REST_API_BASE_URL + "/account/wishlist/add"
    return this.http.post<number>(url, {'prod_id':prod_id},httpOptions);
  }

  remWishList(prod_id:number):Observable<any>{
    const url = REST_API_BASE_URL + "/account/wishlist/rem/"+prod_id
    return this.http.delete<number>(url);
  }

  isWished(id:number):Observable<boolean>{
    const url = REST_API_BASE_URL + "/shop/products/wished/"+id;
    return this.http.get<boolean>(url);
  }
}
