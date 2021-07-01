import { Injectable } from '@angular/core';
import {Shop} from "../_models/shop";
import {Observable} from "rxjs/internal/Observable";
import {HttpClient,HttpHeaders} from "@angular/common/http";
import {REST_API_BASE_URL} from "../GlobalVars";

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
}

