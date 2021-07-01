import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";

@Injectable({
  providedIn: 'root'
})
export class WishlistService {

 private baseURL= REST_API_BASE_URL + "/products"

  constructor(private http:HttpClient) { }

  isWished(id:number):Observable<boolean>{
    const url = REST_API_BASE_URL + "/shop/products/wished/"+id;
    return this.http.get<boolean>(url);
  }
}
