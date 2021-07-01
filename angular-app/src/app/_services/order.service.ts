import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";
import {Observable} from "rxjs/internal/Observable";
import {Order} from "../_models/order";

const httpOptions = {
  headers : new HttpHeaders({'Content-Type': 'application/json'})
};


@Injectable({
  providedIn: 'root'
})

export class OrderService {

  private baseURL= REST_API_BASE_URL + "/account/orders"

  constructor(private http:HttpClient) { }

  getOrders():Observable<Order[]> {
    return this.http.get<Order[]>(this.baseURL);
  }
}
