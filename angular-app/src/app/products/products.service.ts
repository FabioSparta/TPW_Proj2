import { Injectable } from '@angular/core';
import {Product} from "./products";
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
  private baseURL= REST_API_BASE_URL + "/prods"

  constructor(private http:HttpClient) { }

  getProducts():Observable<Product[]> {
    const url = this.baseURL
    return this.http.get<Product[]>(url);
  }

  getHotDeals():Observable<Product[]> {
    const url = this.baseURL + "/hotdeals";
    return this.http.get<Product[]>(url);
  }

  getNewArrivals():Observable<Product[]> {
    const url = this.baseURL + "/newarrivals";
    return this.http.get<Product[]>(url);
  }

}
