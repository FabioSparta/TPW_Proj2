import { Injectable } from '@angular/core';
import {Shop} from "../_models/shop";
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {User} from "../_models/user";

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})

export class ShopsService {
  private baseURL= REST_API_BASE_URL + "/shops"

  constructor(private http:HttpClient) { }

  getShops():Observable<Shop[]> {
    const url = this.baseURL
    return this.http.get<Shop[]>(url);
  }

  getShopDetails(id: number): Observable<Shop>{
    const url = this.baseURL + '/' + id;
    return this.http.get<Shop>(url)
  }
/*
  getShopInfo():Observable<any> {
    const url = this.baseURL + "/info"
    return this.http.get<Shop>(url);
  }

  updateShop(shop: {}): Observable<any>  {
    console.log("shop right before post")
    console.log(shop)
    const url = this.baseURL + '/info/update';
    return this.http.put<any>(url,shop, httpOptions);
  }


  newAddress(address: {}): Observable<any>  {
    const url = this.baseURL + '/address/add';
    return this.http.post<any>(url, address, httpOptions);
  }

  updateAddress(address: {}): Observable<any>  {
    const url = this.baseURL + '/address/update';
    return this.http.put<any>(url,address, httpOptions);
  }*/
}

